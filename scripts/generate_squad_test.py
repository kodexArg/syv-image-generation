#!/usr/bin/env python3
"""
Generate realistic artistic combat-useful character portraits for SyV testing.

Creates a "full squad" proposal:
- Complete Confederación Argentina squad (Sargento -> Colimba)
- At least one of each class for Ejército Rojo (via lealtad/ejercito_rojo)
- 4 old retired veterans (some still somewhat active)
- 8-10 clear-trade interesting personalities (support/combat useful)

First produces markdown proposal (with full prompts) + JSON of all jobs.
Then can --run against ComfyUI using same seed per character across models.

Models combos (important ones installed):
1. ponyDiffusionV6XL_v6StartWithThisOne.safetensors (detailed characters)
2. zavyfantasiaxlPDXL_v20.safetensors (artistic base)
3. sdxl_lightning_4step.safetensors (fast)
4. sdxl_lightning_8step.safetensors (fast balanced)

Style strictly follows syv-docs canon (read via MCP + files): olive drab + celeste + crema for FA/Conf,
red worn for Rojo, limited tech, religious-military flavor, gritty believable fighters.

Docs SSOT: every run ends in docs/tests/...

Usage:
  uv run scripts/generate_squad_test.py --dry-run
  uv run scripts/generate_squad_test.py --run
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = REPO_ROOT / "build"
DOCS_TESTS = REPO_ROOT / "docs" / "tests"
COMFYUI_API = "http://127.0.0.1:8188"
POLL_INTERVAL = 2.0
POLL_TIMEOUT = 400.0

# Models we care about for comparison (same seed)
MODELS = [
    "ponyDiffusionV6XL_v6StartWithThisOne.safetensors",
    "zavyfantasiaxlPDXL_v20.safetensors",
    "sdxl_lightning_4step.safetensors",
    "sdxl_lightning_8step.safetensors",
]

# ---------------------------------------------------------------------------
# Path helpers (reuse from generate_portraits)
# ---------------------------------------------------------------------------

_CANDIDATE_ROOTS = [
    Path(__import__("os").environ.get("SYV_PJ_PATH", "")) if __import__("os").environ.get("SYV_PJ_PATH") else None,
    REPO_ROOT.parent / "syv-pj",
    REPO_ROOT.parent / "syv-pj-api" / "vendor" / "syv-pj",
]

def find_personajes_dir() -> Path:
    for root in _CANDIDATE_ROOTS:
        if root is None:
            continue
        candidate = root / "resources" / "personajes"
        if candidate.is_dir():
            return candidate
    sys.exit("ERROR: No syv-pj personajes dir found.")

# ---------------------------------------------------------------------------
# Load real records (stdlib parser copy minimal)
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip()
    return _parse_yaml_block(block.splitlines(), 0)[0]

def _parse_yaml_block(lines: list[str], indent: int) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        current_indent = len(line) - len(stripped)
        if current_indent < indent:
            break
        if ":" in stripped:
            colon = stripped.index(":")
            key = stripped[:colon].strip()
            rest = stripped[colon + 1:].strip()
            if rest == "" or rest == "|" or rest == ">":
                i += 1
                if i < len(lines):
                    next_stripped = lines[i].lstrip()
                    next_indent = len(lines[i]) - len(next_stripped)
                    if next_stripped.startswith("- "):
                        items = []
                        while i < len(lines):
                            ls = lines[i].lstrip()
                            if not ls.startswith("- "):
                                break
                            item_val = ls[2:].strip()
                            if (item_val.startswith('"') and item_val.endswith('"')) or (item_val.startswith("'") and item_val.endswith("'")):
                                item_val = item_val[1:-1]
                            items.append(item_val)
                            i += 1
                        result[key] = items
                        continue
                    elif next_indent > current_indent:
                        sub, consumed = _parse_yaml_block(lines[i:], next_indent)
                        result[key] = sub
                        i += consumed
                        continue
                    else:
                        result[key] = None
                        continue
                else:
                    result[key] = None
                    continue
            else:
                val: Any = rest
                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                if val == "null" or val == "~":
                    val = None
                elif val == "true":
                    val = True
                elif val == "false":
                    val = False
                else:
                    try:
                        val = int(val)
                    except ValueError:
                        try:
                            val = float(val)
                        except ValueError:
                            pass
                result[key] = val
                i += 1
                continue
        else:
            i += 1
            continue
    return result, i

def load_records(personajes_dir: Path, slugs: list[str]) -> list[dict[str, Any]]:
    records = []
    for md_file in sorted(personajes_dir.glob("*.md")):
        if md_file.name.startswith("_"):
            continue
        if slugs and md_file.stem not in slugs:
            continue
        text = md_file.read_text(encoding="utf-8")
        fm = _parse_frontmatter(text)
        if fm:
            records.append(fm)
    return records

# ---------------------------------------------------------------------------
# Proposal characters (additional to fill squad / retirees / oficios)
# These are "propuesta" for the test only. Not written to syv-pj.
# ---------------------------------------------------------------------------

PROPOSAL_RECORDS: list[dict[str, Any]] = [
    # --- Additional Colimbas / Reclutas for complete Conf squad ---
    {
        "slug": "julio-mendez-colimba",
        "nombre": "Julio Méndez",
        "tags": ["lealtad/confederacion", "rango/recluta", "especialidad/combate/fusilero", "equipo/vestidura/uniforme_linea", "aspecto/veterano"],  # young but learning
        "edad": 19,
        "genero": "m",
        "atributos": {"cuerpo": 3, "mente": 4, "alma": 3},
        "aspectos": ["instinto"],
        "rasgos": ["mirada_cansada"],
        "faccion": "fuerzas_armadas",
    },
    {
        "slug": "laura-vazquez-colimba",
        "nombre": "Laura Vázquez",
        "tags": ["lealtad/confederacion", "rango/recluta", "especialidad/oficio/radio", "equipo/vestidura/uniforme_linea"],
        "edad": 20,
        "genero": "f",
        "atributos": {"cuerpo": 3, "mente": 6, "alma": 4},
        "aspectos": ["tactico"],
        "rasgos": [],
        "faccion": "fuerzas_armadas",
    },
    # --- More to complete squad roles ---
    {
        "slug": "carlos-ramirez-medico",
        "nombre": "Carlos Ramírez",
        "tags": ["lealtad/confederacion", "rango/soldado_linea", "especialidad/oficio/medico", "equipo/vestidura/uniforme_linea", "equipo/vestidura/chaleco"],
        "edad": 31,
        "genero": "m",
        "atributos": {"cuerpo": 4, "mente": 5, "alma": 5},
        "aspectos": ["veterano"],
        "rasgos": ["mirada_cansada"],
        "faccion": "fuerzas_armadas",
    },
    # --- Ejército Rojo one-per-class fills ---
    {
        "slug": "ezequiel-fusilero-rojo",
        "nombre": "Ezequiel 'El Zurdo' Medina",
        "tags": ["lealtad/ejercito_rojo", "rango/militante_resistencia", "especialidad/combate/fusilero", "equipo/vestidura/uniforme_rojo"],
        "edad": 27,
        "genero": "m",
        "atributos": {"cuerpo": 5, "mente": 4, "alma": 5},
        "aspectos": ["instinto", "vanguardia"],
        "rasgos": ["cicatriz_perturbadora"],
        "faccion": "resistencia_subterranea",
    },
    {
        "slug": "rosa-tiradora-roja",
        "nombre": "Rosa 'La Gata' Quiroga",
        "tags": ["lealtad/ejercito_rojo", "rango/militante_resistencia", "especialidad/combate/tirador", "equipo/vestidura/uniforme_tactico_rojo"],
        "edad": 34,
        "genero": "f",
        "atributos": {"cuerpo": 3, "mente": 6, "alma": 5},
        "aspectos": ["ojo_de_aguila", "terco"],
        "rasgos": ["tatuaje_de_unidad"],
        "faccion": "resistencia_subterranea",
    },
    # --- 4 Viejos jubilados (some active) ---
    {
        "slug": "antonio-rios-veterano-jubilado",
        "nombre": "Antonio Ríos 'El Viejo'",
        "tags": ["lealtad/confederacion", "rango/sargento", "especialidad/combate/lider", "equipo/vestidura/uniforme_linea"],
        "edad": 68,
        "genero": "m",
        "atributos": {"cuerpo": 3, "mente": 6, "alma": 5},
        "aspectos": ["veterano", "tactico"],
        "rasgos": ["mirada_cansada", "constitucion_robusta"],
        "faccion": "fuerzas_armadas",
    },
    {
        "slug": "marta-veterana-roja",
        "nombre": "Marta 'La Tuerta' Delgado",
        "tags": ["lealtad/ejercito_rojo", "rango/cabecilla", "especialidad/combate/tirador", "equipo/vestidura/uniforme_rojo"],
        "edad": 64,
        "genero": "f",
        "atributos": {"cuerpo": 3, "mente": 6, "alma": 6},
        "aspectos": ["veterano", "terco"],
        "rasgos": ["cicatriz_perturbadora"],
        "faccion": "resistencia_subterranea",
    },
    {
        "slug": "padre-emilio-capellan-jubilado",
        "nombre": "Padre Emilio Vargas",
        "tags": ["lealtad/confederacion", "rango/capellan", "especialidad/oficio/medico", "equipo/vestidura/sotana"],
        "edad": 67,
        "genero": "m",
        "atributos": {"cuerpo": 3, "mente": 5, "alma": 6},
        "aspectos": ["religioso", "veterano"],
        "rasgos": ["fe_obstinada"],
        "faccion": "fuerzas_armadas",
    },
    {
        "slug": "jorge-mecanico-viejo",
        "nombre": "Jorge 'El Tuercas' Sosa",
        "tags": ["lealtad/ejercito_rojo", "rango/militante_resistencia", "especialidad/oficio/mecanico", "equipo/vestidura/chaqueta_de_cuero"],
        "edad": 59,
        "genero": "m",
        "atributos": {"cuerpo": 4, "mente": 5, "alma": 4},
        "aspectos": ["manos_asperas", "instinto_de_supervivencia"],
        "rasgos": [],
        "faccion": "resistencia_subterranea",
    },
    # --- 10 oficios claros + personalidades interesantes (combat / unit useful) ---
    {
        "slug": "carlos-armero",
        "nombre": "Carlos 'El Cerrajero' Ibáñez",
        "tags": ["lealtad/confederacion", "rango/soldado_linea", "especialidad/oficio/armero", "equipo/vestidura/delantal_manchado", "equipo/vestidura/uniforme_linea"],
        "edad": 44,
        "genero": "m",
        "atributos": {"cuerpo": 4, "mente": 5, "alma": 4},
        "aspectos": ["manos_asperas", "tactico"],
        "rasgos": ["mirada_cansada"],
        "faccion": "fuerzas_armadas",
    },
    {
        "slug": "sara-radio",
        "nombre": "Sara 'La Voz' Molina",
        "tags": ["lealtad/confederacion", "rango/soldado_linea", "especialidad/oficio/radio", "equipo/vestidura/uniforme_linea"],
        "edad": 29,
        "genero": "f",
        "atributos": {"cuerpo": 3, "mente": 6, "alma": 5},
        "aspectos": ["tactico"],
        "rasgos": [],
        "faccion": "fuerzas_armadas",
    },
    {
        "slug": "tito-raciones",
        "nombre": "Tito 'El Cuchara' Benítez",
        "tags": ["lealtad/confederacion", "rango/soldado_linea", "especialidad/oficio/cocinero", "equipo/vestidura/delantal_manchado"],
        "edad": 38,
        "genero": "m",
        "atributos": {"cuerpo": 5, "mente": 4, "alma": 5},
        "aspectos": ["instinto_de_supervivencia"],
        "rasgos": [],
        "faccion": "fuerzas_armadas",
    },
    {
        "slug": "raul-ingeniero",
        "nombre": "Raúl 'Puentes' Ortega",
        "tags": ["lealtad/ejercito_rojo", "rango/militante_resistencia", "especialidad/combate/zapador", "equipo/vestidura/uniforme_tactico_rojo"],
        "edad": 36,
        "genero": "m",
        "atributos": {"cuerpo": 4, "mente": 6, "alma": 4},
        "aspectos": ["tactico"],
        "rasgos": ["manos_asperas"],
        "faccion": "resistencia_subterranea",
    },
    {
        "slug": "el-chango-conductor",
        "nombre": "Diego 'El Chango' Navarro",
        "tags": ["lealtad/confederacion", "rango/soldado_linea", "especialidad/oficio/conductor", "equipo/vestidura/uniforme_linea"],
        "edad": 32,
        "genero": "m",
        "atributos": {"cuerpo": 4, "mente": 5, "alma": 3},
        "aspectos": ["instinto"],
        "rasgos": [],
        "faccion": "fuerzas_armadas",
    },
    {
        "slug": "el-aguila-scout",
        "nombre": "Emiliano 'El Águila' Soto",
        "tags": ["lealtad/ejercito_rojo", "rango/militante_resistencia", "especialidad/combate/tirador", "equipo/vestidura/uniforme_rojo"],
        "edad": 25,
        "genero": "m",
        "atributos": {"cuerpo": 3, "mente": 5, "alma": 4},
        "aspectos": ["ojo_de_aguila", "instinto"],
        "rasgos": [],
        "faccion": "resistencia_subterranea",
    },
    {
        "slug": "hermana-cura",
        "nombre": "Hermana Ana 'La Cura' Paredes",
        "tags": ["lealtad/confederacion", "rango/sacerdote", "especialidad/oficio/medico", "equipo/vestidura/sotana"],
        "edad": 41,
        "genero": "f",
        "atributos": {"cuerpo": 3, "mente": 5, "alma": 6},
        "aspectos": ["religioso"],
        "rasgos": ["silencio_sagrado"],
        "faccion": "fuerzas_armadas",
    },
    {
        "slug": "el-soldador",
        "nombre": "Roberto 'Chispas' Aguirre",
        "tags": ["lealtad/ejercito_rojo", "rango/militante_resistencia", "especialidad/oficio/mecanico", "equipo/vestidura/chaqueta_de_cuero"],
        "edad": 47,
        "genero": "m",
        "atributos": {"cuerpo": 5, "mente": 4, "alma": 4},
        "aspectos": ["manos_asperas"],
        "rasgos": [],
        "faccion": "resistencia_subterranea",
    },
    {
        "slug": "el-cronista",
        "nombre": "Mateo 'El Cronista' López",
        "tags": ["lealtad/confederacion", "rango/soldado_linea", "especialidad/investigacion/espia", "equipo/vestidura/uniforme_gris_dns"],
        "edad": 35,
        "genero": "m",
        "atributos": {"cuerpo": 3, "mente": 6, "alma": 5},
        "aspectos": ["tactico"],
        "rasgos": ["paranoia_vigilancia"],
        "faccion": "fuerzas_armadas",
    },
]

# Selected real slugs we want to include (core squad + rojo examples)
REAL_SLUGS_CONF = [
    "ovidio-gauna-sargento",
    "ruben-ferreyra-cabo",
    "elian-quiroga-fusilero",
    "marcos-paez-fusilero",
    "facundo-rios-tirador",
    "hernan-bordon-asalto",
    "lucas-veron-medico",
    "tomas-aguirre-recluta",
]

REAL_SLUGS_ROJO = [
    "anibal-painemal-comandante",
    "ezequiel-madariaga-camarada",
    "valentina-roca-camarada",
    "ivan-leiva-asalto",
    "gaston-brizuela-zapador",
]

def build_all_jobs() -> list[dict[str, Any]]:
    """Build full matrix of jobs: all selected characters x all models."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from realistic_portrait_prompt import build_realistic_prompt  # noqa: E402

    personajes_dir = find_personajes_dir()
    real_conf = load_records(personajes_dir, REAL_SLUGS_CONF)
    real_rojo = load_records(personajes_dir, REAL_SLUGS_ROJO)

    base_records = real_conf + real_rojo + PROPOSAL_RECORDS

    jobs: list[dict[str, Any]] = []
    for rec in base_records:
        for model in MODELS:
            job = build_realistic_prompt(rec, model=model)
            # Ensure consistent filename across runs
            job["filename_prefix"] = f"syv_real_{job['slug']}_{model.split('.')[0][:12]}"
            jobs.append(job)
    return jobs

def write_proposal_md(jobs: list[dict[str, Any]], out_path: Path) -> None:
    """Write human proposal markdown listing every character + prompt (one per slug, note combos)."""
    DOCS_TESTS.mkdir(parents=True, exist_ok=True)
    # Group by slug
    by_slug: dict[str, list[dict]] = {}
    for j in jobs:
        by_slug.setdefault(j["slug"], []).append(j)

    lines = []
    lines.append("# Propuesta — Gran Escuadra Realista de Combate (SyV)")
    lines.append("")
    lines.append(f"- **Fecha:** 2026-06-27")
    lines.append(f"- **Objetivo:** Probar creador de personaje múltiples veces con retratos creíbles, realistas, útiles para combate.")
    lines.append(f"- **Canon:** Facciones, uniformes y paleta de `syv-docs` (Fuerzas Armadas / Resistencia Subterránea / Ejército Rojo). Paleta: olive drab #7B8A4E + celeste #8FB8D6 + crema #F3EEE4 + negro cálido #0C0B09. Estilo: realista artístico + gadgets low-tech retro-futuristas limitados (respeta Anatema Mecánico).")
    lines.append(f"- **Total personajes:** {len(by_slug)}")
    lines.append(f"- **Modelos por personaje (mismo seed):** {', '.join(MODELS)}")
    lines.append("")
    lines.append("## Personajes")
    lines.append("")

    # Order: conf squad first, then rojo, retired, oficios (rough)
    order = list(by_slug.keys())
    for slug in order:
        js = by_slug[slug]
        j0 = js[0]
        lines.append(f"### {j0['nombre']} (`{slug}`)")
        lines.append(f"- **Ejército / Lealtad:** {j0['army']}")
        lines.append(f"- **Seed (común):** {j0['seed']}")
        lines.append(f"- **Resolución:** {j0['width']}x{j0['height']}")
        lines.append("")
        lines.append("**Prompt positivo (base, se adapta ligeramente por modelo):**")
        lines.append("```")
        lines.append(j0["positive"])
        lines.append("```")
        lines.append("")
        lines.append("**Negativo:**")
        lines.append("```")
        lines.append(j0["negative"])
        lines.append("```")
        lines.append("")
        lines.append("**Variantes generadas (mismo seed):**")
        for j in js:
            lines.append(f"- {j['model']} → `{j['filename_prefix']}` (steps={j['steps']}, cfg={j['cfg']}, sampler={j['sampler']})")
        lines.append("")
        lines.append("---")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Proposal written: {out_path}")

def write_jobs_json(jobs: list[dict[str, Any]], out_path: Path) -> None:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(jobs, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Jobs JSON: {out_path} ({len(jobs)} total)")

def build_simple_workflow(job: dict[str, Any]) -> dict[str, Any]:
    """Minimal SDXL txt2img. For pony we still use it (prompt carries the pony scores)."""
    # For lightning we use low steps + specific sampler already in job.
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": job["model"]}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["1", 1], "text": job["positive"]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["1", 1], "text": job["negative"]}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": job["width"], "height": job["height"], "batch_size": 1}},
        "5": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["1", 0],
                "positive": ["2", 0],
                "negative": ["3", 0],
                "latent_image": ["4", 0],
                "seed": job["seed"],
                "steps": job["steps"],
                "cfg": job["cfg"],
                "sampler_name": job["sampler"],
                "scheduler": job["scheduler"],
                "denoise": job["denoise"],
            },
        },
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": job["filename_prefix"]}},
    }

def post_job(job: dict[str, Any]) -> str:
    """Fire and forget a single job. Returns prompt_id."""
    workflow = build_simple_workflow(job)
    payload = json.dumps({"prompt": workflow}).encode("utf-8")
    req = urllib.request.Request(f"{COMFYUI_API}/prompt", data=payload, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    prompt_id = data.get("prompt_id")
    if not prompt_id:
        raise RuntimeError(f"No prompt_id: {data}")
    print(f"  queued {job['slug']} @ {job['model'][:18]}... pid={prompt_id}")
    return prompt_id

def wait_for(prompt_id: str) -> list[str]:
    deadline = time.monotonic() + POLL_TIMEOUT
    while time.monotonic() < deadline:
        time.sleep(POLL_INTERVAL)
        with urllib.request.urlopen(f"{COMFYUI_API}/history/{prompt_id}", timeout=15) as resp:
            hist = json.loads(resp.read())
        if prompt_id in hist:
            outputs = hist[prompt_id].get("outputs", {})
            imgs = []
            for o in outputs.values():
                imgs.extend([im.get("filename") for im in o.get("images", [])])
            return imgs
    return []

def main() -> None:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", default=True)
    mode.add_argument("--run", action="store_false", dest="dry_run")
    ap.add_argument("--out", type=Path, default=BUILD_DIR / "squad_test_jobs.json")
    ap.add_argument("--proposal", type=Path, default=DOCS_TESTS / "20260627-gran-escuadra-realista.md")
    args = ap.parse_args()

    print("Building realistic squad test jobs (conf squad + rojo classes + retirees + oficios)...")
    jobs = build_all_jobs()
    print(f"Total jobs (characters x models): {len(jobs)}")

    write_jobs_json(jobs, args.out)
    write_proposal_md(jobs, args.proposal)

    if not args.dry_run:
        print(f"\nQueueing {len(jobs)} jobs to {COMFYUI_API} (same seed per slug across models)...")
        prompt_ids = []
        for j in jobs:
            try:
                pid = post_job(j)
                prompt_ids.append((j, pid))
            except Exception as e:
                print(f"  ERROR queuing {j['slug']}: {e}", file=sys.stderr)
        print(f"\nAll {len(prompt_ids)} jobs queued. Comfy is processing the queue.")
        print("Run `curl http://127.0.0.1:8188/queue` to watch. When empty, run `uv run scripts/export.py` then the comparison page script.")
        # Optional: if you want to block until done, uncomment:
        # for j, pid in prompt_ids:
        #     imgs = wait_for(pid)
        #     print(f"  {j['slug']}: {imgs}")

if __name__ == "__main__":
    main()