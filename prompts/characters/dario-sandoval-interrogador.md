---
title: Darío Sandoval · ficha ComfyUI (v7)
folder: prompts/characters
slug: dario-sandoval-interrogador
source: syv-pj/resources/personajes/dario-sandoval-interrogador.md
description: Compilación determinista de Darío Sandoval para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Darío Sandoval · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/dario-sandoval-interrogador.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | +0.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | +0.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | +0.0 | `cuerpo - 3`, clamp -2..+3.0 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
World of Subordinación y Valor: cold rain-grey overcast light, low-tech analog Catholic-military theocracy, worn concrete; muted olive-drab, pale celeste and cream palette. medium shot at a muddy fortified encampment, grey overcast, slight low angle, militarized dystopia.

**② prompt-character** (middle, variable — the subject):
a 36-year-old man, criollo (mixed Spanish-American), short hair, cold stare, warm magnetic presence, engaged gaze, a 9mm sidearm, an olive-drab state-issue uniform, a heavy assault vest, natural overcast light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
state propaganda order, olive-drab and celeste discipline, brass insignia, dignified martial bearing, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | fuerzas_armadas |
| rango | cabo |
| especialidad | especialidad-investigacion-interrogador |
| edad | 36 |
| genero | m |
| atributos | cuerpo 3 / mente 3 / alma 4 |
