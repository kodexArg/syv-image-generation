---
title: Ovidio Gauna · ficha ComfyUI (v7)
folder: prompts/characters
slug: ovidio-gauna-sargento
source: syv-pj/resources/personajes/ovidio-gauna-sargento.md
description: Compilación determinista de Ovidio Gauna para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Ovidio Gauna · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/ovidio-gauna-sargento.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | +1.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | +1.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | +1.0 | `cuerpo - 3`, clamp -2..+3.0 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
World of Subordinación y Valor: cold rain-grey overcast light, low-tech analog Catholic-military theocracy, worn concrete; muted olive-drab, pale celeste and cream palette. medium shot at a muddy fortified encampment, grey overcast, slight low angle, militarized dystopia.

**② prompt-character** (middle, variable — the subject):
a 40-year-old man, criollo (mixed Spanish-American), grey-haired, mustache, solid athletic build, alert attentive eyes, sharp focus, commanding presence, regal bearing, intense steady gaze, a slung submachine gun, a 9mm sidearm, a heavy assault vest, an olive-drab state-issue uniform, lit with a subtle hero rim light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
state propaganda order, olive-drab and celeste discipline, brass insignia, dignified martial bearing, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | fuerzas_armadas |
| rango | sargento |
| especialidad | especialidad-combate-lider |
| edad | 40 |
| genero | m |
| atributos | cuerpo 4 / mente 4 / alma 5 |
