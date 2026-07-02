#!/usr/bin/env python3
"""Arma la matriz 5x5 HTML del panorama Z-Image Turbo desde results.json.
Copia las imágenes a la carpeta de sesión (images/) y emite index.html autocontenido."""
import json, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _comfy_root import comfy_output  # noqa: E402

SESSION = HERE.parent / "prompts/inbox/20260628-z-image-turbo-panorama"
RESULTS = SESSION / "results.json"
COMFY_OUT = comfy_output()
IMGDIR = SESSION / "images"

SLUG_ORDER = ["luisa-pescadora", "baltasar-quevedo-inquisidor", "anibal-painemal-comandante",
              "iracema-chaman-pantano", "yara-sacerdotisa-orixa"]
NAMES = {"luisa-pescadora": "Luisa · Pescadora (F40)",
         "baltasar-quevedo-inquisidor": "Baltasar · Inquisidor (M28)",
         "anibal-painemal-comandante": "Aníbal · Comandante (M58)",
         "iracema-chaman-pantano": "Iracema · Chamán (F47)",
         "yara-sacerdotisa-orixa": "Yara · Sacerdotisa (F58)"}
VARIANTS = {1: "close-up / ventana", 2: "medio / entorno", 3: "3-4 / golden hour",
            4: "flash / noche-lluvia", 5: "ambiental / amplio"}


def main():
    data = json.loads(RESULTS.read_text())
    recipe = data["recipe"]
    res = data["results"]
    IMGDIR.mkdir(exist_ok=True)
    idx = {(r["slug"], r["variant"]): r for r in res}

    # copiar imágenes
    for r in res:
        if r.get("filename"):
            src = COMFY_OUT / r.get("subfolder", "") / r["filename"]
            if src.exists():
                shutil.copy2(src, IMGDIR / r["filename"])

    cells = []
    for slug in SLUG_ORDER:
        row = [f'<div class="rowlabel">{NAMES.get(slug, slug)}</div>']
        for v in range(1, 6):
            r = idx.get((slug, v))
            if r and r.get("filename"):
                row.append(
                    f'<figure><img src="images/{r["filename"]}" loading="lazy" alt="{slug} v{v}">'
                    f'<figcaption>{VARIANTS[v]}<br><span class="seed">seed {r.get("seed","")}</span></figcaption></figure>')
            else:
                row.append('<figure class="miss"><div>—</div><figcaption>falló</figcaption></figure>')
        cells.append('<div class="row">' + "".join(row) + '</div>')

    ok = sum(1 for r in res if r.get("filename"))
    header_cols = '<div class="row head"><div class="rowlabel"></div>' + \
        "".join(f'<div class="colhead">V{v} · {VARIANTS[v]}</div>' for v in range(1, 6)) + '</div>'

    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SyV · Z-Image Turbo · Panorama 5×5</title>
<style>
:root{{--bg:#0C0B09;--fg:#F3EEE4;--olive:#7B8A4E;--cyan:#8FB8D6;--card:#16140f;}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.4 system-ui,sans-serif;padding:24px}}
h1{{font-size:20px;margin:0 0 2px;letter-spacing:.5px}}
.sub{{color:var(--cyan);font-size:12px;margin-bottom:18px}}
.sub b{{color:var(--olive)}}
.grid{{display:flex;flex-direction:column;gap:10px;min-width:1100px}}
.row{{display:grid;grid-template-columns:170px repeat(5,1fr);gap:10px;align-items:stretch}}
.row.head .colhead{{color:var(--cyan);font-size:11px;text-transform:uppercase;letter-spacing:.5px;align-self:end;padding-bottom:4px;border-bottom:1px solid #2a2720}}
.rowlabel{{display:flex;align-items:center;font-weight:600;color:var(--fg);font-size:13px;padding-right:6px;border-right:2px solid var(--olive)}}
figure{{margin:0;background:var(--card);border:1px solid #221f18;border-radius:8px;overflow:hidden;display:flex;flex-direction:column}}
figure img{{width:100%;aspect-ratio:832/1248;object-fit:cover;display:block}}
figcaption{{font-size:10.5px;color:#b9b3a3;padding:5px 7px;text-align:center}}
.seed{{color:#6f6a5c}}
figure.miss{{align-items:center;justify-content:center;color:#5a554a;min-height:180px}}
footer{{margin-top:20px;color:#6f6a5c;font-size:11px;font-family:ui-monospace,monospace}}
</style></head><body>
<h1>Subordinación y Valor — Panorama Z-Image Turbo</h1>
<div class="sub">5 personajes × 5 variantes · <b>{ok}/25</b> generadas · imágenes naturales/documentales</div>
<div class="grid">{header_cols}{''.join(cells)}</div>
<footer>UNet zimageTurboByStable_2602Q8.gguf (Q8) · CLIP qwen_3_4b (lumina2) · VAE ae ·
{recipe['sampler']}/{recipe['scheduler']} · {recipe['steps']} steps · cfg {recipe['cfg']} · shift 3 · {recipe['width']}×{recipe['height']} · RTX 2060 SUPER 8GB</footer>
</body></html>"""

    out = SESSION / "index.html"
    out.write_text(html)
    print(f"OK {ok}/25 -> {out}")


if __name__ == "__main__":
    main()
