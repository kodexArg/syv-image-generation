---
title: Walter · ficha ComfyUI (v7)
folder: prompts/characters
slug: walter-puntero-tuberias
source: syv-pj/resources/personajes/walter-puntero-tuberias.md
description: Compilación determinista de Walter para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Walter · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/walter-puntero-tuberias.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | -1.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | +0.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | +0.0 | `cuerpo - 3`, clamp -2..+3.0 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
cold rain-grey overcast light, worn concrete and damp plaster walls, analog low-tech dystopia, muted olive-drab, pale celeste and cream palette. half-body portrait, plain worn concrete wall background, soft overcast studio light, neutral eye-level framing, shallow depth of field.

**② prompt-character** (middle, variable — the subject):
a photo of a 22-year-old man, wiry sinewy build, pale skin, undercut, shaved sides, alert attentive eyes, sharp focus, warm magnetic presence, engaged gaze, clearly male face and body, a worn leather jacket, natural overcast light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
insurgent red-army fervor, patched red cloth, improvised gear, defiant underground resolve, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | punteros |
| rango | puntero |
| especialidad | especialidad-combate-lider |
| edad | 22 |
| genero | m |
| atributos | cuerpo 3 / mente 4 / alma 4 |
