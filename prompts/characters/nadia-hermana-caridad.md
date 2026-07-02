---
title: Hermana Nadia · ficha ComfyUI (v7)
folder: prompts/characters
slug: nadia-hermana-caridad
source: syv-pj/resources/personajes/nadia-hermana-caridad.md
description: Compilación determinista de Hermana Nadia para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Hermana Nadia · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/nadia-hermana-caridad.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | -2.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | -1.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | -1.0 | `cuerpo - 3`, clamp -2..+1.5 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
cold rain-grey overcast light, worn concrete and damp plaster walls, analog low-tech dystopia, muted olive-drab, pale celeste and cream palette. half-body portrait, plain worn concrete wall background, soft overcast studio light, neutral eye-level framing, shallow depth of field.

**② prompt-character** (middle, variable — the subject):
a photo of a 19-year-old woman, young and rough-hewn, weathered calloused hands, a simple braid, wiry spare build, overwhelming magnetic aura, luminous commanding gaze, clearly female face and body, a monastic habit, a medical kit, haloed by dramatic rim light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
state propaganda order, olive-drab and celeste discipline, brass insignia, dignified martial bearing, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | iglesia |
| rango | novicio |
| especialidad | especialidad-oficio-asistente |
| edad | 19 |
| genero | f |
| atributos | cuerpo 2 / mente 3 / alma 7 |
