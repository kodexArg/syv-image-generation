---
title: Iracema · ficha ComfyUI (v7)
folder: prompts/characters
slug: iracema-chaman-pantano
source: syv-pj/resources/personajes/iracema-chaman-pantano.md
description: Compilación determinista de Iracema para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Iracema · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/iracema-chaman-pantano.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | +1.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | +0.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | +0.0 | `cuerpo - 3`, clamp -2..+1.5 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
World of Subordinación y Valor: cold rain-grey overcast light, low-tech analog Catholic-military theocracy, worn concrete; muted olive-drab, pale celeste and cream palette. medium shot among misty swamp reeds, dim ritual light, slow contemplative framing.

**② prompt-character** (middle, variable — the subject):
a 47-year-old woman, Shipibo-Conibo features, copper-toned skin, long black hair, overwhelming magnetic aura, luminous commanding gaze, a bundle of dried herbs, ritual face paint, a Guaraní talisman, haloed by dramatic rim light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
syncretic ritual mysticism, swamp mist, old-world reverence, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | shipibo_conibo |
| rango | meraya |
| especialidad | especialidad-paranormal-curandero |
| edad | 47 |
| genero | f |
| atributos | cuerpo 3 / mente 3 / alma 7 |
