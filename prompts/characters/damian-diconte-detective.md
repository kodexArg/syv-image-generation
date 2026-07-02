---
title: Damián DiConte · ficha ComfyUI (v7)
folder: prompts/characters
slug: damian-diconte-detective
source: syv-pj/resources/personajes/damian-diconte-detective.md
description: Compilación determinista de Damián DiConte para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Damián DiConte · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/damian-diconte-detective.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | +2.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | +0.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | +0.0 | `cuerpo - 3`, clamp -2..+3.0 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
cold rain-grey overcast light, worn concrete and damp plaster walls, analog low-tech dystopia, muted olive-drab, pale celeste and cream palette. half-body portrait, plain worn concrete wall background, soft overcast studio light, neutral eye-level framing, shallow depth of field.

**② prompt-character** (middle, variable — the subject):
a photo of a 58-year-old man, very tall, obese, sagging gaunt face, piercing intelligent gaze, penetrating analytical stare, clearly male face and body, a worn leather jacket, a battered leather hat, natural overcast light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
quiet dystopian resignation, analog low-tech world, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | independiente |
| rango | detective_privado |
| especialidad | null |
| edad | 58 |
| genero | m |
| atributos | cuerpo 3 / mente 7 / alma 3 |
