---
title: Iván Leiva · ficha ComfyUI (v7)
folder: prompts/characters
slug: ivan-leiva-asalto
source: syv-pj/resources/personajes/ivan-leiva-asalto.md
description: Compilación determinista de Iván Leiva para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Iván Leiva · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/ivan-leiva-asalto.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | -1.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | +0.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | +0.0 | `cuerpo - 3`, clamp -2..+3.0 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
World of Subordinación y Valor: cold rain-grey overcast light, low-tech analog Catholic-military theocracy, worn concrete; muted olive-drab, pale celeste and cream palette. medium shot at a muddy fortified encampment, grey overcast, slight low angle, militarized dystopia.

**② prompt-character** (middle, variable — the subject):
a 24-year-old man, criollo (mixed Spanish-American), dark-haired olive-skinned, quiet anodyne bearing, weary downcast eyes, a slung submachine gun, a heavy assault vest, an olive-drab state-issue uniform, spare magazines at the belt, flat even light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
state propaganda order, olive-drab and celeste discipline, brass insignia, dignified martial bearing, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | fuerzas_armadas |
| rango | soldado_linea |
| especialidad | especialidad-combate-asalto |
| edad | 24 |
| genero | m |
| atributos | cuerpo 3 / mente 3 / alma 2 |
