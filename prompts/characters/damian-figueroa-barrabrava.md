---
title: Damián Figueroa · ficha ComfyUI (v7)
folder: prompts/characters
slug: damian-figueroa-barrabrava
source: syv-pj/resources/personajes/damian-figueroa-barrabrava.md
description: Compilación determinista de Damián Figueroa para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Damián Figueroa · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/damian-figueroa-barrabrava.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | +0.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | +0.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | +0.0 | `cuerpo - 3`, clamp -2..+3.0 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
World of Subordinación y Valor: cold rain-grey overcast light, low-tech analog Catholic-military theocracy, worn concrete; muted olive-drab, pale celeste and cream palette. medium shot in a cramped underground hideout, bare bulb light, tense close framing.

**② prompt-character** (middle, variable — the subject):
a 35-year-old man, corpulent, heavyset, bearded, criollo (mixed Spanish-American), plain simple expression, unfocused eyes, quiet anodyne bearing, weary downcast eyes, a battered trumpet, flat even light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
insurgent red-army fervor, patched red cloth, improvised gear, defiant underground resolve, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | resistencia_subterranea |
| rango | simpatizante |
| especialidad | null |
| edad | 35 |
| genero | m |
| atributos | cuerpo 3 / mente 2 / alma 2 |
