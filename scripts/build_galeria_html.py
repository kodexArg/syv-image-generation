#!/usr/bin/env python3
"""Galería HTML 5×5 (personajes × estilos) — estética kdx Presentation Orange.
Lee results.json, copia imágenes a un assets/ junto al HTML, emite la página."""
import json, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _comfy_root import comfy_output  # noqa: E402

SESSION = HERE.parent / "prompts/inbox/20260629-galeria-estilos"
RESULTS = SESSION / "results.json"
COMFY_OUT = comfy_output()
OUTDIR = Path.home() / "Documents/kdx-report"
ASSETS = OUTDIR / "galeria-syv-assets"
HTML = OUTDIR / "galeria-syv-estilos-20260629.html"

CSS = """
:root{--ink-1000:#0C0B09;--ink-900:#141210;--ink-850:#1a1714;--ink-600:#3a352f;--ink-500:#6b6358;--cream-100:#F3EEE4;--warm-200:#cdbfa8;--orange-500:#ff8c42;--orange-deep:#FF6A1A;--teal-300:#7cc4c8;--font-sans:'Nunito',system-ui,sans-serif;--font-mono:'DM Mono',ui-monospace,monospace;--hairline:1.5px solid var(--ink-600)}
*{box-sizing:border-box}body{margin:0;background:var(--ink-1000);color:var(--cream-100);font-family:var(--font-sans);padding:28px 22px 64px;position:relative}
.po-glow{position:fixed;inset:0;z-index:-1;pointer-events:none;background:radial-gradient(55% 35% at 82% 8%,rgba(255,106,26,.16),rgba(255,106,26,.04) 40%,transparent 72%)}
.kicker{font-family:var(--font-mono);font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--orange-500);margin:0 0 10px}
h1{font-weight:800;letter-spacing:-.02em;text-transform:lowercase;font-size:clamp(2rem,6vw,3rem);margin:0 0 6px}
.sub{color:var(--warm-200);max-width:70ch;margin:0 0 26px}
.grid{display:grid;grid-template-columns:150px repeat(5,1fr);gap:10px;min-width:1180px}
.colhead{font-family:var(--font-mono);font-size:.7rem;letter-spacing:.04em;text-transform:uppercase;color:var(--teal-300);align-self:end;padding-bottom:6px;border-bottom:var(--hairline)}
.rowlabel{display:flex;align-items:center;font-weight:800;font-size:.95rem;color:var(--cream-100);padding-right:8px;border-right:2px solid var(--orange-deep);line-height:1.15}
figure{margin:0;background:var(--ink-850);border:var(--hairline);border-radius:14px;overflow:hidden;display:flex;flex-direction:column}
figure img{width:100%;aspect-ratio:704/960;object-fit:cover;display:block}
figcaption{font-family:var(--font-mono);font-size:.62rem;color:var(--ink-500);padding:5px 7px;text-align:center}
figure.miss{align-items:center;justify-content:center;color:var(--ink-500);min-height:150px;font-family:var(--font-mono);font-size:.7rem}
footer{margin-top:24px;color:var(--ink-500);font-family:var(--font-mono);font-size:.7rem;line-height:1.7;border-top:var(--hairline);padding-top:14px}
.wrap{overflow-x:auto}
"""


def main():
    data = json.loads(RESULTS.read_text())
    chars, styles = data["chars"], data["styles"]
    idx = {(r["char"], r["style"]): r for r in data["results"]}
    ASSETS.mkdir(parents=True, exist_ok=True)

    for r in data["results"]:
        if r.get("filename"):
            src = COMFY_OUT / r.get("subfolder", "") / r["filename"]
            if src.exists():
                shutil.copy2(src, ASSETS / r["filename"])

    head = '<div class="colhead"></div>' + "".join(
        f'<div class="colhead">{s["label"]}</div>' for s in styles)
    rows = ['<div class="grid">' + head]
    for c in chars:
        cells = [f'<div class="rowlabel">{c["name"]}</div>']
        for s in styles:
            r = idx.get((c["key"], s["key"]))
            if r and r.get("filename"):
                cells.append(
                    f'<figure><img loading="lazy" src="galeria-syv-assets/{r["filename"]}" '
                    f'alt="{c["name"]} {s["label"]}"><figcaption>seed {r.get("seed","")}</figcaption></figure>')
            else:
                cells.append('<figure class="miss"><div>—</div></figure>')
        rows.append("".join(cells))
    rows.append("</div>")

    ok = sum(1 for r in data["results"] if r.get("filename"))
    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>galería · estilos SyV</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;800&family=DM+Mono:wght@400&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="po-glow"></div>
<p class="kicker">galería · estilos</p>
<h1>5 personajes · 5 estilos</h1>
<p class="sub">Subordinación y Valor — realismo gráfico entre cartoon y foto (serigrafía · noir Sin City · risograph · gouache), paletas limitadas SyV y kdx. {ok}/25 generadas.</p>
<div class="wrap">{''.join(rows)}</div>
<footer>Z-Image Turbo (GGUF Q8) · res_multistep/simple · 8 steps · cfg 1.4-1.6 · shift 3 · 704×960 · sin texto · paletas: olive #7B8A4E · celeste #8FB8D6 · crema #F3EEE4 · negro #0C0B09 · naranja kdx #FF6A1A</footer>
</body></html>"""
    HTML.write_text(html)
    print(f"OK {ok}/25 -> {HTML}")


if __name__ == "__main__":
    main()
