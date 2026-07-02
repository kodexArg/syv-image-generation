---
title: Baltasar Quevedo · ficha ComfyUI (v7)
folder: prompts/characters
slug: baltasar-quevedo-inquisidor
source: syv-pj/resources/personajes/baltasar-quevedo-inquisidor.md
description: Compilación determinista de Baltasar Quevedo para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Baltasar Quevedo · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/baltasar-quevedo-inquisidor.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | -1.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | +1.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | +1.0 | `cuerpo - 3`, clamp -2..+3.0 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
World of Subordinación y Valor: cold rain-grey overcast light, low-tech analog Catholic-military theocracy, worn concrete; muted olive-drab, pale celeste and cream palette. medium shot in a damp candle-lit stone hall, low three-quarter angle, oppressive gloom.

**② prompt-character** (middle, variable — the subject):
a 28-year-old man, burly, criollo (mixed Spanish-American), fit trained build, plain simple expression, unfocused eyes, a consecrated sword, a long dark cassock, a blessed medallion, natural overcast light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
state propaganda order, olive-drab and celeste discipline, brass insignia, dignified martial bearing, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | iglesia |
| rango | novicio |
| especialidad | especialidad-combate-cruzado |
| edad | 28 |
| genero | m |
| atributos | cuerpo 4 / mente 2 / alma 3 |
