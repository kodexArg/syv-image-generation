# Prueba — Retrato pixel-art de oficial (teocracia militar)

- **Fecha:** 2026-06-25
- **Slug:** 20260625-pixel-art-oficial
- **Objetivo:** retrato pixel-art estilo RPG 16-bit de un oficial de la
  teocracia militar, fijando la paleta SyV (olive drab / celeste / crema /
  negro cálido) y un pipeline de pixelado (downscale a 64 → upscale a 512).
- **Estado:** prueba inicial migrada desde la raíz de `~/Dev/SyV/` al crear
  este repo. Sin imagen seleccionada todavía (regenerar y exportar).

## Parámetros

| Campo | Valor |
|---|---|
| Workflow | `workflows/syv_pixel_art_portrait.json` (UI) · `..._api.json` (API) |
| Checkpoint | `zavyfantasiaxlPDXL_v20.safetensors` |
| Resolución | `1024x1024` → downscale nearest-exact 64x64 → upscale 512x512 |
| Sampler | `dpmpp_2m` |
| Scheduler | `karras` |
| Steps | `28` |
| CFG | `7.0` |
| Seed | `977125715` |
| Save prefix | `syv_pixel_art_portrait` |

## Prompt

**Positivo:**

```
score_9, score_8_up, score_7_up, pixel art, retro 16-bit RPG character portrait, close-up face of a stern 27-year-old male officer of the military theocracy. He has a rugged face, short grey stubble, cold eyes, wearing an olive-drab military cap and the high collar of an olive-drab uniform. Under perpetual cold rain, dark atmospheric lighting. Color palette: matte military olive drab green (#7B8A4E), celeste blue accents (#8FB8D6), cream white (#F3EEE4), deep warm-black backdrop (#0C0B09). Classic gaming pixel sprite art, clean visible square pixel grid, dithered shading, nostalgic aesthetic, 64x64 style.
```

**Negativo:**

```
score_6, score_5, score_4, worst quality, low quality, photo, photorealistic, 3d render, smooth, blurry, noisy, gradient backgrounds, signature, logo, watermark, border, frame
```

## Pipeline (nodos)

`CheckpointLoaderSimple` → `CLIPTextEncode` (pos/neg) + `EmptyLatentImage`
(1024²) → `KSampler` → `VAEDecode` → `ImageScale` nearest-exact a **64x64**
(pixelado real) → `ImageScale` nearest-exact a **512x512** (visualización con
grid visible) → `SaveImage` (`syv_pixel_art_portrait`).

## Conclusiones

- El doble `ImageScale` nearest-exact (downscale fuerte + upscale) es lo que da
  el grid de píxeles visible sin antialias. Buen punto de partida.
- Pendiente: regenerar, exportar con `uv run scripts/export.py --prefix
  syv_pixel_art_portrait`, elegir la mejor → `images/seleccionadas/` y enlazar
  acá.
- A probar después: variar seed, bajar pasos, y validar la paleta contra
  `syv-design-system/` / canon de `syv-docs/`.
