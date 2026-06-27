# Prueba — <título>

- **Fecha:** AAAA-MM-DD
- **Slug:** AAAAMMDD-<slug>
- **Objetivo:** qué se quería lograr / qué hipótesis se prueba.
- **Entidad SyV / referencia de canon:** `[[...]]` (de `syv-docs/`), si aplica.

## Parámetros

| Campo | Valor |
|---|---|
| Workflow | `workflows/<archivo>.json` |
| Checkpoint | `<modelo>.safetensors` |
| Resolución | `1024x1024` (→ downscale 64 → upscale 512, etc.) |
| Sampler | `dpmpp_2m` |
| Scheduler | `karras` |
| Steps | `28` |
| CFG | `7.0` |
| Seed | `<seed>` |

## Prompt

**Positivo:**

```
<prompt positivo literal>
```

**Negativo:**

```
<prompt negativo literal>
```

## Resultado

![[seleccionadas/<archivo>.png]]   <!-- o ruta relativa images/seleccionadas/... -->

## Conclusiones

- Qué funcionó.
- Qué no.
- Próximos ajustes a probar (seed, cfg, paleta, modelo…).
