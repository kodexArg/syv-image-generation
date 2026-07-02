---
title: Valentina Roca · ficha ComfyUI (v7)
folder: prompts/characters
slug: valentina-roca-camarada
source: syv-pj/resources/personajes/valentina-roca-camarada.md
description: Compilación determinista de Valentina Roca para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Valentina Roca · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/valentina-roca-camarada.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | +0.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | +0.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | +0.0 | `cuerpo - 3`, clamp -2..+1.5 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
World of Subordinación y Valor: cold rain-grey overcast light, low-tech analog Catholic-military theocracy, worn concrete; muted olive-drab, pale celeste and cream palette. medium shot in a cramped underground hideout, bare bulb light, tense close framing.

**② prompt-character** (middle, variable — the subject):
a 34-year-old woman, criolla (mixed Spanish-American), dark hair tied back, alert attentive eyes, sharp focus, overwhelming magnetic aura, luminous commanding gaze, a field radio clipped to the shoulder, a battered leather hat, haloed by dramatic rim light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
insurgent red-army fervor, patched red cloth, improvised gear, defiant underground resolve, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | resistencia_subterranea |
| rango | cabecilla |
| especialidad | especialidad-investigacion-espia |
| edad | 34 |
| genero | f |
| atributos | cuerpo 3 / mente 4 / alma 6 |
