# Flujo de una prueba — de punta a punta

Cómo correr una prueba de generación y dejarla documentada. La meta del repo:
**toda imagen tiene su nota** con el prompt y los parámetros que la produjeron,
de modo que sea reproducible.

## 1. Arrancar ComfyUI

Vía el skill `comfyui`:

```bash
~/.agents/skills/comfyui/scripts/comfyctl status   # ¿está arriba?
~/.agents/skills/comfyui/scripts/comfyctl start --port 8188 --enable-manager
```

## 2. Cargar workflow y generar

Abrí `http://127.0.0.1:8188`, cargá un `.json` de `workflows/`, ajustá prompt /
seed / params y generá. (O automatizá con el `_api.json` vía el comfyui-mcp /
HTTP `/prompt`.)

> La paleta y los nombres salen del canon: consultá `syv-docs/` por la MCP
> `markdown-vault-syv` antes de fijar una serie. No se inventa canon acá.

## 3. Exportar las imágenes al repo

ComfyUI escribe en su output dir; este repo las importa a `images/raw/`:

```bash
uv run scripts/export.py                              # últimos 5 PNG
uv run scripts/export.py --prefix syv_pixel_art_portrait
uv run scripts/export.py --since 30                   # últimos 30 min
```

`images/raw/` está en `.gitignore`: el bulk crudo no se versiona.

## 4. Entregar al `inbox`

Cada generación es una carpeta `prompts/inbox/<AAAAMMDD>-<personaje>-<estilo>/`:

- **`preview.png`** — la imagen curada (se commitea; `inbox/` no está ignorado).
- **`entry.md`** — prompt positivo + negativo completos y los metadatos
  (personaje, facción, estilo, checkpoint, sampler, scheduler, steps, cfg, seed,
  resolución, workflow) + el bloque de evaluación vacío (`rating: null`,
  `liked`, `disliked`).

```bash
mkdir -p prompts/inbox/20260628-oficial-propaganda
cp images/raw/syv_..._00012_.png prompts/inbox/20260628-oficial-propaganda/preview.png
# escribí entry.md con prompt + metadatos
```

## 5. Ranking → whitelist (el loop)

El usuario pone `rating: 1-5` en el `entry.md`. Cuando esté rankeado, promové el
link Obsidian a `prompts/whitelist.md`: `rating >= 4` → `## Positivos`,
`rating <= 2` → `## Negativos`. Antes de la próxima generación, leé esa whitelist
para reforzar lo que funcionó y evitar lo que no.

## Convenciones

- **Slug de entrega:** `AAAAMMDD-<personaje>-<estilo>` (`20260628-oficial-propaganda`).
- **Una carpeta por entrega** en `inbox/` (imagen + metadatos juntos).
- **Seed siempre anotado** — sin seed no hay reproducibilidad.
- **Prompt completo, literal** — nada de "el de siempre con cambios".
