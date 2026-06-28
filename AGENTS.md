# AGENTS.md — `syv-image-prompts`

Punto de partida de la **generación visual de personajes** del universo
*Subordinación y Valor* con **ComfyUI**. Este AGENTS.md manda sobre el de la raíz
`~/Dev/SyV/` cuando trabajás *dentro* de este repo, y **es el cerebro del repo**:
no hay skill externo: la lógica de retrato vive acá.

## Qué es

Fábrica de retratos: leés una ficha de personaje, construís el par de prompts
(positivo + negativo), generás la imagen en ComfyUI y la **entregás al `inbox`**
para que el usuario la rankee. Los ganadores se promueven a `whitelist.md` y
calibran las próximas generaciones. Ese loop es el corazón del repo.

## El ecosistema: a quién servís y qué necesitás

### Te alimenta: `../syv-pj` (crítico)

Los **sujetos a retratar no se inventan acá**: viven en el repo hermano
**`syv-pj`**. Sus **personajes mock** son la materia prima:

- **Ubicación:** `../syv-pj/resources/personajes/*.md` (34 fichas, por facción:
  Fuerzas Armadas/Confederación · Resistencia Subterránea/Ejército Rojo ·
  Iglesia/Inquisición · facciones menores). Índice en `_moc-personajes.md`.
- **Resolución de path** (scripts), en orden:
  1. `$SYV_PJ_PATH/resources/personajes/`
  2. hermano `../syv-pj/resources/personajes/` (default)
  3. `../syv-pj-api/vendor/syv-pj/resources/personajes/`

  Si ninguno existe, no hay a quién retratar: cortá y avisá.

> `syv-pj` es **solo lectura** desde acá: solo se lee como entrada.

### A quién servís: el creador de personajes

Tu servicio es la imagen: el retrato / ficha visual del personaje. Lo consume la
línea del **creador de personajes** (`syv-pj`, `syv-pj-api`, los visualizadores
`syv-pj-frontend` / `syv-pj-flutter`). La **paleta** y el **lore** salen de
`syv-docs` vía la MCP `markdown-vault-syv`.

## Flujo de retrato (el cerebro)

Convierte una ficha en un par de prompts ComfyUI, genera, entrega y aprende.

### Paso 1 — Leer la ficha

Matcheá el input (slug o nombre) contra `../syv-pj/resources/personajes/<slug>.md`.
Si es parcial y único, resolvé; si es ambiguo, listá candidatos y pará. Extraé del
frontmatter + prosa: `nombre`, `genero`, `edad`, `faccion`, `rango`,
`especialidad`, `aspectos`, `rasgos`, `equipo`, `description`, y la prosa narrativa
(minala para detalle visual concreto).

### Paso 2 — Calibrar con `whitelist.md` (SIEMPRE antes de generar)

Leé `prompts/whitelist.md`. Es la memoria de calibración:

- **REFORZAR** — fraseo/descriptores de las entradas en **`## Positivos`**: reusalos.
- **EVITAR** — patrones de **`## Negativos`**: excluilos (al negativo o directamente).

Si está vacío, primera corrida sin calibración.

### Paso 3 — Construir los prompts

**Pesos por atributo** (`atributos`: cuerpo/mente/alma, escala 1-6):
- `cuerpo >= 5` → cuerpo atlético/musculoso, presencia física.
- `mente >= 5` → mirada intensa/enfocada, complexión magra.
- `alma >= 5` → rostro expresivo, peso emocional, luz cálida o atormentada.
- `cuerpo <= 2` → frame liviano. `mente <= 2` → expresión simple.

**Positivo — en este orden:**
```
[SUJETO]    <genero: "1man"/"1woman">, <edad>, oficial/soldado de <faccion>
[ASPECTO]   <rasgos traducidos a visual; aspectos>
[EQUIPO]    <equipo traducido: uniforme, gorra, arma, insignia>
[ESCENA]    <atmósfera SyV: lluvia perpetua, low-tech analógico, hormigón gastado>
[ESTILO]    <propaganda screenprint | realista cinematográfico | pixel-art> + paleta SyV
[CALIDAD]   masterpiece, best quality, sharp focus, film grain (+ score_9, score_8_up… si Pony)
```
Tejé el fraseo REFORZAR del Paso 2.

**Negativo — base + específico de facción/atributo:**
```
[BASE]   lowres, bad anatomy, bad hands, extra digits, text, watermark, signature,
         worst quality, low quality, jpeg artifacts, blurry, cartoon, 3d render
[ESPEC]  <genero opuesto> · <si pixel-art: photo, photorealistic, smooth, gradient>
         <patrones del bucket EVITAR>
```

**Paleta SyV (obligatoria):** olive drab `#7B8A4E` · celeste `#8FB8D6` ·
crema `#F3EEE4` · negro cálido `#0C0B09`. Confirmá contra `syv-docs/` /
`syv-design-system/` antes de fijar una serie. **No inventes canon acá.**

### Paso 4 — Generar en ComfyUI

Vía el skill `comfyui` (ver abajo). Workflow de `workflows/`, ajustá prompt /
seed / params, generá, verificá el output.

### Paso 5 — Entregar al `inbox`

Cada entrega = una carpeta `prompts/inbox/<AAAAMMDD>-<personaje>-<estilo>/` con:
- **`preview.png`** — la imagen generada con esos params.
- **`entry.md`** — prompt (positivo + negativo) + metadatos (personaje, facción,
  estilo, checkpoint, sampler, scheduler, steps, cfg, seed, resolución, workflow)
  + bloque de evaluación vacío para el usuario:
  ```yaml
  rating: null      # 1-5 — lo llena el usuario
  liked: ""
  disliked: ""
  ```

### Paso 6 — Promover a `whitelist.md`

Cuando encontrés un `entry.md` ya rankeado por el usuario, actualizá
`prompts/whitelist.md` (idempotente, sin duplicar) con un wikilink Obsidian:
- `rating >= 4` → bajo `## Positivos`.
- `rating <= 2` → bajo `## Negativos`.

Eso cierra el loop: la próxima generación (Paso 2) lee esto y mejora.

## ComfyUI — vía única

Para cualquier tarea de ComfyUI (start/stop/status, cargar workflow, generar,
cola, modelos, exportar imágenes) **usá el skill `comfyui`**. No hardcodees rutas.

- Root en esta máquina: `/home/kodex/ComfyUI` · output: `/home/kodex/ComfyUI/output`
- Las imágenes nacen ahí; el bulk crudo se importa a `images/raw/` con
  `scripts/export.py` (scratch gitignored). La entrega curada de cada retrato va
  a `prompts/inbox/<slug>/preview.png`.

## Visibilidad y trabajo público (REGLA OBLIGATORIA)

**ALWAYS show what you're seeing** y **work public**:

- Cuando el usuario pide control visible o "ver lo que yo veo", operá vía el
  browser visible (debug Chromium con remote-debugging) y **chrome-devtools**:
  - `take_snapshot` (a11y tree con uids) + `evaluate_script` para leer prompts,
    widgets, errores, queue y nodos.
  - `take_screenshot` + `read_file` en las imágenes generadas para confirmar
    visualmente lo que se ve.
- Nunca trabajo "invisible" o solo-API sin cross-verificar contra la UI abierta.
- Después de cada generación: snapshot + screenshot + leer la imagen y reportarlo.
- **Work public:** todo a la vista. Entregá al `inbox` inmediatamente, mostrá
  previews. El usuario debe poder ver/reproducir exactamente lo que hiciste.

## Reglas del repo

1. **`prompts/inbox/` es el registro de cada generación** (reemplaza al viejo
   `docs/tests/`). Sin `entry.md` + `preview.png`, la generación no existe.
   La curación vive en `prompts/whitelist.md`, no en una carpeta de imágenes.
2. **Imágenes:** el bulk crudo de ComfyUI va a `images/raw/` y **no se versiona**
   (`.gitignore`). Las previews curadas se commitean dentro de `prompts/inbox/`.
3. **Workflows** versionados en `workflows/`: el `.json` (UI) y el `_api.json` (API).
4. **Canon:** lugares, personajes, facciones y **paleta** salen de `syv-docs/`
   vía la MCP `markdown-vault-syv`. Este repo no escribe en la SSOT.
5. **Python > Bash**, `uv` para paquetes. Scripts con shebang.
6. **`docs/`** queda solo para guías de referencia (`comfyui-setup.md`,
   `workflow.md`), no para registrar generaciones.

## Input para entrenamiento de LoRAs SyV

El input para entrenar un LoRA de SyV es un dataset de pares imagen + caption
(80-150 imágenes para un primer LoRA de estilo viable sobre base SDXL/Pony).

- Imágenes: de los 34 personajes mock de `../syv-pj/resources/personajes/*.md`.
- Prompts: el Flujo de retrato de arriba (estilos propaganda screenprint y
  realista cinematográfico). Checkpoint base: `zavyfantasiaxlPDXL_v20.safetensors`.
- Cada imagen lleva un `.txt` con el caption: trigger word + descriptores del
  sujeto (edad, complexión, expresión, rasgos), facción, rango, especialidad,
  vestidura, equipo, paleta SyV y atmósfera (theocracia militar católica, lluvia
  perpetua, low-tech analógico, uniformes gastados). Tags de calidad del modelo
  base (score_9, score_8_up… para Pony) cuando aplique.
- Estructura para trainers (Kohya_ss / OneTrainer):
  ```
  training/<nombre-lora>/dataset/<repeats>_<trigger>/<nombre>.png + <nombre>.txt
  ```
- Las imágenes se generan en ComfyUI, se importan a `images/raw/` y se curan al
  dataset. La diversidad cubre facciones (Confederación, Ejército Rojo,
  Inquisición), rangos, especialidades, tomas (close-up / medio cuerpo) e
  iluminación.
