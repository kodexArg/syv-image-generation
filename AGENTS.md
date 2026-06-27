# AGENTS.md — `syv-image-prompts`

Playground de generación de imágenes SyV con **ComfyUI**. Este AGENTS.md manda
sobre el de la raíz `~/Dev/SyV/` cuando trabajás *dentro* de este repo.

## Qué es

Banco de pruebas: prompts, workflows y modelos de ComfyUI para el universo
*Subordinación y Valor*. Se exportan las imágenes desde ComfyUI a este repo y se
documenta cada prueba en `docs/`.

## El ecosistema: a quién servís y qué necesitás

Este repo **no vive solo**: es la **fábrica de retratos** del ecosistema SyV
(`~/Dev/SyV/`). No hace falta que sepas todo el universo para operar acá, pero sí
quién te alimenta y quién te consume.

### Te alimenta: `../syv-pj` (crítico)

Los **sujetos a retratar no se inventan acá**: viven en el repo hermano
**`syv-pj`**, el módulo de la entidad mínima de SyV (el *personaje*). Sus
**personajes mock** — las fichas canónicas de ejemplo — son la materia prima de
todo retrato:

- **Ubicación:** `../syv-pj/resources/personajes/*.md` (34 fichas, agrupadas por
  facción: Fuerzas Armadas/Confederación · Resistencia Subterránea/Ejército Rojo ·
  Iglesia/Inquisición · facciones menores). Índice en `_moc-personajes.md`.
- **Qué leés de cada ficha** (frontmatter YAML + prosa): `nombre`, `faccion`,
  `rango`, `especialidad`, `edad`, `genero`, `aspectos`, `rasgos`, `equipo` y la
  `description` / prosa narrativa. De ahí salen el sujeto, su facción y su
  tratamiento visual.
- **Cómo lo resuelven los scripts** (`scripts/generate_portraits.py`), en orden:
  1. `$SYV_PJ_PATH/resources/personajes/`
  2. hermano `../syv-pj/resources/personajes/` (default)
  3. `../syv-pj-api/vendor/syv-pj/resources/personajes/`

  Si ninguno existe, no hay a quién retratar: cortá y avisá.

> `syv-pj` es **solo lectura** desde acá. Es un playground hermano, pero este
> repo **no escribe** fichas de personaje — solo las lee como entrada.

### A quién servís: el creador de personajes

Tu **servicio** es la imagen: el retrato / ficha visual del personaje. Lo consume
la línea del **creador de personajes** — `syv-pj` (define la entidad y declara la
*generación visual* como uno de sus casos de uso), `syv-pj-api` (motor backend) y
los visualizadores `syv-pj-frontend` / `syv-pj-flutter` (muestran la ficha
visual). La **paleta** y el **lore** (facciones, lugares) salen de `syv-docs` vía
la MCP `markdown-vault-syv` (ver regla 4).

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
