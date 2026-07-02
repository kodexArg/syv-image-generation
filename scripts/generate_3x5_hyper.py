#!/usr/bin/env python3
"""Generate 10 images (5 chars x 2 models) for syv-character-3x5 Hyper-SD vs Lightning test.

Uses direct ComfyUI /prompt API with hand-crafted minimal graphs for:
- Lightning 4step (no lora)
- Hyper-SDXL 8step CFG LoRA on Zavy

Saves consistently named files to OUT_DIR:
  elian-quiroga-fusilero_lightning.png
  elian-quiroga-fusilero_hyper.png
  ...

Then ready for build_grid.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

import requests

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from _comfy_root import comfy_output  # noqa: E402

COMFY = "http://127.0.0.1:8188"
POLL = 1.5
TIMEOUT = 180.0

# 5 chars + their full prompts (crafted for hyper-real tenebrist military)
CHARS = [
    {
        "slug": "elian-quiroga-fusilero",
        "nombre": "Elián Quiroga",
        "positive": "photorealistic, hyperrealistic, RAW photo, ultra detailed skin texture pores and imperfections, realistic eyes with depth catchlights and subtle blood vessels, cinematic dramatic tenebrist chiaroscuro, strong directional side key light, deep shadows and high contrast, gritty atmospheric military realism, sharp focus on face, shallow depth of field, weathered skin details sweat and grime, realistic cloth wear and folds, 8k uhd, masterpiece, best quality, highly detailed, a 23 year old man, lean wiry build, tired glazed eyes, withdrawn hollow presence, raw young conscript, basic rank insignia, rifle shouldered infantry stance, cartridge belt, olive drab state-issue military uniform that is too large, instinctive alert tense posture, learning the trade door to door, Confederación urban military recruit in the barrios del muro, intense expression, Subordinación y Valor universe character",
        "negative": "score_6, score_5, score_4, cartoon, anime, illustration, drawing, painting, 3d render, plastic skin, doll-like, airbrushed, beauty filter, blurry, lowres, deformed, mutated, bad anatomy, extra limbs, fused fingers, missing fingers, watermark, text, logo, overexposed, underexposed, smooth, soft focus, duplicate",
        "seed": 711215499,
    },
    {
        "slug": "anibal-painemal-comandante",
        "nombre": "Aníbal Painemal",
        "positive": "photorealistic, hyperrealistic, RAW photo, ultra detailed skin texture pores and imperfections, realistic eyes with depth catchlights and subtle blood vessels, cinematic dramatic tenebrist chiaroscuro, strong directional side key light, deep shadows and high contrast, gritty atmospheric military realism, sharp focus on face, shallow depth of field, weathered skin details sweat and grime, realistic cloth wear and folds, 8k uhd, masterpiece, best quality, highly detailed, a 58 year old man, athletic build, alert focused eyes, commanding iron gaze straight spine, commander cabecilla, confident bearing and authority, worn red military uniform, pistol and binoculars, stubborn set jaw locked resolute gaze, weathered calm scarred face with disturbing deep facial scar across cheek, veteran composure, revolutionary leader, Ejército Rojo resistance commander, founder lineage, red army revolutionary, intense expression, Subordinación y Valor universe character",
        "negative": "score_6, score_5, score_4, cartoon, anime, illustration, drawing, painting, 3d render, plastic skin, doll-like, airbrushed, beauty filter, blurry, lowres, deformed, mutated, bad anatomy, extra limbs, fused fingers, missing fingers, watermark, text, logo, overexposed, underexposed, smooth, soft focus, duplicate",
        "seed": 638262774,
    },
    {
        "slug": "baltasar-quevedo-inquisidor",
        "nombre": "Baltasar Quevedo",
        "positive": "photorealistic, hyperrealistic, RAW photo, ultra detailed skin texture pores and imperfections, realistic eyes with depth catchlights and subtle blood vessels, cinematic dramatic tenebrist chiaroscuro, strong directional side key light, deep shadows and high contrast, gritty atmospheric military realism, sharp focus on face, shallow depth of field, weathered skin details sweat and grime, realistic cloth wear and folds, 8k uhd, masterpiece, best quality, highly detailed, a 28 year old man, athletic build, tired glazed eyes, withdrawn hollow presence, inquisitor initiate novicio, rank sash and cassock, consecrated sword raised crusader iconography holy warrior, heavy assault vest over long dark clerical cassock, stubborn set jaw locked resolute gaze, robust powerful build broad muscular frame, mole of muscle and dogma, Iglesia Inquisición crusader, second iniciado of the squad, intense expression, Subordinación y Valor universe character",
        "negative": "score_6, score_5, score_4, cartoon, anime, illustration, drawing, painting, 3d render, plastic skin, doll-like, airbrushed, beauty filter, blurry, lowres, deformed, mutated, bad anatomy, extra limbs, fused fingers, missing fingers, watermark, text, logo, overexposed, underexposed, smooth, soft focus, duplicate",
        "seed": 794655301,
    },
    {
        "slug": "iracema-chaman-pantano",
        "nombre": "Iracema",
        "positive": "photorealistic, hyperrealistic, RAW photo, ultra detailed skin texture pores and imperfections, realistic eyes with depth catchlights and subtle blood vessels, cinematic dramatic tenebrist chiaroscuro, strong directional side key light, deep shadows and high contrast, gritty atmospheric military realism, sharp focus on face, shallow depth of field, weathered skin details sweat and grime, realistic cloth wear and folds, 8k uhd, masterpiece, best quality, highly detailed, a 47 year old woman, lean wiry build, vacant trance gaze, otherworldly stillness, shipibo-conibo meraya curandera, traditional facial paint and guaraní lineage tattoo on face, ritual talisman, bundle of healing herbs, psychic trance expression, affinity with animals especially yarará viper, distant focused shamanic presence, Shipibo-conibo pantano shaman healer, arrives at Las Tuberías with icaros chants, viewed with suspicion by the Church, intense expression, Subordinación y Valor universe character",
        "negative": "score_6, score_5, score_4, cartoon, anime, illustration, drawing, painting, 3d render, plastic skin, doll-like, airbrushed, beauty filter, blurry, lowres, deformed, mutated, bad anatomy, extra limbs, fused fingers, missing fingers, watermark, text, logo, overexposed, underexposed, smooth, soft focus, duplicate",
        "seed": 91368580,
    },
    {
        "slug": "facundo-rios-tirador",
        "nombre": "Facundo Ríos",
        "positive": "photorealistic, hyperrealistic, RAW photo, ultra detailed skin texture pores and imperfections, realistic eyes with depth catchlights and subtle blood vessels, cinematic dramatic tenebrist chiaroscuro, strong directional side key light, deep shadows and high contrast, gritty atmospheric military realism, sharp focus on face, shallow depth of field, weathered skin details sweat and grime, realistic cloth wear and folds, 8k uhd, masterpiece, best quality, highly detailed, a 28 year old man, lean wiry build, sharp piercing eyes, alert focused, designated marksman tirador, scoped rifle steady measured aim, binoculars around neck, olive drab state-issue military uniform worn, piercing eagle gaze hawk-eye intensity, focused tactical bearing calculating look, counts resistance heads from distance, Fuerzas Armadas confederación urban squad designated marksman, intense expression, Subordinación y Valor universe character",
        "negative": "score_6, score_5, score_4, cartoon, anime, illustration, drawing, painting, 3d render, plastic skin, doll-like, airbrushed, beauty filter, blurry, lowres, deformed, mutated, bad anatomy, extra limbs, fused fingers, missing fingers, watermark, text, logo, overexposed, underexposed, smooth, soft focus, duplicate",
        "seed": 61231855,
    },
]

# Resolutions (vertical portrait, 8GB friendly)
W, H = 512, 832

# Setup A - Lightning fast distilled
LIGHTNING = {
    "name": "lightning",
    "label": "Lightning 4s (sdxl_lightning_4step + euler simple cfg=1)",
    "checkpoint": "sdxl_lightning_4step.safetensors",
    "lora": None,
    "vae": "ponyDiffusionV6XL_vae.safetensors",
    "steps": 4,
    "cfg": 1.0,
    "sampler": "euler",
    "scheduler": "simple",
}

# Setup B - Hyper-SDXL 8step CFG LoRA
HYPER = {
    "name": "hyper",
    "label": "Hyper-SDXL 8s (zavy + Hyper-SDXL-8steps-CFG-lora ddim sgm_uniform cfg=6.5)",
    "checkpoint": "zavyfantasiaxlPDXL_v20.safetensors",
    "lora": "Hyper-SDXL-8steps-CFG-lora.safetensors",
    "vae": "ponyDiffusionV6XL_vae.safetensors",
    "steps": 8,
    "cfg": 6.5,
    "sampler": "ddim",
    "scheduler": "sgm_uniform",
}


def build_workflow(char: dict, setup: dict, prefix: str) -> dict:
    """Build a minimal API workflow for the given setup."""
    nodes: dict[str, Any] = {}
    nid = 1

    # 1. Checkpoint
    nodes[str(nid)] = {
        "class_type": "CheckpointLoaderSimple",
        "inputs": {"ckpt_name": setup["checkpoint"]},
    }
    ckpt_id = str(nid)
    nid += 1

    # optional Lora (ModelOnly for Hyper)
    if setup["lora"]:
        nodes[str(nid)] = {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {
                "model": [ckpt_id, 0],
                "lora_name": setup["lora"],
                "strength_model": 1.0,
            },
        }
        model_id = str(nid)
        nid += 1
    else:
        model_id = ckpt_id

    # Latent
    nodes[str(nid)] = {
        "class_type": "EmptyLatentImage",
        "inputs": {"width": W, "height": H, "batch_size": 1},
    }
    latent_id = str(nid)
    nid += 1

    # Pos
    nodes[str(nid)] = {
        "class_type": "CLIPTextEncode",
        "inputs": {"text": char["positive"], "clip": [ckpt_id, 1]},
    }
    pos_id = str(nid)
    nid += 1

    # Neg
    nodes[str(nid)] = {
        "class_type": "CLIPTextEncode",
        "inputs": {"text": char["negative"], "clip": [ckpt_id, 1]},
    }
    neg_id = str(nid)
    nid += 1

    # VAE Loader (pony for both)
    nodes[str(nid)] = {
        "class_type": "VAELoader",
        "inputs": {"vae_name": setup["vae"]},
    }
    vae_id = str(nid)
    nid += 1

    # KSampler
    nodes[str(nid)] = {
        "class_type": "KSampler",
        "inputs": {
            "seed": char["seed"],
            "steps": setup["steps"],
            "cfg": setup["cfg"],
            "sampler_name": setup["sampler"],
            "scheduler": setup["scheduler"],
            "denoise": 1.0,
            "model": [model_id, 0],
            "positive": [pos_id, 0],
            "negative": [neg_id, 0],
            "latent_image": [latent_id, 0],
        },
    }
    sampler_id = str(nid)
    nid += 1

    # Decode
    nodes[str(nid)] = {
        "class_type": "VAEDecode",
        "inputs": {"samples": [sampler_id, 0], "vae": [vae_id, 0]},
    }
    decode_id = str(nid)
    nid += 1

    # Save
    nodes[str(nid)] = {
        "class_type": "SaveImage",
        "inputs": {
            "filename_prefix": prefix,
            "images": [decode_id, 0],
        },
    }

    return nodes


def queue_and_wait(workflow: dict, timeout: float = TIMEOUT) -> list[str]:
    """POST workflow, poll history, return list of output filenames."""
    resp = requests.post(f"{COMFY}/prompt", json={"prompt": workflow}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    prompt_id = data.get("prompt_id")
    if not prompt_id:
        raise RuntimeError(f"No prompt_id: {data}")

    start = time.time()
    while time.time() - start < timeout:
        time.sleep(POLL)
        h = requests.get(f"{COMFY}/history/{prompt_id}").json()
        if prompt_id in h:
            hist = h[prompt_id]
            if hist.get("status", {}).get("status_str") == "error":
                raise RuntimeError(f"Comfy error: {hist.get('status')}")
            outputs = hist.get("outputs", {})
            files = []
            for node_out in outputs.values():
                if "images" in node_out:
                    for im in node_out["images"]:
                        if im.get("type") == "output":
                            files.append(im["filename"])
            if files:
                return files
    raise TimeoutError(f"Timeout waiting for {prompt_id}")


def main():
    # SSOT: syv-image-generation es el único home de imágenes generadas.
    out_dir = REPO_ROOT / "prompts" / "inbox" / "20260627-hyper-vs-lightning-3x5"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output dir: {out_dir}")

    comfy_out = comfy_output()

    setups = [LIGHTNING, HYPER]
    for c in CHARS:
        for s in setups:
            prefix = f"3x5_{c['slug']}_{s['name']}"
            print(f"\n=== {c['nombre']} / {s['name']} (seed {c['seed']}) ===")
            wf = build_workflow(c, s, prefix)
            try:
                files = queue_and_wait(wf)
                print("  produced:", files)
                for f in files:
                    src = comfy_out / f
                    dst = out_dir / f"{c['slug']}_{s['name']}.png"
                    if src.exists():
                        # take the first (or last) match; simple cp last
                        import shutil
                        shutil.copy2(src, dst)
                        print(f"  saved -> {dst}")
                    else:
                        print(f"  WARN: {src} not found, check output/")
            except Exception as e:
                print(f"  ERROR: {e}")
                # continue with next

    print("\nDone. Now run the grid builder with the 10 pngs in", out_dir)


if __name__ == "__main__":
    main()
