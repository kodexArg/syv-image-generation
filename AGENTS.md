# AGENTS.md — `syv-image-prompts`

Playground de generación de imágenes SyV con **ComfyUI**. Este AGENTS.md manda
sobre el de la raíz `~/Dev/SyV/` cuando trabajás *dentro* de este repo.

## Qué es

Banco de pruebas: prompts, workflows y modelos de ComfyUI para el universo
*Subordinación y Valor*. Se exportan las imágenes desde ComfyUI a este repo y se
documenta cada prueba en `docs/`.

## ComfyUI — vía única

Para cualquier tarea de ComfyUI (start/stop/status, cargar workflow, generar,
cola, modelos, exportar imágenes) **usá el skill `comfyui`**. No hardcodees
rutas: el skill autodetecta el root.

- Root detectado en esta máquina: `/home/kodex/ComfyUI`
- Output de ComfyUI: `/home/kodex/ComfyUI/output`
- Las imágenes nacen ahí; este repo las **importa** a `images/raw/` con
  `scripts/export.py`. Ver `docs/comfyui-setup.md`.

## Reglas del repo

1. **`docs/` es la SSOT del repo.** Toda prueba se documenta en
   `docs/tests/AAAAMMDD-<slug>.md`: prompt completo (positivo + negativo),
   modelo/checkpoint, sampler, steps, cfg, seed, resolución, workflow usado y
   conclusión. Sin nota documentada, la prueba no existe.
2. **Imágenes:** los exports crudos van a `images/raw/` y **no se versionan**
   (`.gitignore`). Solo las elegidas pasan a `images/seleccionadas/` y se
   commitean con `git add -f` (ver `docs/workflow.md`).
3. **Workflows** versionados en `workflows/`: guardá el `.json` (UI, editable)
   y el `_api.json` (formato API, para automatizar).
4. **Inspiración del canon:** sacá lugares, personajes, facciones y **paleta**
   de la SSOT `syv-docs/` vía la MCP `markdown-vault-syv` (ver regla del vault
   raíz). No inventes canon acá; este repo no escribe en la SSOT.
5. **Python > Bash**, `uv` para paquetes. Scripts con shebang.

## Paleta SyV (referencia rápida)

Olive drab militar `#7B8A4E` · celeste `#8FB8D6` · crema `#F3EEE4` ·
negro cálido `#0C0B09`. (Confirmá contra `syv-docs/` / `syv-design-system/`
antes de fijar una serie.)
