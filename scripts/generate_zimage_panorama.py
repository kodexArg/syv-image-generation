#!/usr/bin/env python3
"""Genera el panorama 5x5 Z-Image Turbo (GGUF Q8) en ComfyUI.

Grafo fiel al template oficial `image_z_image_turbo.json`:
  UnetLoaderGGUF -> ModelSamplingAuraFlow(shift=3) -> KSampler(res_multistep/simple/8/cfg1)
  CLIPLoader(qwen_3_4b, type=lumina2) -> CLIPTextEncode(+) -> ConditioningZeroOut(-)
  VAELoader(ae) -> VAEDecode -> SaveImage

Uso:
  python3 generate_zimage_panorama.py [--limit N] [--only slug] [--seed-base 1000]
"""
import argparse, json, time, urllib.request, urllib.error, sys
from pathlib import Path

COMFY = "http://127.0.0.1:8188"
HERE = Path(__file__).resolve().parent
PROMPTS = HERE.parent / "prompts/inbox/20260628-z-image-turbo-panorama/prompts.json"

UNET = "zimageTurboByStable_2602Q8.gguf"
CLIP = "qwen_3_4b.safetensors"
VAE = "ae.safetensors"


def build_workflow(positive: str, seed: int, w: int, h: int, prefix: str) -> dict:
    return {
        "1": {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": UNET}},
        "2": {"class_type": "ModelSamplingAuraFlow", "inputs": {"shift": 3.0, "model": ["1", 0]}},
        "3": {"class_type": "CLIPLoader", "inputs": {"clip_name": CLIP, "type": "lumina2", "device": "default"}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": positive, "clip": ["3", 0]}},
        "5": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["4", 0]}},
        "6": {"class_type": "EmptySD3LatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
        "7": {"class_type": "KSampler", "inputs": {
            "seed": seed, "steps": 8, "cfg": 1.0, "sampler_name": "res_multistep",
            "scheduler": "simple", "denoise": 1.0,
            "model": ["2", 0], "positive": ["4", 0], "negative": ["5", 0], "latent_image": ["6", 0]}},
        "8": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "9": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["8", 0]}},
        "10": {"class_type": "SaveImage", "inputs": {"filename_prefix": prefix, "images": ["9", 0]}},
    }


def post(workflow: dict) -> str:
    data = json.dumps({"prompt": workflow}).encode()
    req = urllib.request.Request(f"{COMFY}/prompt", data=data, headers={"Content-Type": "application/json"})
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=30).read())
    except urllib.error.HTTPError as e:
        print("  HTTP ERROR:", e.read().decode()[:500]); raise
    return r["prompt_id"]


def wait(pid: str, timeout=300) -> list:
    t0 = time.time()
    while time.time() - t0 < timeout:
        h = json.loads(urllib.request.urlopen(f"{COMFY}/history/{pid}", timeout=15).read())
        if pid in h:
            outs = h[pid].get("outputs", {})
            imgs = [i for n in outs.values() for i in n.get("images", [])]
            if imgs:
                return imgs
            if h[pid].get("status", {}).get("status_str") == "error":
                print("  EXEC ERROR:", json.dumps(h[pid].get("status", {}))[:600]); return []
        time.sleep(1.5)
    print("  TIMEOUT"); return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", type=str, default="")
    ap.add_argument("--seed-base", type=int, default=1000)
    a = ap.parse_args()

    spec = json.loads(PROMPTS.read_text())
    r = spec["recipe"]; w, h = r["width"], r["height"]
    items = spec["prompts"]
    if a.only:
        items = [p for p in items if p["slug"] == a.only]
    if a.limit:
        items = items[: a.limit]

    print(f"Generando {len(items)} imágenes @ {w}x{h}  (res_multistep/simple/8/cfg1, shift3)")
    results = []
    for i, p in enumerate(items):
        seed = a.seed_base + p["variant"] + 7 * sum(ord(c) for c in p["slug"][:4])
        prefix = f"zpan/{p['slug']}_v{p['variant']}"
        t0 = time.time()
        print(f"[{i+1}/{len(items)}] {p['slug']} v{p['variant']} ({p['label']}) seed={seed} ...", flush=True)
        pid = post(build_workflow(p["positive"], seed, w, h, prefix))
        imgs = wait(pid)
        dt = time.time() - t0
        if imgs:
            fn = imgs[0]["filename"]
            print(f"     OK {dt:.0f}s -> {fn}")
            results.append({**p, "seed": seed, "filename": fn, "subfolder": imgs[0].get("subfolder", "")})
        else:
            print(f"     FAIL {dt:.0f}s")
            results.append({**p, "seed": seed, "filename": None})

    out = PROMPTS.parent / "results.json"
    out.write_text(json.dumps({"recipe": r, "results": results}, ensure_ascii=False, indent=2))
    ok = sum(1 for x in results if x["filename"])
    print(f"\nListo: {ok}/{len(results)} OK -> {out}")


if __name__ == "__main__":
    main()
