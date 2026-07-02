---
title: Severo · ficha ComfyUI (v7)
folder: prompts/characters
slug: severo-tratante-de-almas
source: syv-pj/resources/personajes/severo-tratante-de-almas.md
description: Compilación determinista de Severo para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Severo · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/severo-tratante-de-almas.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | +1.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | +0.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | +0.0 | `cuerpo - 3`, clamp -2..+3.0 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
World of Subordinación y Valor: cold rain-grey overcast light, low-tech analog Catholic-military theocracy, worn concrete; muted olive-drab, pale celeste and cream palette. medium shot in a worn dystopian setting, perpetual rain, neutral eye-level framing.

**② prompt-character** (middle, variable — the subject):
a 49-year-old man, gaunt, lean, gaunt, hollow-cheeked, criollo (mixed Spanish-American), alert attentive eyes, sharp focus, warm magnetic presence, engaged gaze, a worn leather jacket, a worn leather notebook, natural overcast light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
quiet dystopian resignation, analog low-tech world, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | traficantes_de_almas |
| rango | tratante |
| especialidad | especialidad-oficio-tratante |
| edad | 49 |
| genero | m |
| atributos | cuerpo 3 / mente 4 / alma 4 |
