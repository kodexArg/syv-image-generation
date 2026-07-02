---
title: Sofía · ficha ComfyUI (v7)
folder: prompts/characters
slug: sor-sofia-guardaespaldas
source: syv-pj/resources/personajes/sor-sofia-guardaespaldas.md
description: Compilación determinista de Sofía para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Sofía · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/sor-sofia-guardaespaldas.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | -1.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | +1.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | +1.0 | `cuerpo - 3`, clamp -2..+1.0 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
cold rain-grey overcast light, worn concrete and damp plaster walls, analog low-tech dystopia, muted olive-drab, pale celeste and cream palette. half-body portrait, plain worn concrete wall background, soft overcast studio light, neutral eye-level framing, shallow depth of field.

**② prompt-character** (middle, variable — the subject):
a photo of a 25-year-old woman, wiry, fibrous muscle, broad shoulders, calm grey eyes, toned athletic build, strong defined arms, alert attentive eyes, sharp focus, commanding presence, regal bearing, intense steady gaze, clearly female face and body, a consecrated sword, a monastic habit, lit with a subtle hero rim light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
state propaganda order, olive-drab and celeste discipline, brass insignia, dignified martial bearing, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | iglesia |
| rango | novicio |
| especialidad | especialidad-combate-cruzado |
| edad | 25 |
| genero | f |
| atributos | cuerpo 5 / mente 4 / alma 5 |
