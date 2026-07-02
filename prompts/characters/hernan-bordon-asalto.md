---
title: Hernán Bordón · ficha ComfyUI (v7)
folder: prompts/characters
slug: hernan-bordon-asalto
source: syv-pj/resources/personajes/hernan-bordon-asalto.md
description: Compilación determinista de Hernán Bordón para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Hernán Bordón · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/hernan-bordon-asalto.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | -1.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | +1.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | +1.0 | `cuerpo - 3`, clamp -2..+3.0 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
World of Subordinación y Valor: cold rain-grey overcast light, low-tech analog Catholic-military theocracy, worn concrete; muted olive-drab, pale celeste and cream palette. medium shot at a muddy fortified encampment, grey overcast, slight low angle, militarized dystopia.

**② prompt-character** (middle, variable — the subject):
a 27-year-old man, gaunt, lean, criollo (mixed Spanish-American), shaved head, solid athletic build, quiet anodyne bearing, weary downcast eyes, a slung submachine gun, a grenade on the belt, a heavy assault vest, an olive-drab state-issue uniform, flat even light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
state propaganda order, olive-drab and celeste discipline, brass insignia, dignified martial bearing, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | fuerzas_armadas |
| rango | soldado_linea |
| especialidad | especialidad-combate-asalto |
| edad | 27 |
| genero | m |
| atributos | cuerpo 4 / mente 3 / alma 2 |
