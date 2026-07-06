# ComfyUI — setup en esta máquina

Referencia del entorno ComfyUI usado por este repo. No hardcodees nada en
código: el skill `comfyui` y `scripts/export.py` autodetectan el root. Esto es
solo documentación de lo que hay hoy (verificado 2026-06-27).

## Rutas

| Qué | Dónde |
|---|---|
| Root ComfyUI | `/home/kodex/ComfyUI` |
| Output (PNG generados) | `/home/kodex/ComfyUI/output` |
| venv | `/home/kodex/ComfyUI/.venv` (uv) |
| Puerto HTTP | `8188` (`http://127.0.0.1:8188`) |
| `last_root` (lo deja el skill) | `~/.config/comfyui/last_root` |

`scripts/export.py` importa los PNG desde el output dir hacia `images/raw/`
sin tocar el origen.

## Lifecycle (vía skill `comfyui`)

```bash
~/SyV/syv-harness/skills/comfyui/scripts/comfyctl status      # proceso + HTTP + cola + modelos
~/SyV/syv-harness/skills/comfyui/scripts/comfyctl start --listen 0.0.0.0 --port 8188 --enable-manager
~/SyV/syv-harness/skills/comfyui/scripts/comfyctl stop
~/SyV/syv-harness/skills/comfyui/scripts/comfyctl url
```

## MCP

El skill `comfyui` exige un **chequeo de liveness del comfyui-mcp** antes de
usar sus tools (`generate-image`, `health-check`, `queue`, `workflow-*`…). Si
las tools no aparecen en la sesión, el MCP no está registrado: se cae al
control por HTTP + `comfyctl` (igual de funcional). Ver el SKILL.md del skill.

## Modelos en uso

### Canónico — Z Image Turbo (jun 2026)

| Componente | Archivo | Nodo ComfyUI |
|---|---|---|
| UNet GGUF | `zimageTurboByStable_2602Q8.gguf` | `UnetLoaderGGUF` (city96/ComfyUI-GGUF) |
| Text encoder | `qwen_3_4b.safetensors` | `CLIPLoader` — type `lumina2` |
| VAE | `ae.safetensors` | `VAELoader` |

Fuente: HF `Comfy-Org/z_image_turbo` (sin token). Workflow: `syv_zimage_turbo.json`.
Receta: `res_multistep`/`simple`, 8 steps, CFG 1, shift 3 (`ModelSamplingAuraFlow`),
sin negativo (`ConditioningZeroOut`). Resolución mínima: 704×960.
Pre-generación: matar `local-llm` para liberar ~1.9 GB VRAM (2060 Super 8GB).

### Legacy — Pony/zavy (deprecado)

- `zavyfantasiaxlPDXL_v20.safetensors` (SDXL/Pony-style). Requería tags
  `score_9, score_8_up, score_7_up` en positivo y `score_6, score_5, score_4`
  en negativo. **No da tenebrismo** — reemplazado por Z Image Turbo (jun 2026).

## Formato de los workflows

Cada workflow se guarda en dos formas en `workflows/`:

- `<nombre>.json` — formato **UI** (el que abrís/editás en ComfyUI).
- `<nombre>_api.json` — formato **API** (nodos por id; para automatizar vía
  HTTP `/prompt` o el comfyui-mcp).

El nodo `SaveImage` define el `filename_prefix`, que es el prefijo con el que
salen los PNG en el output (útil para `export.py --prefix`).
