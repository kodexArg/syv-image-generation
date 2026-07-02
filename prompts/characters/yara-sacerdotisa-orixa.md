---
title: Yara · ficha ComfyUI (v7)
folder: prompts/characters
slug: yara-sacerdotisa-orixa
source: syv-pj/resources/personajes/yara-sacerdotisa-orixa.md
description: Compilación determinista de Yara para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Yara · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/yara-sacerdotisa-orixa.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | +2.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | -1.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | -1.0 | `cuerpo - 3`, clamp -2..+1.5 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
World of Subordinación y Valor: cold rain-grey overcast light, low-tech analog Catholic-military theocracy, worn concrete; muted olive-drab, pale celeste and cream palette. medium shot in a damp candle-lit stone hall, low three-quarter angle, oppressive gloom.

**② prompt-character** (middle, variable — the subject):
a 58-year-old woman, Afro-descendant, braided grey hair, dark skin, wiry spare build, alert attentive eyes, sharp focus, overwhelming magnetic aura, luminous commanding gaze, a syncretic devotional medal, agogo, a feathered headdress, haloed by dramatic rim light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
theocratic solemnity, incense and candlelight, sacred authority, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | los_umbanda |
| rango | pai_de_santo |
| especialidad | especialidad-paranormal-medium |
| edad | 58 |
| genero | f |
| atributos | cuerpo 2 / mente 4 / alma 7 |
