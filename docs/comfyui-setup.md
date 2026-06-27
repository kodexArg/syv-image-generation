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
~/.agents/skills/comfyui/scripts/comfyctl status      # proceso + HTTP + cola + modelos
~/.agents/skills/comfyui/scripts/comfyctl start --listen 0.0.0.0 --port 8188 --enable-manager
~/.agents/skills/comfyui/scripts/comfyctl stop
~/.agents/skills/comfyui/scripts/comfyctl url
```

## MCP

El skill `comfyui` exige un **chequeo de liveness del comfyui-mcp** antes de
usar sus tools (`generate-image`, `health-check`, `queue`, `workflow-*`…). Si
las tools no aparecen en la sesión, el MCP no está registrado: se cae al
control por HTTP + `comfyctl` (igual de funcional). Ver el SKILL.md del skill.

## Modelos en uso (pruebas actuales)

- Checkpoint: `zavyfantasiaxlPDXL_v20.safetensors` (PDXL / Pony-style SDXL).
  Por eso los prompts llevan tags `score_9, score_8_up, score_7_up` en
  positivo y `score_6, score_5, score_4` en negativo.

## Formato de los workflows

Cada workflow se guarda en dos formas en `workflows/`:

- `<nombre>.json` — formato **UI** (el que abrís/editás en ComfyUI).
- `<nombre>_api.json` — formato **API** (nodos por id; para automatizar vía
  HTTP `/prompt` o el comfyui-mcp).

El nodo `SaveImage` define el `filename_prefix`, que es el prefijo con el que
salen los PNG en el output (útil para `export.py --prefix`).
