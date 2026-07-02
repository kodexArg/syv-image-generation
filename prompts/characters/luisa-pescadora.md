---
title: Luisa · ficha ComfyUI (v7)
folder: prompts/characters
slug: luisa-pescadora
source: syv-pj/resources/personajes/luisa-pescadora.md
description: Compilación determinista de Luisa para el workflow ComfyUI v7 (Z-Image Turbo).
---

# Luisa · ficha ComfyUI (v7)

Generado por `scripts/sheet_to_comfy.py` desde `[[syv-pj/resources/personajes/luisa-pescadora.md]]`.
No editar a mano — volver a correr el script si la ficha fuente cambia.

## Sliders (v7 LoraLoader strengths)

| slider | valor | fórmula |
|---|---|---|
| age | +1.0 | `(edad // 10) - 3`, clamp -3..+3 |
| fat | +1.0 | `cuerpo - 3`, clamp -1..+1 |
| muscle | +1.0 | `cuerpo - 3`, clamp -2..+1.5 |

## Prompts (v7 slots ①②③)

**① prompt-scene** (top, fixed — camera + setting):
World of Subordinación y Valor: cold rain-grey overcast light, low-tech analog Catholic-military theocracy, worn concrete; muted olive-drab, pale celeste and cream palette. medium shot on rotting rain-soaked docks, perpetual drizzle, handheld documentary framing.

**② prompt-character** (middle, variable — the subject):
a 40-year-old woman, salt-weathered leathery skin, mestiza, hair tied back, solid athletic build, quiet anodyne bearing, weary downcast eyes, a mended fishing net, a worn rosary, a patched darned shawl, flat even light.

**③ prompt-ambience** (bottom, fixed — faction flavor + style):
worn working-class dignity, salt and rust, honest hard labor, photorealistic skin texture, 35mm film grain.

## Fuente (resumen)

| campo | valor |
|---|---|
| faccion | gremio_de_pescadores |
| rango | marinero |
| especialidad | especialidad-oficio-pescador |
| edad | 40 |
| genero | f |
| atributos | cuerpo 4 / mente 3 / alma 2 |
