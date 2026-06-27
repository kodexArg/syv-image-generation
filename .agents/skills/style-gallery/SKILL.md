---
name: style-gallery
description: >
  Use when comparing image-generation styles in ComfyUI: "dame N opciones de
  estilo", "mostrame estilos en el navegador", "quiero ver estilos lado a lado",
  "comparar estilos de retrato", style-exploration galleries for ComfyUI.
  Produces a dark side-by-side HTML gallery with numbered cards, labels,
  descriptions, full prompts, and a shared negative + sampler footer.
triggers:
  - comparar estilos
  - opciones de estilo
  - style gallery
  - mostrame estilos
  - dame N opciones
  - style options
  - explorar estilos
---

# Skill: style-gallery

Genera una galería de comparación de estilos ComfyUI: N retratos verticales
lado a lado en el navegador, cada uno con número, etiqueta, descripción y el
prompt exacto. Footer con negativo compartido y parámetros del sampler.

## Flujo

### 1. Definir la spec JSON

Armá un archivo JSON con esta forma (o dictalo in-line y escribilo a `/tmp/style_spec.json`):

```json
{
  "title": "SyV · estilos de prueba",
  "subject": ", descripción detallada del sujeto, pose, encuadre",
  "pony_prefix": "score_9, score_8_up, score_7_up, rating_safe, solo, one person, ",
  "negative": "score_6, score_5, score_4, photorealistic, ...",
  "seed": 7777,
  "steps": 30,
  "cfg": 7.0,
  "sampler": "dpmpp_2m",
  "scheduler": "karras",
  "checkpoint": "zavyfantasiaxlPDXL_v20.safetensors",
  "width": 832,
  "height": 1344,
  "output_dir": "/home/kodex/Dev/SyV/syv-image-prompts/build/style_<slug>",
  "options": [
    {
      "label": "Nombre visible",
      "desc": "Descripción corta en HTML (puede usar &amp; &middot; etc.)",
      "style_clause": "(oil painting:1.3), visible brushstrokes, ..."
    }
  ]
}
```

Campos opcionales con defaults:
- `pony_prefix` → `"score_9, score_8_up, score_7_up, rating_safe, solo, one person, "`
- `seed` → 7777 · `steps` → 30 · `cfg` → 7.0
- `sampler` → dpmpp_2m · `scheduler` → karras
- `checkpoint` → zavyfantasiaxlPDXL_v20.safetensors
- `width`/`height` → 832/1344 (Fibonacci 13:21, vertical)

### 2. Ejecutar el generador

```bash
python3 /home/kodex/Dev/SyV/syv-image-prompts/.agents/skills/style-gallery/scripts/build_gallery.py \
    /ruta/al/spec.json
```

El script:
- Encola cada opción en ComfyUI (`POST /prompt`), espera el resultado, copia la imagen.
- Ensambla el `index.html` en `output_dir/`.
- Imprime la ruta absoluta y la URL `file://` al finalizar.

Dry-run (sin GPU, imágenes placeholder de color sólido):
```bash
python3 .../build_gallery.py /ruta/al/spec.json --dry-run
```

### 3. Abrir en el navegador

**NO** lanzar Chromium por shell. Usar la MCP `chrome-devtools`:

```
mcp__chrome-devtools__navigate  url="file:///ruta/absoluta/index.html"
```

La URL `file://` la imprime el script en la última línea `[gallery] ...`.

## Ejemplo rápido

```bash
python3 /home/kodex/Dev/SyV/syv-image-prompts/.agents/skills/style-gallery/scripts/build_gallery.py \
    /home/kodex/Dev/SyV/syv-image-prompts/.agents/skills/style-gallery/scripts/example_spec.json \
    --dry-run
```

Luego navegar con chrome-devtools a la URL impresa.

## Notas

- ComfyUI debe estar corriendo en `http://127.0.0.1:8188`.
- Las imágenes generadas van a `output_dir/` (numeradas `1.png`, `2.png`, …).
- El `output_dir` se crea automáticamente.
- El prompt completo de cada imagen = `pony_prefix + style_clause + subject`.
