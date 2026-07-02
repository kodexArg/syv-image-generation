# Whitelist — Z-Image Turbo / Qwen3-4B (lumina2)

> Reseteado jul 2026. Modelo canónico: **Z Image Turbo** (S3-DiT, text encoder Qwen3-4B).
> Prompts en lenguaje natural fotográfico. Sin booru tags. Sin negativo (ConditioningZeroOut).

Memoria de calibración. Antes de generar un prompt nuevo se lee esto: **reforzar
lo que funcionó (Buenos), evitar lo que no (Malos)**.

Cada entrada es el **combo completo** de un prompt ComfyUI guardado como JSON:
`Positivo` (lo que el modelo busca) + `Negativo` (lo que excluye). Los wrappers
(`personaje`, `estilo`, `rating`, `fuente`) son metadatos para reusar el combo;
el corazón es el par `Positivo`/`Negativo`.

- **Buenos** = combos que sirvieron (`rating >= 4`).
- **Malos** = combos que no sirvieron (`rating <= 2`).
- `fuente` enlaza a la entrega original en `inbox/` (wikilink Obsidian).
- Idempotente: no dupliques un combo ya presente.

## Buenos

_(vacío)_

<!-- Plantilla por entrada:
```json
{
  "personaje": "<slug>",
  "estilo": "<propaganda-screenprint | realista-cinematografico | pixel-art>",
  "rating": 5,
  "fuente": "[[inbox/<AAAAMMDD>-<personaje>-<estilo>/entry]]",
  "Positivo": "...",
  "Negativo": "..."
}
```
-->

## Malos

_(vacío)_
