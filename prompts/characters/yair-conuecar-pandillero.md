---
title: Yair Coñuecar · ficha ComfyUI (v7)
folder: prompts/characters
slug: yair-conuecar-pandillero
source: syv-pj/resources/personajes/yair-conuecar-pandillero.md
description: Compilación determinista de Yair Coñuecar para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Yair Coñuecar · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/yair-conuecar-pandillero.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | -1.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | +0.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | +0.0 | `cuerpo - 3`, clamp -2..+3.0 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
World of Subordinación y Valor: cold rain-grey overcast light, low-tech analog Catholic-military theocracy, worn concrete; muted olive-drab, pale celeste and cream palette. medium shot in a cramped underground hideout, bare bulb light, tense close framing.

**② prompt-character** (middle, variable — the subject):
a 21-year-old man, gaunt, lean, mestizo, Mapuche features, plain simple expression, unfocused eyes, a machete at the hip, natural overcast light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
insurgent red-army fervor, patched red cloth, improvised gear, defiant underground resolve, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | resistencia_subterranea |
| rango | militante_resistencia |
| especialidad | especialidad-combate-asalto |
| edad | 21 |
| genero | m |
| atributos | cuerpo 3 / mente 2 / alma 3 |
