# Prueba — Gran Escuadra Realista (Confederación + Ejército Rojo + Jubilados + Oficios)

- **Fecha:** 2026-06-27
- **Slug:** 20260627-gran-escuadra-realista
- **Objetivo:** Probar el creador de personaje (portrait_prompt + extensión realista) múltiples veces con personajes creíbles, realistas, útiles para combate. Cubrir escuadra completa Confederación (Sargento a Colimba), al menos uno de cada clase del Ejército Rojo, 4 viejos jubilados (algunos activos), y ~10 oficios claros con personalidades interesantes.
- **Entidad SyV / referencia de canon:** `[[fuerzas-armadas]]`, `[[resistencia-subterranea]]`, `[[1_trasfondo/codex/anatema-mecanico]]`, `[[2_atlas/notas-sobre-arte-en-confederacion]]`, paleta y vestimenta de syv-docs + syv-design-system. No se inventa canon; se lee obligatoriamente.

## Resumen de la serie

Se definieron ~31 personajes (selección de existentes en syv-pj + propuestas para completar gaps).

Estilo pedido: **realista + artístico**, con gadgets futuristas **hasta cierto punto** (low-tech, analógico, relics santificados, respeta Anatema Mecánico). Fuerte seguimiento a paleta (olive drab #7B8A4E + celeste #8FB8D6 + crema #F3EEE4 + negro cálido #0C0B09), uniformes (uniforme_linea para Conf, uniforme_rojo para Rojo), insignias, rol de combate realista.

Se generó con **mismo seed por personaje** a través de **4 combinaciones importantes de modelos** instalados:
- ponyDiffusionV6XL_v6StartWithThisOne.safetensors
- zavyfantasiaxlPDXL_v20.safetensors
- sdxl_lightning_4step.safetensors
- sdxl_lightning_8step.safetensors

Total: 124 imágenes.

## Herramientas / scripts usados

- `scripts/realistic_portrait_prompt.py` (nuevo): builder realista que reutiliza mappings del creador principal (`portrait_prompt.py`).
- `scripts/generate_squad_test.py`: construye la lista completa (carga reales + propuestas), genera jobs por modelo, escribe JSON + propuesta markdown.
- ComfyUI API directa (sin UI) — cola masiva.
- `scripts/export.py` para traer crudos a `images/raw/`.
- `scripts/generate_comparison_page.py`: genera la página de comparación.

## Parámetros comunes

| Campo | Valor |
|---|---|
| Resolución | 832x1344 (portrait vertical) |
| Seed | Determinístico por slug (sha256 lower 32) — idéntico en los 4 modelos |
| Workflow base | 7-node SDXL txt2img (adaptado por modelo: pony prompt + lightning steps/cfg/sampler) |
| Estilo base | photoreal + artistic cinematic, low-tech gadgets, canon uniforms + demeanor |

Prompt positivo y negativo completos por personaje están en la **propuesta** generada automáticamente (ver abajo).

## Propuesta completa + prompts

Ver: [docs/tests/20260627-gran-escuadra-realista-prompts.md](20260627-gran-escuadra-realista-prompts.md) (generada por el script: lista cada personaje con prompt positivo/negativo literal completo + variantes por modelo).

El JSON `build/squad_test_jobs.json` contiene todos los jobs listos para reproducción exacta.

El archivo `build/squad_test_jobs.json` contiene todos los jobs listos para reproducción.

## Página de comparación

Generada: `docs/comparisons/20260627-squad-realistic-comparison.html`

- Grid 4 columnas por personaje (Pony / Zavy / Lightning 4 / Lightning 8)
- Mismo seed
- Colores del design system SyV (ink/cream/green/celeste)
- Imágenes referencian `../../images/raw/syv_real_...` (correr export.py después de que la cola termine)

## Resultados (a completar cuando termine la cola)

**Estado al momento de documentar:** 124 jobs encolados exitosamente. Comfy procesando la cola en background (sin pausa). 

Ejecutar cuando la cola esté vacía:
```bash
curl http://127.0.0.1:8188/queue
uv run scripts/export.py
python3 scripts/generate_comparison_page.py
```

Luego mover las mejores a `images/seleccionadas/` + `git add -f`.

## Conclusiones (preliminares)

- El creador de personaje (mappings de rango/especialidad/aspectos/rasgos/vestidura) se reutilizó exitosamente para un estilo completamente distinto (realista vs propaganda poster).
- Los personajes propuestos son creíbles y útiles en combate: roles de escuadra (líder, fusilero, asalto, tirador, zapador, medico, radio, armero, etc.) + personalidades variadas (terco, religioso, veterano cansado, idealista joven, pragmático).
- Cumplimiento canon: paleta, uniformes (linea vs rojo), insignias, gadgets limitados (radio analógica, sights de hierro, relics), atmósfera grim teocrática militar / fervor revolucionario.
- Modelos elegidos cubren velocidad (lightning) y calidad de personajes (pony + zavy).
- Próximos: 
  - Evaluar consistencia de cara/edad/uniforme a través de modelos (mismo seed ayuda).
  - Posible LoRA Niji semi-realism como 5ta variante.
  - Ajustes finos de prompt por modelo (pony vs SDXL).
  - Agregar más colimbas o un segundo médico si la escuadra se usa en juego.

## Archivos clave generados

- `docs/tests/20260627-gran-escuadra-realista.md` (esta nota)
- `build/squad_test_jobs.json`
- `docs/comparisons/20260627-squad-realistic-comparison.html`
- `images/raw/syv_real_*` (después de export)
- `scripts/realistic_portrait_prompt.py` (extensión reutilizable del creador)

Sin nota documentada la prueba no existe — aquí está.