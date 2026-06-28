# syv-image-prompts

Punto de partida de la **generación visual de personajes del universo
*Subordinación y Valor*** usando **ComfyUI**. Leés una ficha de personaje,
construís los prompts, generás la imagen y la entregás al `inbox` para que el
usuario la rankee; los ganadores se promueven a `whitelist.md` y calibran las
próximas generaciones. La lógica completa vive en `AGENTS.md`.

> Es un *playground* del ecosistema SyV. La inspiración (lugares, facciones,
> personajes, paleta) sale de la SSOT `syv-docs/`; las herramientas se
> construyen alrededor de ella.

## Estructura

```
syv-image-prompts/
├── README.md            ← este archivo
├── AGENTS.md            ← el cerebro: flujo de retrato + reglas (CLAUDE.md → symlink)
├── docs/                ← guías de referencia
│   ├── workflow.md      ← cómo correr una generación de punta a punta
│   └── comfyui-setup.md ← root de ComfyUI, output dir, modelos, MCP
├── workflows/           ← workflows ComfyUI versionados (.json + _api.json)
├── prompts/
│   ├── inbox/           ← una carpeta por entrega: entry.md (prompt+metadata) + preview.png
│   └── whitelist.md     ← curación: links Obsidian a los rankeados (Positivos / Negativos)
├── images/
│   └── raw/             ← bulk crudo de ComfyUI (NO versionado, .gitignore)
└── scripts/
    └── export.py        ← copia los últimos PNG de ComfyUI/output → images/raw
```

## Flujo rápido

1. Arrancá ComfyUI (skill `comfyui` / `comfyctl start`).
2. Leé la ficha (`../syv-pj/resources/personajes/`) y `prompts/whitelist.md`.
3. Construí los prompts (ver `AGENTS.md` → Flujo de retrato) y generá.
4. Entregá a `prompts/inbox/<AAAAMMDD>-<personaje>-<estilo>/`: `entry.md` + `preview.png`.
5. El usuario rankea en el `entry.md`; los `>=4` se linkean en `whitelist.md`.

Ver `docs/workflow.md` para el detalle y `AGENTS.md` para la lógica completa.
