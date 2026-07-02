#!/usr/bin/env python3
"""Detección dinámica del root de ComfyUI — nunca hardcodear /home/kodex/ComfyUI.

Delega en find_comfy.py del skill `comfyui` (syv-harness). Fallback liviano
a ~/.config/comfyui/last_root / ~/ComfyUI si el skill no está disponible.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
FINDER = REPO_ROOT.parent / "syv-harness" / "skills" / "comfyui" / "scripts" / "find_comfy.py"


def comfy_root() -> Path:
    if env := os.environ.get("COMFYUI_PATH") or os.environ.get("COMFYUI_ROOT"):
        p = Path(env).expanduser()
        if p.is_dir():
            return p

    if FINDER.is_file():
        out = subprocess.run(
            ["python3", str(FINDER), "--quiet"], capture_output=True, text=True, check=False
        )
        root = out.stdout.strip()
        if root and Path(root).is_dir():
            return Path(root)

    last_root = Path.home() / ".config" / "comfyui" / "last_root"
    if last_root.is_file():
        p = Path(last_root.read_text().strip()).expanduser()
        if p.is_dir():
            return p

    fallback = Path.home() / "ComfyUI"
    if fallback.is_dir():
        return fallback

    raise RuntimeError(
        "No pude detectar el root de ComfyUI. Definí $COMFYUI_PATH o corré "
        "el skill comfyui (comfyctl find)."
    )


def comfy_output() -> Path:
    return comfy_root() / "output"
