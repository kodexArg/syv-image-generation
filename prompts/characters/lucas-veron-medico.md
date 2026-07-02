---
title: Lucas Verón · ficha ComfyUI (v7)
folder: prompts/characters
slug: lucas-veron-medico
source: syv-pj/resources/personajes/lucas-veron-medico.md
description: Compilación determinista de Lucas Verón para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Lucas Verón · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/lucas-veron-medico.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | -1.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | -1.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | -1.0 | `cuerpo - 3`, clamp -2..+3.0 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
World of Subordinación y Valor: cold rain-grey overcast light, low-tech analog Catholic-military theocracy, worn concrete; muted olive-drab, pale celeste and cream palette. medium shot at a muddy fortified encampment, grey overcast, slight low angle, militarized dystopia.

**② prompt-character** (middle, variable — the subject):
a 29-year-old man, criollo (mixed Spanish-American), gaunt, lean, wiry spare build, quiet anodyne bearing, weary downcast eyes, a medical kit, a 9mm sidearm, an olive-drab state-issue uniform, flat even light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
state propaganda order, olive-drab and celeste discipline, brass insignia, dignified martial bearing, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | fuerzas_armadas |
| rango | soldado_linea |
| especialidad | especialidad-oficio-medico |
| edad | 29 |
| genero | m |
| atributos | cuerpo 2 / mente 3 / alma 2 |
