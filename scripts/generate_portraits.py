#!/usr/bin/env python3
"""Generate ComfyUI propaganda-poster jobs for all syv-pj soldier records.

With --dry-run (DEFAULT): writes all prompts to build/portrait_prompts.json.
With --run: posts each job to http://127.0.0.1:8188 sequentially and polls
/history until complete.

Locates soldier records automatically:
  1. $SYV_PJ_PATH/resources/personajes/
  2. Sibling repo ../syv-pj/resources/personajes/ (relative to this repo)
  3. vendor/syv-pj/resources/personajes/ inside syv-pj-api

Records starting with '_' (MOC/index files) are skipped.
Records lacking a `lealtad/*` tag are included but army defaults to 'confederacion'.

Uso:
    uv run scripts/generate_portraits.py             # dry-run (default)
    uv run scripts/generate_portraits.py --dry-run   # same
    uv run scripts/generate_portraits.py --run        # post to ComfyUI
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = REPO_ROOT / "build"
COMFYUI_API = "http://127.0.0.1:8188"
POLL_INTERVAL = 2.0   # seconds between /history polls
POLL_TIMEOUT = 300.0  # seconds max wait per image

_CANDIDATE_ROOTS = [
    Path(os.environ.get("SYV_PJ_PATH", "")) if os.environ.get("SYV_PJ_PATH") else None,
    REPO_ROOT.parent / "syv-pj",
    REPO_ROOT.parent / "syv-pj-api" / "vendor" / "syv-pj",
]


def find_personajes_dir() -> Path:
    for root in _CANDIDATE_ROOTS:
        if root is None:
            continue
        candidate = root / "resources" / "personajes"
        if candidate.is_dir():
            return candidate
    sys.exit(
        "ERROR: No encontré resources/personajes/. "
        "Definí $SYV_PJ_PATH o corré desde dentro del ecosistema SyV."
    )


# ---------------------------------------------------------------------------
# Frontmatter parser (stdlib only — no PyYAML dependency)
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> dict[str, Any]:
    """Minimal YAML-ish frontmatter parser sufficient for syv-pj records.

    Handles: scalar values, lists (- item), nested dicts (key:\\n  subkey:).
    Does NOT handle full YAML; it covers the exact schema used in these files.
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip()
    return _parse_yaml_block(block.splitlines(), 0)[0]


def _parse_yaml_block(lines: list[str], indent: int) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        current_indent = len(line) - len(stripped)
        if current_indent < indent:
            break

        if stripped.startswith("- "):
            # This shouldn't happen at the top level; handled in list parsing
            break

        if ":" in stripped:
            colon = stripped.index(":")
            key = stripped[:colon].strip()
            rest = stripped[colon + 1:].strip()

            if rest == "" or rest == "|" or rest == ">":
                # Could be a list or nested dict — peek ahead
                i += 1
                if i < len(lines):
                    next_stripped = lines[i].lstrip()
                    next_indent = len(lines[i]) - len(next_stripped)
                    if next_stripped.startswith("- "):
                        # list
                        items = []
                        while i < len(lines):
                            ls = lines[i].lstrip()
                            li = len(lines[i]) - len(ls)
                            if not ls.startswith("- "):
                                break
                            item_val = ls[2:].strip()
                            # strip inline YAML quotes
                            if (item_val.startswith('"') and item_val.endswith('"')) or \
                               (item_val.startswith("'") and item_val.endswith("'")):
                                item_val = item_val[1:-1]
                            items.append(item_val)
                            i += 1
                        result[key] = items
                        continue
                    elif next_indent > current_indent:
                        # nested dict
                        sub, consumed = _parse_yaml_block(lines[i:], next_indent)
                        result[key] = sub
                        i += consumed
                        continue
                    else:
                        result[key] = None
                        continue
                else:
                    result[key] = None
                    continue
            else:
                # inline scalar
                val: Any = rest
                # strip inline YAML quotes
                if (val.startswith('"') and val.endswith('"')) or \
                   (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                # coerce simple types
                if val == "null" or val == "~":
                    val = None
                elif val == "true":
                    val = True
                elif val == "false":
                    val = False
                else:
                    try:
                        val = int(val)
                    except ValueError:
                        try:
                            val = float(val)
                        except ValueError:
                            pass
                result[key] = val
                i += 1
                continue
        else:
            i += 1
            continue

    return result, i


# ---------------------------------------------------------------------------
# Record loading
# ---------------------------------------------------------------------------

def load_records(personajes_dir: Path) -> list[dict[str, Any]]:
    records = []
    for md_file in sorted(personajes_dir.glob("*.md")):
        if md_file.name.startswith("_"):
            continue
        text = md_file.read_text(encoding="utf-8")
        fm = _parse_frontmatter(text)
        if not fm:
            continue
        # Only include soldiers (lealtad tag present, or faccion is military)
        tags = fm.get("tags", [])
        has_lealtad = any(t.startswith("lealtad/") for t in tags)
        faccion = fm.get("faccion", "")
        is_military = faccion in (
            "fuerzas_armadas", "iglesia", "resistencia_subterranea", "punteros"
        )
        if has_lealtad or is_military:
            records.append(fm)
    return records


# ---------------------------------------------------------------------------
# Dry run
# ---------------------------------------------------------------------------

def dry_run(records: list[dict[str, Any]], out_path: Path) -> list[dict[str, Any]]:
    # Import here so portrait_prompt.py is the single source of prompt logic
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from portrait_prompt import build_prompt  # noqa: PLC0415

    jobs = [build_prompt(r) for r in records]
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(jobs, indent=2, ensure_ascii=False), encoding="utf-8")

    # Per-army summary
    counts: dict[str, int] = {}
    for j in jobs:
        counts[j["army"]] = counts.get(j["army"], 0) + 1

    print(f"Dry-run: {len(jobs)} prompts -> {out_path}")
    for army, n in sorted(counts.items()):
        print(f"  {army}: {n} soldier(s)")
    return jobs


# ---------------------------------------------------------------------------
# Live run
# ---------------------------------------------------------------------------

def build_comfyui_workflow(job: dict[str, Any]) -> dict[str, Any]:
    """Standard 7-node SDXL txt2img graph."""
    return {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": job["model"]},
        },
        "2": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["1", 1],
                "text": job["positive"],
            },
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["1", 1],
                "text": job["negative"],
            },
        },
        "4": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": job["width"],
                "height": job["height"],
                "batch_size": 1,
            },
        },
        "5": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["1", 0],
                "positive": ["2", 0],
                "negative": ["3", 0],
                "latent_image": ["4", 0],
                "seed": job["seed"],
                "steps": job["steps"],
                "cfg": job["cfg"],
                "sampler_name": job["sampler"],
                "scheduler": job["scheduler"],
                "denoise": job["denoise"],
            },
        },
        "6": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["5", 0],
                "vae": ["1", 2],
            },
        },
        "7": {
            "class_type": "SaveImage",
            "inputs": {
                "images": ["6", 0],
                "filename_prefix": job["filename_prefix"],
            },
        },
    }


def post_and_wait(job: dict[str, Any]) -> None:
    import urllib.request  # stdlib only

    workflow = build_comfyui_workflow(job)
    payload = json.dumps({"prompt": workflow}).encode("utf-8")

    req = urllib.request.Request(
        f"{COMFYUI_API}/prompt",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        resp_data = json.loads(resp.read())
    prompt_id = resp_data.get("prompt_id")
    if not prompt_id:
        raise RuntimeError(f"No prompt_id in response: {resp_data}")

    print(f"  queued: {prompt_id}")

    # Poll /history until done
    deadline = time.monotonic() + POLL_TIMEOUT
    while time.monotonic() < deadline:
        time.sleep(POLL_INTERVAL)
        with urllib.request.urlopen(
            f"{COMFYUI_API}/history/{prompt_id}", timeout=10
        ) as resp:
            history = json.loads(resp.read())
        if prompt_id in history:
            outputs = history[prompt_id].get("outputs", {})
            images = []
            for node_out in outputs.values():
                images.extend(node_out.get("images", []))
            print(f"  done: {[img['filename'] for img in images]}")
            return

    raise TimeoutError(f"Timed out waiting for {job['slug']} ({POLL_TIMEOUT}s)")


def live_run(records: list[dict[str, Any]]) -> None:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from portrait_prompt import build_prompt  # noqa: PLC0415

    jobs = [build_prompt(r) for r in records]
    print(f"Posting {len(jobs)} jobs to {COMFYUI_API} ...")
    for job in jobs:
        print(f"\n[{job['slug']}] army={job['army']}")
        try:
            post_and_wait(job)
        except Exception as exc:
            print(f"  ERROR: {exc}", file=sys.stderr)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        dest="dry",
        help="Write prompts to build/portrait_prompts.json (default)",
    )
    mode.add_argument(
        "--run",
        action="store_false",
        dest="dry",
        help="Post jobs to ComfyUI at http://127.0.0.1:8188",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=BUILD_DIR / "portrait_prompts.json",
        help="Output path for dry-run JSON (default: build/portrait_prompts.json)",
    )
    args = ap.parse_args()

    personajes_dir = find_personajes_dir()
    print(f"Records from: {personajes_dir}")
    records = load_records(personajes_dir)
    print(f"Loaded {len(records)} soldier records")

    if args.dry:
        dry_run(records, args.out)
    else:
        live_run(records)


if __name__ == "__main__":
    main()
