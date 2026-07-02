---
title: Eulogio Sarmiento · ficha ComfyUI (v7)
folder: prompts/characters
slug: eulogio-sarmiento-capellan
source: syv-pj/resources/personajes/eulogio-sarmiento-capellan.md
description: Compilación determinista de Eulogio Sarmiento para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Eulogio Sarmiento · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/eulogio-sarmiento-capellan.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | +2.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | +0.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | +0.0 | `cuerpo - 3`, clamp -2..+3.0 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
World of Subordinación y Valor: cold rain-grey overcast light, low-tech analog Catholic-military theocracy, worn concrete; muted olive-drab, pale celeste and cream palette. medium shot in a damp candle-lit stone hall, low three-quarter angle, oppressive gloom.

**② prompt-character** (middle, variable — the subject):
a 52-year-old man, grey-haired, grey-streaked beard, criollo (mixed Spanish-American), plain simple expression, unfocused eyes, overwhelming magnetic aura, luminous commanding gaze, a small healing vial, a jar of medicinal ointment, a long dark cassock, a worn rosary, haloed by dramatic rim light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
state propaganda order, olive-drab and celeste discipline, brass insignia, dignified martial bearing, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | iglesia |
| rango | sacerdote |
| especialidad | especialidad-oficio-medico |
| edad | 52 |
| genero | m |
| atributos | cuerpo 3 / mente 2 / alma 6 |
