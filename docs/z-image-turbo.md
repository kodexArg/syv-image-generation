# Z Image Turbo — referencia canónica

Modelo activo para retratos SyV desde jun 2026. Reemplaza a zavy/Pony.
Arquitectura S3-DiT (transformer unificado), 6.15B parámetros, text encoder Qwen3-4B.

## Stack ComfyUI

| Componente | Archivo | Nodo |
|---|---|---|
| UNet GGUF | `zimageTurboByStable_2602Q8.gguf` | `UnetLoaderGGUF` (city96/ComfyUI-GGUF) |
| Text encoder | `qwen_3_4b.safetensors` | `CLIPLoader` — type `lumina2` |
| VAE | `ae.safetensors` | `VAELoader` |

Fuente: HF `Comfy-Org/z_image_turbo` (sin token de acceso).

## Receta canónica

```
Workflow:    workflows/syv_zimage_turbo.json
Scheduler:  res_multistep / simple
Sampler:    Euler o Euler Ancestral
Steps:      8  (fijo — no mejora con más)
CFG:        1  (sin guidance clásico; 0.0 también funciona)
Shift:      3  (ModelSamplingAuraFlow)
Negativo:   ConditioningZeroOut (no hay prompt negativo)
Resolución: ~1MP es el régimen óptimo (1024×1024 baseline; 1328×1328 sweet spot)
```

### Resolución — régimen óptimo, buckets oficiales y 704×960

Z-Image es resolución-flexible (S3-DiT, no UNet de resolución fija), pero no
arbitraria. Hay **una restricción dura y un régimen recomendado**:

- **Dura (arquitectura):** ancho y alto **deben ser divisibles por 16**
  (8× VAE + 2× patch). No es opcional. *704 y 960 lo cumplen.*
- **Recomendado (autor):** quedarse a **±256 px de la base 1024** → rango
  práctico **~768–1280 px** por lado. Techo: **no pasar de 2048 px**.
- **Óptimo práctico:** **~1 megapíxel o más**. El ejemplo oficial de HF genera
  a **1024×1024**; la comunidad cita **1328×1328** como sweet spot de detalle.

El modelo se entrenó sobre **buckets de aspecto** (grids oficiales del HF Space).
Generar *dentro* de un bucket da el mejor resultado. Buckets base-1024
(11 aspectos; portrait relevantes para retrato):

| Resolución (base 1024) | Aspecto | Megapíxeles | Uso |
|---|---|---|---|
| 1024×1024 | 1:1 | 1.05 MP | baseline confiable |
| 864×1152 | 3:4 | 0.99 MP | **retrato — bucket nativo** |
| 832×1248 | 2:3 | 1.04 MP | **retrato vertical — bucket nativo** |
| 1280×1280 (base 1280) | 1:1 | 1.64 MP | máximo detalle dentro de rango |

**704×960 (resolución de trabajo actual) — veredicto:** es **divisible por 16
(legal)** y el modelo lo genera sin problemas, pero es **sub-óptimo**: 0.68 MP
queda por debajo del umbral de ~1MP, **no es un bucket de entrenamiento**, y el
lado corto (704 px) cae por debajo del piso recomendado de ~768 px. Resultado
esperado: imágenes usables pero **más blandas / con menos detalle** que a ~1MP.

→ **Para retratos de calidad, preferir `864×1152` (3:4) o `832×1248` (2:3)** —
buckets nativos, ≥~1MP, mismo encuadre vertical. Reservá 704×960 para
borrador/modo rápido.

Las proporciones no-cuadradas de retrato (3:4, 2:3) están bien soportadas (son
buckets nativos); los aspectos extremos (21:9 / 9:21) acumulan artefactos.
Fuente: HF `Tongyi-MAI/Z-Image-Turbo` (discussions del autor: divisible-16,
rango ±256), grids oficiales del HF Space, ComfyUI docs
(`docs.comfy.org/tutorials/image/z-image`), consenso de comunidad.

Pre-generación en el 2060 Super 8GB: matar el servicio `local-llm`
(`pkill -f local-llm` o `systemctl --user stop local-llm`) para liberar ~1.9 GB VRAM.

## Prompting

Qwen3-4B entiende lenguaje natural; booru tags son ignorados o contraproducentes.

**No usar:** `score_9`, `score_8_up`, `masterpiece`, `best quality`, `worst quality`,
`lowres`, ni ningún tag booru. Tampoco prompt negativo.

**Estructura recomendada:**

```
[SUJETO]   <género, edad, rol/facción>
[ASPECTO]  <rasgos físicos, expresión, complexión — en prosa>
[EQUIPO]   <vestimenta, insignias, equipo — describiendo, no listando>
[ESCENA]   <atmósfera SyV: concreto gastado, lluvia, low-tech analógico>
[TÉCNICO]  <lente (35mm/85mm), película (35mm film), iluminación, grade>
```

Ejemplo SyV completo:
```
cinematic portrait, tired soldier woman in her 40s, Ejército Rojo officer,
short dark hair with grey streaks, intense gaze, gaunt face,
worn olive drab uniform with faded rank insignia, cracked concrete wall background,
perpetual rain, analog low-tech aesthetic,
85mm lens, 35mm film grain, harsh side lighting with soft fill,
teal-amber color grade, shallow depth of field
```

## LoRAs

LoRAs de SDXL/Pony **no cargan** (arquitecturas incompatibles: UNet vs S3-DiT).
Usar exclusivamente LoRAs nativas Z-Image.

### Cinematic Portrait Lighting LoRA (activa)

- **CivitAI:** civitai.com/models/2595570 (Cinematic Portrait Lighting LoRA — zimg-turbo-sdxl)
- Especialidad: iluminación de estudio / cinematográfica — rim lights, soft fill,
  golden hour, key light lateral
- Compatible directa con el stack actual; no requiere ajustes de receta
- Trigger word: verificar en la página del modelo (puede ser opcional con lenguaje natural)
- Aplicar vía nodo `Load LoRA` antes del sampler; strength recomendado: 0.6–0.9

### Otras LoRAs nativas Z-Image (comunidad 2025)

- `CyberRealistic Z-Image Turbo` — fotorrealismo extremo
- `Realistic Snapshot` — fotografía de calle/candid
- 80+ LoRAs en civitai.com/models bajo tag `z-image-turbo`

## Comparación vs SDXL Turbo

| | Z Image Turbo | SDXL Turbo |
|---|---|---|
| Arquitectura | S3-DiT (transformer) | UNet |
| Pasos | 8 | 1–4 |
| Resolución | hasta 1024×1024 | 512×512 fija |
| Text encoder | Qwen3-4B (LLM) | CLIP |
| Prompting | lenguaje natural | booru tags |
| Negativo | no (ZeroOut) | sí (CFG=0 igual) |
| Tenebrismo/cine | sí, nativo | no (ignoraba descriptores) |
| LoRAs SDXL | incompatible | compatible |
| Licencia | Apache 2.0 | nc-community |

## Variantes cuantizadas

Para < 10 GB VRAM:

| Variante | Repo HF | VRAM aprox |
|---|---|---|
| FP8 (bfloat16 a FP8) | `drbaph/Z-Image-Turbo-FP8` | ~8 GB |
| GGUF Q8 (activo) | `zimageTurboByStable_2602Q8.gguf` | ~7–8 GB |
| GGUF Q4 | `leejet/Z-Image-Turbo-GGUF` | ~4–5 GB |

El Q8 GGUF es el balance óptimo calidad/VRAM para el 2060 Super 8GB.

## Entrenamiento de LoRAs nativas

Base requerida: `Tongyi-MAI/Z-Image-Omni-Base` (el Turbo distillado es inferencia-only).
Trainer: Ostris AI Toolkit (documentado en HF Blog).
Captions: lenguaje natural (no booru). Trigger: token único sin colisión con Qwen3.
