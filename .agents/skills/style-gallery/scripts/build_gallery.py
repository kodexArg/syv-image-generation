#!/usr/bin/env python3
"""Build a style-comparison gallery for ComfyUI.

Usage:
    python3 build_gallery.py <spec.json> [--dry-run]

    --dry-run   Build HTML from solid-color placeholder images (no GPU/ComfyUI needed).

The spec JSON schema is documented in SKILL.md.
"""
import argparse
import html as _h
import json
import os
import shutil
import sys
import time
import urllib.request
from pathlib import Path

# ── defaults (overridable via spec) ──────────────────────────────────────────
_DEFAULTS = {
    "pony_prefix": "score_9, score_8_up, score_7_up, rating_safe, solo, one person, ",
    "seed": 7777,
    "steps": 30,
    "cfg": 7.0,
    "sampler": "dpmpp_2m",
    "scheduler": "karras",
    "checkpoint": "zavyfantasiaxlPDXL_v20.safetensors",
    "width": 832,
    "height": 1344,
    "comfyui_host": "http://127.0.0.1:8188",
    "comfyui_output_dir": "/home/kodex/ComfyUI/output",
    "poll_interval": 2,
    "timeout": 300,
}


# ── ComfyUI helpers ───────────────────────────────────────────────────────────

def _workflow(pos: str, neg: str, prefix: str, cfg: dict) -> dict:
    """Build a minimal SDXL txt2img workflow dict."""
    return {
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": cfg["checkpoint"]},
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": cfg["width"],
                "height": cfg["height"],
                "batch_size": 1,
            },
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": pos, "clip": ["4", 1]},
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": neg, "clip": ["4", 1]},
        },
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "seed": cfg["seed"],
                "steps": cfg["steps"],
                "cfg": cfg["cfg"],
                "sampler_name": cfg["sampler"],
                "scheduler": cfg["scheduler"],
                "denoise": 1.0,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0],
            },
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {"filename_prefix": prefix, "images": ["8", 0]},
        },
    }


def _post_prompt(host: str, wf: dict) -> str:
    body = json.dumps({"prompt": wf}).encode()
    req = urllib.request.Request(
        host + "/prompt",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    return json.load(urllib.request.urlopen(req))["prompt_id"]


def _wait_for_image(host: str, prompt_id: str, timeout: int, interval: int) -> str:
    """Poll /history until the image filename appears; return the filename."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        data = json.load(urllib.request.urlopen(host + f"/history/{prompt_id}"))
        if prompt_id in data:
            for node in data[prompt_id].get("outputs", {}).values():
                for img in node.get("images", []):
                    return img["filename"]
        time.sleep(interval)
    raise TimeoutError(f"ComfyUI did not finish prompt {prompt_id} within {timeout}s")


def _generate_image(pos: str, neg: str, prefix: str, cfg: dict, dst: Path) -> None:
    """Send one prompt to ComfyUI and copy the result to dst."""
    wf = _workflow(pos, neg, prefix, cfg)
    pid = _post_prompt(cfg["comfyui_host"], wf)
    print(f"[queued] {prefix}  pid={pid}", flush=True)
    fn = _wait_for_image(
        cfg["comfyui_host"], pid, cfg["timeout"], cfg["poll_interval"]
    )
    src = Path(cfg["comfyui_output_dir"]) / fn
    shutil.copy(src, dst)
    print(f"[done]   {prefix} -> {dst}", flush=True)


# ── placeholder image for --dry-run ──────────────────────────────────────────

def _placeholder_image(dst: Path, width: int, height: int, index: int) -> None:
    """Write a solid-color PNG using only stdlib (no Pillow dependency)."""
    # Palette: cycle through muted SyV colors
    palette = [
        (123, 138, 78),   # olive
        (143, 184, 214),  # celeste
        (243, 238, 228),  # cream
        (12, 11, 9),      # near-black → lightened for visibility
        (90, 100, 60),
    ]
    r, g, b = palette[index % len(palette)]
    if (r, g, b) == (12, 11, 9):
        r, g, b = 40, 38, 32  # lighten so it's not invisible

    try:
        from PIL import Image
        img = Image.new("RGB", (width, height), (r, g, b))
        img.save(dst)
    except ImportError:
        # PIL not available: write a minimal valid 1×1 PNG then note it
        # (1×1 is valid; aspect-ratio CSS still enforces card shape)
        import struct, zlib

        def _png_chunk(tag: bytes, data: bytes) -> bytes:
            c = struct.pack(">I", len(data)) + tag + data
            return c + struct.pack(">I", zlib.crc32(c[4:]) & 0xFFFFFFFF)

        ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
        idat = zlib.compress(bytes([0, r, g, b]))
        png = (
            b"\x89PNG\r\n\x1a\n"
            + _png_chunk(b"IHDR", ihdr)
            + _png_chunk(b"IDAT", idat)
            + _png_chunk(b"IEND", b"")
        )
        dst.write_bytes(png)


# ── HTML gallery ──────────────────────────────────────────────────────────────

def _build_html(title: str, options_data: list[dict], neg: str, cfg: dict) -> str:
    """
    options_data: list of {label, desc, full_prompt, img_filename}
    Returns the complete HTML string.
    """
    n = len(options_data)
    # 5-up grid; fall back to fewer columns for small sets
    cols = min(n, 5)

    cards_html = ""
    for i, opt in enumerate(options_data, start=1):
        cards_html += f"""<figure>
      <div class="num">{i}</div>
      <img src="./{opt['img_filename']}" alt="{_h.escape(opt['label'])}">
      <figcaption>
        <h2>{opt['label']}</h2>
        <p>{opt['desc']}</p>
        <pre class="prompt">{_h.escape(opt['full_prompt'])}</pre>
      </figcaption>
    </figure>
"""

    footer_neg = _h.escape(neg)
    footer_params = (
        f"{_h.escape(cfg['checkpoint'])} &middot; "
        f"{_h.escape(cfg['sampler'])} / {_h.escape(cfg['scheduler'])} &middot; "
        f"{cfg['steps']} steps &middot; cfg {cfg['cfg']} &middot; "
        f"seed {cfg['seed']} &middot; "
        f"{cfg['width']}&times;{cfg['height']}"
    )

    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{_h.escape(title)}</title>
<style>
:root{{--olive:#7B8A4E;--celeste:#8FB8D6;--cream:#F3EEE4;--black:#0C0B09}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--black);color:var(--cream);
  font-family:'Segoe UI',system-ui,sans-serif}}
header{{padding:26px 32px 6px}}
h1{{margin:0;font-size:23px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--celeste)}}
header p{{margin:6px 0 0;color:#9a978d;font-size:13.5px}}
.grid{{display:grid;grid-template-columns:repeat({cols},1fr);gap:16px;
  padding:22px 32px 44px}}
@media(max-width:1200px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}
figure{{margin:0;background:#15140f;border:1px solid #2a2820;border-radius:10px;
  overflow:hidden;position:relative;display:flex;flex-direction:column}}
figure img{{width:100%;display:block;aspect-ratio:13/21;object-fit:cover;
  background:#000}}
.num{{position:absolute;top:10px;left:10px;width:30px;height:30px;
  background:var(--olive);color:var(--black);border-radius:50%;font-weight:700;
  display:flex;align-items:center;justify-content:center;font-size:16px}}
figcaption{{padding:11px 13px 14px}}
figcaption h2{{margin:0 0 4px;font-size:14.5px;color:var(--celeste)}}
figcaption p{{margin:0 0 8px;font-size:12px;line-height:1.45;color:#b8b4a6}}
pre.prompt{{margin:0;font-family:'DM Mono',ui-monospace,monospace;font-size:9.5px;
  line-height:1.4;color:#8f8c82;background:#0c0b09;border:1px solid #232118;
  border-radius:6px;padding:8px;white-space:pre-wrap;word-break:break-word;
  max-height:150px;overflow:auto}}
footer{{padding:0 32px 40px;color:#6f6c63;font-size:11px;
  font-family:ui-monospace,monospace}}
footer b{{color:#9a978d}}
</style>
</head>
<body>
<header>
  <h1>{_h.escape(title)}</h1>
  <p>{n} opciones &middot; {cfg['width']}&times;{cfg['height']} (Fibonacci 13:21)
     &middot; seed {cfg['seed']} &middot; prompt debajo de cada imagen.</p>
</header>
<div class="grid">
{cards_html}</div>
<footer>
  <b>negativo (compartido):</b> {footer_neg}<br>
  <b>params:</b> {footer_params}
</footer>
</body>
</html>"""


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a ComfyUI style-comparison gallery from a spec JSON."
    )
    parser.add_argument("spec", help="Path to the options-spec JSON file.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build HTML from placeholder images without calling ComfyUI.",
    )
    args = parser.parse_args()

    spec_path = Path(args.spec).resolve()
    if not spec_path.exists():
        print(f"ERROR: spec not found: {spec_path}", file=sys.stderr)
        sys.exit(1)

    with spec_path.open() as f:
        spec = json.load(f)

    # merge defaults
    cfg: dict = {**_DEFAULTS, **{k: v for k, v in spec.items() if k not in ("options", "title", "subject", "negative", "output_dir")}}

    title = spec.get("title", "SyV · style gallery")
    subject = spec.get("subject", "")
    negative = spec.get("negative", "score_6, score_5, score_4")
    output_dir = Path(spec.get("output_dir", "/tmp/style_gallery")).resolve()
    options = spec["options"]

    output_dir.mkdir(parents=True, exist_ok=True)

    options_data = []
    for i, opt in enumerate(options, start=1):
        img_filename = f"{i}.png"
        dst = output_dir / img_filename
        full_prompt = cfg["pony_prefix"] + opt["style_clause"] + subject

        if args.dry_run:
            print(f"[dry-run] placeholder {img_filename}", flush=True)
            _placeholder_image(dst, cfg["width"], cfg["height"], i - 1)
        else:
            prefix = f"syv_gallery_{i}"
            _generate_image(full_prompt, negative, prefix, cfg, dst)

        options_data.append(
            {
                "label": opt["label"],
                "desc": opt.get("desc", ""),
                "full_prompt": full_prompt,
                "img_filename": img_filename,
            }
        )

    html = _build_html(title, options_data, negative, cfg)
    index_path = output_dir / "index.html"
    index_path.write_text(html, encoding="utf-8")

    file_url = index_path.as_uri()
    print(f"[gallery] {index_path}", flush=True)
    print(f"[url]     {file_url}", flush=True)


if __name__ == "__main__":
    main()
