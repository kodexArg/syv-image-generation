# Findings de calibración — Z-Image Turbo / acuarela (jun 2026)

Aprendizajes de la sesión de retratos de Luisa la Pescadora. Complementa
[`z-image-turbo.md`](z-image-turbo.md) (receta canónica) con lo que se descubrió
empíricamente sobre **estilo acuarela, fondos y transparencia**.

## 1. Acuarela FUERTE con manchas — la receta que funciona

| Palanca | Valor | Por qué |
|---|---|---|
| Latente | **vacío** (papel blanco) | la acuarela vive sobre papel; el blanco hace respirar los washes |
| **CFG** | **2.0** (no 1.0) | a CFG 1 el modelo vuelve a **foto**; CFG ~2 **liga el estilo**. >2 fríe |
| Prompt | **liderado por el medio** | arrancar con `Vivid loose watercolor painting of…` |
| Manchas | explícitas | `heavy pigment blooms, cauliflower backruns, splattered ink droplets, dripping edges, granulating washes` |
| Pistas foto | **SACAR** | nada de `visible pores`, `photoreal`, `40yo mestiza skin` → arrastran a foto |

> Regla: **CFG 1 = foto, CFG 2 = acuarela.** Y cuantos más descriptores fotográficos
> apiles, más se va a foto. Menos sujeto realista, más medio.

## 2. Fondo negro: el latente negro NO sirve para acuarela

Probado img2img desde un latente `#000000` (`LoadImage` negro → `VAEEncode` → KSampler):
- **denoise alto (~0.9):** el negro se renoisea casi entero → vuelve a foto diurna.
- **denoise bajo (~0.65):** el modelo no forma el sujeto → sale **negro entero**.

Para **negro plano** real (sin acuarela) sí funciona: **low-key tenebrista** por prompt
(`single hard light on her face, the rest into solid pure black, total darkness`) con
latente vacío — pero ahí cede el medio (sale foto/pintura realista, no acuarela).

**Acuarela y negro plano tiran en contra.** El negro que sí convive con acuarela es
**gesto pictórico**, no fondo: `deep black-to-amber gradient, bold ink lines` (ver
`AcuarelaNegra` / v4).

## 3. Transparencia para destinos oscuros

La acuarela tiene **fondo papel BLANCO** → lo que hay que volver transparente es el
**blanco**, no el negro.
- Un **key tonal** (luminancia→alpha) **se come el sujeto claro** (el chal blanco de
  Luisa ≈ papel blanco). No distingue sujeto de fondo por tono.
- `alpha = luminancia` ("screen sobre negro") solo sirve si el arte es **claro sobre
  negro**, no para acuarela-sobre-blanco.
- **Solución limpia:** segmentación de sujeto (`rembg`/u2net) → recorte real con alpha,
  chal intacto, fondo fuera. Pendiente de instalar (`uv pip install rembg onnxruntime`,
  ~170 MB modelo).

## 4. Workflows guardados

| Workflow | Qué es |
|---|---|
| `AcuarelaNegra` (ComfyUI user) | v4 chiaroscuro: prompt `Dramatic chiaroscuro watercolor portrait…`, CFG 1, gradiente negro-ámbar como gesto |
| `workflows/syv_zimage_turbo.json` | base Z-Image Turbo GGUF (10 nodos), 704×960 |
| `scripts/generate_zimage_panorama.py` | generación batch por API |
| `scripts/prompt_compiler.py` | compilador determinista stat→descriptor |

**Tamaño canónico: 704×960** (rectificado en todos los workflows).

## 5. Compilador de stats (cuerpo/mente/alma → visual)

`scripts/prompt_compiler.py`. Leyes:
- **centro = silencio** (stat 3 → no emite nada).
- **asimetría**: low describe carencia, high describe presencia/impacto.
- **canal por atributo**: cuerpo→cuerpo · mente→mirada/rostro (NO lentes) · alma→aura/porte.
- **pool + hash determinista** (`md5(slug+atributo)`): mismo input → mismo output, varía entre personajes.
- **gating por facción** (laborer/soldier/authority/mystic flavorea el pool de cuerpo).
- **alma maneja la luz** (alma alto → rim light dramático; bajo → luz plana).

## 6. LoRAs Civitai

- Descargas requieren token: `~/.config/civitai/token` → `?token=<key>`.
- Solo **LoRAs nativas Z-Image (ZIT)** cargan (SDXL/Pony no).
- Instalada: `ZIT-FullBigTTsceneGFLadyMk1.safetensors` (FullRebelLady EmoScene),
  trigger `ZIT-fullbigttscenegflady-mk.1`, peso 0.8–1.0.
- Cableado: `LoraLoaderModelOnly` entre `UnetLoaderGGUF` y `ModelSamplingAuraFlow`.

## 7. Ops

- Antes de generar pesado: **matar `local-llm`** (`pkill -f Services/local-llm`) → libera ~1.9 GB VRAM en el 2060 Super.
- Nodo GGUF: `city96/ComfyUI-GGUF` (+ lib `gguf` en el venv, vía `uv pip`).
- Tras tirada: render ~40-65s (recarga el modelo entre tiradas).
