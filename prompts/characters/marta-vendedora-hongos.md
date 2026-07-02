---
title: Marta · ficha ComfyUI (v7)
folder: prompts/characters
slug: marta-vendedora-hongos
source: syv-pj/resources/personajes/marta-vendedora-hongos.md
description: Compilación determinista de Marta para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Marta · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/marta-vendedora-hongos.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | +1.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | +0.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | +0.0 | `cuerpo - 3`, clamp -2..+1.5 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
cold rain-grey overcast light, worn concrete and damp plaster walls, analog low-tech dystopia, muted olive-drab, pale celeste and cream palette. half-body portrait, plain worn concrete wall background, soft overcast studio light, neutral eye-level framing, shallow depth of field.

**② prompt-character** (middle, variable — the subject):
a photo of a 45-year-old woman, beautiful, warrior's bearing, fixed grey eyes, clearly female face and body, a wicker basket of foraged mushrooms, a patched darned shawl, natural overcast light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
quiet dystopian resignation, analog low-tech world, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | independiente |
| rango | sanadora_independiente |
| especialidad | especialidad-paranormal-sanador |
| edad | 45 |
| genero | f |
| atributos | cuerpo 3 / mente 3 / alma 3 |
