---
title: SyV — clause atmosférico (system común)
folder: prompts
description: Factor común que inyecta la atmósfera de Subordinación y Valor en cada prompt de imagen, con el menor gasto de tokens posible. Se teje al final del positivo.
---

# Clause atmosférico SyV (el "system" de cada retrato)

Factor común, breve, agnóstico de sujeto: da el mundo sin describir la escena.
Se **antepone o teje al final** del positivo de cada generación. Pensado para
Z-Image Turbo (lenguaje natural, sin booru, sin negativo).

## Canónico (usar este)

```
World of Subordinación y Valor: cold rain-grey overcast light, low-tech analog Catholic-military theocracy, worn concrete; muted olive-drab, pale celeste and cream palette.
```

- **~22 palabras / ~30 tokens.** No repite calidad ni lente (eso lo trae el prompt del sujeto).
- Trabaja por **luz + paleta + mundo**, no por props de escena → no pelea con close-ups.
- Fuente de los elementos: `AGENTS.md` (paleta obligatoria) + `inbox/.../setup.md`
  (lluvia perpetua, low-tech analógico, theocracia militar-católica). No inventa canon.

## Variante mínima (si sobran tokens en otro lado)

```
Subordinación y Valor: rain-grey overcast, worn analog Catholic-military theocracy; olive-drab, celeste and cream palette.
```
