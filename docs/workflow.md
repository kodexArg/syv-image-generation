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

`images/raw/` está en `.gitignore`: los crudos no se versionan.

## 4. Documentar la prueba

Creá `docs/tests/AAAAMMDD-<slug>.md`. Copiá `docs/tests/_template.md`. Mínimo:
prompt positivo y negativo completos, checkpoint, sampler, steps, cfg, seed,
resolución, workflow usado y una conclusión (qué funcionó, qué no, qué probar
después).

## 5. Seleccionar lo que vale

Las imágenes buenas se mueven a `images/seleccionadas/` y **se fuerzan** al
control de versiones (porque `images/` está ignorado salvo esta carpeta):

```bash
mv images/raw/syv_pixel_art_portrait_00012_.png images/seleccionadas/
git add -f images/seleccionadas/syv_pixel_art_portrait_00012_.png
```

Referenciá la imagen seleccionada desde su nota en `docs/tests/`.

## Convenciones

- **Slug de prueba:** `AAAAMMDD-<tema>` (`20260627-pixel-art-oficial`).
- **Una nota por prueba o por serie corta** con la misma intención.
- **Seed siempre anotado** — sin seed no hay reproducibilidad.
- **Prompt completo, literal** — nada de "el de siempre con cambios".
