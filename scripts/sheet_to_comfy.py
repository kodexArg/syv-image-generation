#!/usr/bin/env python3
"""Submit a character render to ComfyUI (v7 / Z-Image Turbo).

Thin executor, not a prompt compiler. Prompt text comes in 2 short parts —
`scene` (short, fixed, reusable across a whole shoot) and `character` (a
placeholder, empty by default: fill it per-render with a specific person +
action) — concatenated at generation time. This script only:
  1. reads the syv-pj sheet for `edad`/`atributos.cuerpo` (slider math),
  2. builds the v7 API graph (3 sliders + 0-2 optional style LoRAs chained
     after them, exactly like zit-v7.json's node 7/8 slots),
  3. submits it to ComfyUI and waits for the output filename(s).

CFG-1 turbo models barely listen to long prompts — keep `scene` short
(SHARED_SCENE below is the ~20-word default: a misty Dársena alley at night,
lifted from syv-docs canon, not a paragraph of world-building). `character`
is meant to stay empty unless you're describing one specific person/action
for this render.

Usage (library):
    from sheet_to_comfy import run_generation
    result = run_generation(
        "sor-sofia-guardaespaldas", character="a woman in a dark habit, sheathed sword at her hip",
        loras=[("IllusT1_v9_Bukacheret.safetensors", 0.82)],
        seed=1234, timestamp="20260701-120000",
    )

Usage (CLI):
    python3 sheet_to_comfy.py <slug> ["<character>"] [--scene "..."] [--timestamp TS] [--seed N]
        [--lora NAME:WEIGHT ...]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

SHEETS_DIR = Path.home() / "Dev" / "SyV" / "syv-pj" / "resources" / "personajes"

COMFYUI_URL = "http://127.0.0.1:8188"
UNET_NAME = "zimageTurboByStable_2602Q8.gguf"
CLIP_NAME = "qwen_3_4b.safetensors"
VAE_NAME = "ae.safetensors"
AGE_LORA = "ZIT-age-slider.safetensors"
FAT_LORA = "ZIT-skinny-fat-slider.safetensors"
MUSCLE_LORA = "ZIT-hulking-muscular-slider.safetensors"

WIDTH = 704
HEIGHT = 960
STEPS = 9
CFG = 1.0
SHIFT = 3.0
SAMPLER = "res_multistep"
SCHEDULER = "simple"

# Short, natural, token-lean scene line — detective-snapshot framing, not a
# world-building paragraph. CFG-1 turbo barely listens past the first dozen
# words anyway, so every extra clause here is wasted weight. Grounded in
# syv-docs canon (Ciudad Dársena: perpetual fog off the Río de la Plata,
# corroded concrete, acid rain, a "callejón" — one of the Microcentro's
# "Callejones Secretos") but described as a photo, never namedropping the
# universe. Kept fixed across a shoot; `character` below is the variable.
SHARED_SCENE = (
    "Night street photo, black wet cobblestone alley, thick fog, "
    "rusted concrete walls, flickering neon reflections in puddles, "
    "grainy noir tone."
)


# ---------------------------------------------------------------------------
# Sheet reader — only what the sliders need (edad, atributos.cuerpo, genero)
# ---------------------------------------------------------------------------

def find_sheet_path(slug: str) -> Path:
    p = SHEETS_DIR / f"{slug}.md"
    if p.exists():
        return p
    raise FileNotFoundError(f"No syv-pj sheet found for slug '{slug}' (looked in {SHEETS_DIR})")


def load_sheet(slug: str) -> dict[str, Any]:
    path = find_sheet_path(slug)
    fm = path.read_text(encoding="utf-8").split("---", 2)[1]

    def scalar(key: str, default: str = "") -> str:
        m = re.search(rf"^{key}:\s*(.*)$", fm, re.M)
        if not m:
            return default
        value = re.sub(r"\s+#.*$", "", m.group(1))  # strip trailing YAML comment
        return value.strip().strip('"').strip("'")

    def cuerpo() -> int:
        m = re.search(r"^atributos:\n((?:  \w+:\s*-?\d+\n?)+)", fm, re.M)
        if not m:
            return 3
        for line in m.group(1).splitlines():
            kv = re.match(r"\s+cuerpo:\s*(-?\d+)", line)
            if kv:
                return int(kv.group(1))
        return 3

    return {
        "slug": scalar("slug", slug),
        "nombre": scalar("nombre", slug),
        "edad": int(scalar("edad") or 30),
        "genero": scalar("genero", "m"),
        "cuerpo": cuerpo(),
        "source_path": path,
    }


# ---------------------------------------------------------------------------
# Sliders — v7 workflow expects age/fat/muscle as LoraLoader strengths.
# Starting points, not gospel — dial per-render.
# ---------------------------------------------------------------------------

def compute_sliders(sheet: dict[str, Any]) -> dict[str, float]:
    age_val = (sheet["edad"] // 10) - 3
    fat_val = sheet["cuerpo"] - 3
    muscle_val = sheet["cuerpo"] - 3
    # LORA.md author warning: above +2 a woman tends to masculinize; the
    # documented female-safe zone is +0.5..+1.5, and +1.5 (the top edge)
    # still rendered male once stacked with combat gear (Sofía, 2026-07-01).
    # Ceiling kept at +1.0 for real margin — don't raise without re-testing.
    muscle_ceiling = 1.0 if sheet.get("genero") == "f" else 3.0
    return {
        "age": float(max(-3, min(3, age_val))),
        "fat": float(max(-1, min(1, fat_val))),
        "muscle": float(max(-2, min(muscle_ceiling, muscle_val))),
    }


# ---------------------------------------------------------------------------
# v7 API-format ComfyUI workflow — mirrors zit-v7.json. Style LoRAs are
# optional and chained after the 3 sliders (same position as v7's node 7/8
# STYLE LoRA slots), 0-2 of them; omit `loras` entirely for the bare path.
# ---------------------------------------------------------------------------

def build_v7_api_workflow(
    scene: str,
    character: str,
    sliders: dict[str, float],
    seed: int,
    filename_prefix: str,
    loras: list[tuple[str, float]] | None = None,
) -> dict[str, Any]:
    graph: dict[str, Any] = {
        "1": {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": UNET_NAME}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": CLIP_NAME, "type": "lumina2", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": VAE_NAME}},
        "4": {
            "class_type": "LoraLoader",
            "inputs": {
                "model": ["1", 0], "clip": ["2", 0],
                "lora_name": AGE_LORA, "strength_model": sliders["age"], "strength_clip": sliders["age"],
            },
        },
        "5": {
            "class_type": "LoraLoader",
            "inputs": {
                "model": ["4", 0], "clip": ["4", 1],
                "lora_name": FAT_LORA, "strength_model": sliders["fat"], "strength_clip": sliders["fat"],
            },
        },
        "6": {
            "class_type": "LoraLoader",
            "inputs": {
                "model": ["5", 0], "clip": ["5", 1],
                "lora_name": MUSCLE_LORA, "strength_model": sliders["muscle"], "strength_clip": sliders["muscle"],
            },
        },
    }

    # chain 0-2 style LoRAs after the sliders (node ids 7, 8 — same slots v7 uses)
    model_link, clip_link = ["6", 0], ["6", 1]
    for i, (lora_name, weight) in enumerate(loras or []):
        node_id = str(7 + i)
        graph[node_id] = {
            "class_type": "LoraLoader",
            "inputs": {
                "model": model_link, "clip": clip_link,
                "lora_name": lora_name, "strength_model": weight, "strength_clip": weight,
            },
        }
        model_link, clip_link = [node_id, 0], [node_id, 1]

    graph.update({
        "9": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": model_link, "shift": SHIFT}},
        "10": {"class_type": "PrimitiveStringMultiline", "inputs": {"value": scene}},
        "11": {"class_type": "PrimitiveStringMultiline", "inputs": {"value": character}},
        "13": {
            "class_type": "StringConcatenate",
            "inputs": {"string_a": ["10", 0], "string_b": ["11", 0], "delimiter": " "},
        },
        "15": {"class_type": "CLIPTextEncode", "inputs": {"clip": clip_link, "text": ["13", 0]}},
        "16": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["15", 0]}},
        "17": {"class_type": "EmptySD3LatentImage", "inputs": {"width": WIDTH, "height": HEIGHT, "batch_size": 1}},
        "18": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["9", 0], "positive": ["15", 0], "negative": ["16", 0], "latent_image": ["17", 0],
                "seed": seed, "steps": STEPS, "cfg": CFG,
                "sampler_name": SAMPLER, "scheduler": SCHEDULER, "denoise": 1.0,
            },
        },
        "19": {"class_type": "VAEDecode", "inputs": {"samples": ["18", 0], "vae": ["3", 0]}},
        "20": {
            "class_type": "SaveImage",
            "inputs": {"images": ["19", 0], "filename_prefix": filename_prefix},
        },
    })
    return graph


def _deterministic_seed(key: str) -> int:
    digest = hashlib.sha256(key.encode()).digest()
    return int.from_bytes(digest[:4], "big") & 0x7FFFFFFF


def submit_generation(
    slug: str,
    scene: str,
    character: str,
    sliders: dict[str, float],
    timestamp: str,
    seed: int | None = None,
    loras: list[tuple[str, float]] | None = None,
    tag: str | None = None,
) -> dict[str, Any]:
    """POST the v7 graph to ComfyUI's /prompt endpoint.

    `seed`: pass an explicit int to force the same seed across style runs
    (e.g. comparing 3 LoRAs on the same character); omitted -> deterministic
    from slug+timestamp, as before.
    `tag`: extra filename suffix (e.g. a lora key) so same-timestamp runs of
    the same slug under different styles don't overwrite each other.
    """
    name = f"{slug}-{timestamp}" + (f"-{tag}" if tag else "")
    if seed is None:
        seed = _deterministic_seed(f"{slug}:{timestamp}")
    graph = build_v7_api_workflow(scene, character, sliders, seed=seed, filename_prefix=name, loras=loras)

    payload = json.dumps({"prompt": graph, "client_id": name}).encode()
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt", data=payload, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"ComfyUI rejected the prompt: {e.read().decode()}") from e

    return {"prompt_id": body["prompt_id"], "workflow_name": name, "seed": seed}


def wait_for_generation(prompt_id: str, timeout: float = 180.0) -> list[str]:
    """Poll /history/<prompt_id> until images appear; return their filenames."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        with urllib.request.urlopen(f"{COMFYUI_URL}/history/{prompt_id}", timeout=10) as resp:
            history = json.loads(resp.read())
        entry = history.get(prompt_id)
        if entry and entry.get("outputs"):
            files = [
                img["filename"]
                for node_out in entry["outputs"].values()
                for img in node_out.get("images", [])
            ]
            if files:
                return files
        time.sleep(2)
    raise TimeoutError(f"ComfyUI generation {prompt_id} did not finish within {timeout}s")


def run_generation(
    slug: str,
    character: str = "",
    scene: str | None = None,
    timestamp: str | None = None,
    seed: int | None = None,
    loras: list[tuple[str, float]] | None = None,
    tag: str | None = None,
) -> dict[str, Any]:
    """One-call entry point: load sheet, compute sliders, submit, wait.

    `character` defaults to empty (pure scene shot, no subject described) —
    fill it in per-render with a specific person/action.
    `scene` defaults to SHARED_SCENE (the short misty-alley line); override
    only if this render needs a genuinely different setting.

    Returns {"prompt_id", "workflow_name", "seed", "files": [...], "sliders"}.
    """
    sheet = load_sheet(slug)
    sliders = compute_sliders(sheet)
    scene = scene if scene is not None else SHARED_SCENE
    timestamp = timestamp or time.strftime("%Y%m%d-%H%M%S")
    submission = submit_generation(slug, scene, character, sliders, timestamp, seed=seed, loras=loras, tag=tag)
    files = wait_for_generation(submission["prompt_id"])
    return {**submission, "files": files, "sliders": sliders}


def _parse_lora_arg(spec: str) -> tuple[str, float]:
    name, _, weight = spec.rpartition(":")
    if not name:
        raise argparse.ArgumentTypeError(f"--lora expects NAME:WEIGHT, got '{spec}'")
    return name, float(weight)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("slug", help="syv-pj character slug")
    ap.add_argument("character", nargs="?", default="", help="character/action placeholder (default: empty)")
    ap.add_argument("--scene", default=None, help="override the shared scene line (default: SHARED_SCENE)")
    ap.add_argument("--timestamp", default=None, help="override run timestamp (default: now)")
    ap.add_argument("--seed", type=int, default=None, help="force a specific seed (default: derived from slug+timestamp)")
    ap.add_argument(
        "--lora", action="append", type=_parse_lora_arg, default=[], metavar="NAME:WEIGHT",
        help="style LoRA to chain after the sliders, e.g. --lora IllusT1_v9_Bukacheret.safetensors:0.82 "
             "(repeatable, max 2, matches v7's two style-LoRA slots)",
    )
    ap.add_argument("--tag", default=None, help="extra filename suffix so parallel style runs don't collide")
    args = ap.parse_args()

    try:
        result = run_generation(
            args.slug, args.character, args.scene, args.timestamp,
            seed=args.seed, loras=args.lora or None, tag=args.tag,
        )
    except (FileNotFoundError, RuntimeError, TimeoutError, urllib.error.URLError) as e:
        print(f"FAILED: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"submitted '{result['workflow_name']}' (prompt_id={result['prompt_id']}, seed={result['seed']})")
    print(f"sliders: {result['sliders']}")
    for fn in result["files"]:
        print(f"-> {fn}")


if __name__ == "__main__":
    main()
