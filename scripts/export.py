#!/usr/bin/env python3
"""Importa los PNG más recientes de ComfyUI/output a este repo (images/raw/).

ComfyUI escribe las imágenes en su propio output dir. Este script las copia
a `images/raw/` para versionar/documentar la prueba sin tocar el origen.

Uso:
    uv run scripts/export.py                 # últimos 5 PNG
    uv run scripts/export.py -n 20           # últimos 20
    uv run scripts/export.py --prefix syv_pixel_art_portrait
    uv run scripts/export.py --since 30      # PNG de los últimos 30 minutos
    uv run scripts/export.py --move          # mover en vez de copiar

Detecta el output de ComfyUI sin hardcodear:
  1. $COMFYUI_OUTPUT
  2. $COMFYUI_PATH/$COMFYUI_DIR/$COMFYUI_ROOT + /output
  3. ~/.config/comfyui/last_root (lo deja el skill comfyui) + /output
  4. ubicaciones conocidas (~/ComfyUI/output, etc.)
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "images" / "raw"

KNOWN_ROOTS = [
    Path.home() / "ComfyUI",
    Path.home() / "comfyui",
    Path.home() / ".local" / "share" / "ComfyUI",
    Path("/opt/ComfyUI"),
]


def find_output_dir() -> Path:
    if env := os.environ.get("COMFYUI_OUTPUT"):
        p = Path(env).expanduser()
        if p.is_dir():
            return p

    for var in ("COMFYUI_PATH", "COMFYUI_DIR", "COMFYUI_ROOT"):
        if env := os.environ.get(var):
            p = Path(env).expanduser() / "output"
            if p.is_dir():
                return p

    last_root = Path.home() / ".config" / "comfyui" / "last_root"
    if last_root.is_file():
        p = Path(last_root.read_text().strip()).expanduser() / "output"
        if p.is_dir():
            return p

    for root in KNOWN_ROOTS:
        p = root / "output"
        if p.is_dir():
            return p

    sys.exit(
        "✗ No encontré el output de ComfyUI. Definí $COMFYUI_OUTPUT o "
        "$COMFYUI_PATH, o corré el skill comfyui (deja ~/.config/comfyui/last_root)."
    )


def collect(out_dir: Path, *, prefix: str | None, since_min: float | None) -> list[Path]:
    pngs = [p for p in out_dir.rglob("*.png") if p.is_file()]
    if prefix:
        pngs = [p for p in pngs if p.name.startswith(prefix)]
    if since_min is not None:
        cutoff = time.time() - since_min * 60
        pngs = [p for p in pngs if p.stat().st_mtime >= cutoff]
    pngs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return pngs


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-n", "--count", type=int, default=5, help="cuántos PNG (default 5)")
    ap.add_argument("--prefix", help="filtrar por prefijo de filename (filename_prefix del SaveImage)")
    ap.add_argument("--since", type=float, metavar="MIN", help="solo PNG de los últimos MIN minutos")
    ap.add_argument("--move", action="store_true", help="mover en vez de copiar")
    args = ap.parse_args()

    out_dir = find_output_dir()
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    pngs = collect(out_dir, prefix=args.prefix, since_min=args.since)
    if not pngs:
        print(f"(sin PNG que coincidan en {out_dir})")
        return
    if args.since is None:
        pngs = pngs[: args.count]

    verb = shutil.move if args.move else shutil.copy2
    action = "movido" if args.move else "copiado"
    print(f"output ComfyUI: {out_dir}")
    for src in pngs:
        dst = RAW_DIR / src.name
        if dst.exists() and not args.move:
            dst = RAW_DIR / f"{src.stem}.dup{int(src.stat().st_mtime)}{src.suffix}"
        verb(str(src), str(dst))
        print(f"  {action}: {src.name} → images/raw/{dst.name}")
    print(f"\n✓ {len(pngs)} archivo(s) en images/raw/")


if __name__ == "__main__":
    main()
