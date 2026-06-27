#!/usr/bin/env python3
"""
Generate a self-contained dark comparison HTML page for the squad test.

Shows all characters (same seed) across the 4 model combinations.
Uses SyV design tokens: deep ink bg, cream text, olive green accents, celeste highlights.
Cards with name/role, short desc, 4 images (one per model), prompt excerpt.

Run after export or point to images/raw filenames.
Output: docs/comparisons/20260627-squad-realistic-comparison.html (or build/)
"""

from __future__ import annotations

import json
from pathlib import Path
from html import escape

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD = REPO_ROOT / "build"
DOCS = REPO_ROOT / "docs"
OUT_DIR = DOCS / "comparisons"
OUT_DIR.mkdir(parents=True, exist_ok=True)

JOBS_JSON = BUILD / "squad_test_jobs.json"
PROPOSAL = DOCS / "tests" / "20260627-gran-escuadra-realista.md"

# Model display order and short labels
MODEL_ORDER = [
    ("ponyDiffusionV6XL_v6StartWithThisOne.safetensors", "Pony v6", "pony"),
    ("zavyfantasiaxlPDXL_v20.safetensors", "Zavy Fantasia", "zavy"),
    ("sdxl_lightning_4step.safetensors", "Lightning 4s", "light4"),
    ("sdxl_lightning_8step.safetensors", "Lightning 8s", "light8"),
]

def load_jobs():
    data = json.loads(JOBS_JSON.read_text(encoding="utf-8"))
    # group by slug
    by_slug = {}
    for j in data:
        by_slug.setdefault(j["slug"], []).append(j)
    return by_slug

def filename_for(job):
    # The SaveImage produces syv_real_<slug>_<modelshort>_00001_.png
    # We use the prefix from job
    prefix = job.get("filename_prefix", f"syv_real_{job['slug']}")
    return f"{prefix}_00001_.png"

def build_html(by_slug: dict) -> str:
    css = """
:root {
  --ink: #0C0B09;
  --ink2: #141210;
  --cream: #F3EEE4;
  --green: #7B8A4E;
  --green-light: #97A267;
  --celeste: #8FB8D6;
  --muted: #6B6358;
}
* { box-sizing: border-box; }
body { margin:0; background: var(--ink); color: var(--cream); font-family: system-ui, -apple-system, sans-serif; line-height:1.4; }
header { background: #111; padding: 1.5rem 2rem; border-bottom: 2px solid var(--green); }
h1 { margin:0 0 .25rem; font-size: 1.8rem; color: var(--cream); }
.subtitle { color: var(--muted); font-size: .95rem; }
main { max-width: 1400px; margin: 0 auto; padding: 1.5rem; }
.card { background: var(--ink2); border: 1px solid var(--green); margin-bottom: 1.25rem; border-radius: 6px; overflow: hidden; }
.card-header { padding: .6rem .9rem; background: #1a1814; display:flex; justify-content:space-between; align-items:center; gap:.5rem; }
.card-header .name { font-weight:600; font-size:1.05rem; }
.card-header .meta { font-size:.8rem; color:var(--muted); }
.grid { display:grid; grid-template-columns: repeat(4, 1fr); gap: 6px; padding: .6rem .9rem; }
.col { text-align:center; }
.col img { width:100%; height:auto; border:1px solid #333; background:#111; display:block; }
.col .model { font-size:.7rem; color:var(--celeste); margin-top:.25rem; font-family:monospace; }
.prompt { font-size:.72rem; background:#111; padding:.5rem .75rem; margin:.5rem .9rem; border-left:3px solid var(--green); color:#c8c2b4; white-space:pre-wrap; max-height: 7.5em; overflow:auto; }
footer { padding: 1rem 2rem; font-size:.75rem; color:var(--muted); border-top:1px solid #222; }
.badge { display:inline-block; padding:1px 6px; background:var(--green); color:#0C0B09; font-size:.65rem; border-radius:3px; }
"""

    html_parts = [
        "<!doctype html>",
        "<html lang='es'>",
        "<head><meta charset='utf-8'><title>SyV — Escuadra Realista (Comparación de Modelos)</title>",
        f"<style>{css}</style>",
        "</head><body>",
        "<header>",
        "<h1>Gran Escuadra Realista — Comparación de Modelos</h1>",
        "<div class='subtitle'>Mismo seed por personaje • Estilo realista + artístico (canon syv-docs) • 2026-06-27</div>",
        "<div style='margin-top:.5rem'>Modelos: <span class='badge'>Pony</span> <span class='badge'>Zavy Fantasia</span> <span class='badge'>SDXL Lightning 4/8</span></div>",
        "</header>",
        "<main>",
    ]

    # Sort slugs roughly: conf squad first then others
    slugs = sorted(by_slug.keys())

    for slug in slugs:
        jobs = by_slug[slug]
        j0 = jobs[0]
        nombre = escape(j0.get("nombre", slug))
        army = j0.get("army", "")
        army_badge = "CONF" if army == "confederacion" else ("ROJO" if army == "ejercito_rojo" else army.upper())
        seed = j0.get("seed")

        html_parts.append("<div class='card'>")
        html_parts.append(f"<div class='card-header'><span class='name'>{nombre}</span> <span class='meta'><span class='badge'>{army_badge}</span> seed={seed} • {j0['width']}×{j0['height']}</span></div>")

        # Images grid
        html_parts.append("<div class='grid'>")
        # map model -> job
        model_map = {j["model"]: j for j in jobs}
        for model_full, label, short in MODEL_ORDER:
            j = model_map.get(model_full)
            if not j:
                html_parts.append("<div class='col'><em>—</em></div>")
                continue
            fname = filename_for(j)
            # Assume after export the files live in ../images/raw/ relative to docs/comparisons/
            src = f"../../images/raw/{fname}"
            html_parts.append("<div class='col'>")
            html_parts.append(f"<img src='{src}' alt='{escape(nombre)} - {label}' loading='lazy'>")
            html_parts.append(f"<div class='model'>{label}</div>")
            html_parts.append("</div>")
        html_parts.append("</div>")

        # Prompt excerpt
        pos = j0.get("positive", "")[:420]
        html_parts.append(f"<div class='prompt'>{escape(pos)}...</div>")

        html_parts.append("</div>")

    html_parts.append("</main>")
    html_parts.append("<footer>Generado desde <code>scripts/generate_comparison_page.py</code>. Imágenes en <code>images/raw/</code> (exportar con <code>scripts/export.py</code>). Ver propuesta completa en <code>docs/tests/20260627-gran-escuadra-realista.md</code>.</footer>")
    html_parts.append("</body></html>")
    return "\n".join(html_parts)

def main():
    by_slug = load_jobs()
    html = build_html(by_slug)
    out = OUT_DIR / "20260627-squad-realistic-comparison.html"
    out.write_text(html, encoding="utf-8")
    print(f"Comparison page written: {out}")
    print(f"  {len(by_slug)} characters × 4 models")

if __name__ == "__main__":
    main()