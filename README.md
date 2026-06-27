# syv-image-prompts

Banco de pruebas (playground) de **generación de imágenes para el universo
*Subordinación y Valor*** usando **ComfyUI**. Acá se experimenta con prompts,
workflows y modelos; se exportan las imágenes desde ComfyUI a este repo y se
documenta cada prueba en Markdown.

> Es un *playground* del ecosistema SyV. La inspiración (lugares, facciones,
> personajes, paleta) sale de la SSOT `syv-docs/`; las herramientas se
> construyen alrededor de ella.

## Estructura

```
syv-image-prompts/
├── README.md            ← este archivo
├── AGENTS.md            ← reglas para agentes (CLAUDE.md → symlink)
├── docs/                ← TODA la documentación de pruebas (SSOT del repo)
│   ├── workflow.md      ← cómo correr una prueba de punta a punta
│   ├── comfyui-setup.md ← root de ComfyUI, output dir, modelos, MCP
│   └── tests/           ← una nota .md por prueba/serie de pruebas
├── workflows/           ← workflows ComfyUI versionados (.json + _api.json)
├── prompts/             ← prompts reutilizables (texto plano / .md)
├── images/
│   ├── raw/             ← exports crudos (NO versionados, .gitignore)
│   └── seleccionadas/   ← las que valen — se commitean con `git add -f`
└── scripts/
    └── export.py        ← copia los últimos PNG de ComfyUI/output → images/raw
```

## Flujo rápido

1. Arrancá ComfyUI (skill `comfyui` / `comfyctl start`).
2. Cargá un workflow de `workflows/` y generá.
3. Exportá los PNG: `uv run scripts/export.py` (o `python3 scripts/export.py`).
4. Documentá la prueba en `docs/tests/AAAAMMDD-<slug>.md` (prompt, params,
   seed, modelo, resultado, conclusiones).
5. Las imágenes que valen → `images/seleccionadas/` y `git add -f`.

Ver `docs/workflow.md` para el detalle completo.
