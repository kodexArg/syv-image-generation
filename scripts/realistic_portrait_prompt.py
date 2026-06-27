#!/usr/bin/env python3
"""Realistic artistic combat portrait prompt builder for SyV character testing.

Reuses mappings from portrait_prompt where possible. Produces prompts suitable
for photoreal + artistic renders with canon-accurate uniforms, limited tech/gadgets,
strong adherence to syv-docs visual and lore (olive drab/celeste for confederacion,
red for ejercito_rojo, religious-military, gritty believable soldiers useful in combat).

Style goal: realistic faces/bodies, artistic cinematic lighting, subtle retro-futuristic
(low-tech analog, sanctified items, no high sci-fi), combat practical gear and demeanor.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path
from typing import Any

# Import mappings and helpers from the main creator (single source of truth for subject/role)
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from portrait_prompt import (  # noqa: E402
    _army,
    _map_subject,
    _map_rank,
    _map_especialidad,
    _map_aspectos,
    _map_rasgos,
    _map_vestidura,
    _tags_of,
    _slug,
)

# ---------------------------------------------------------------------------
# Realistic style base prompts (different from poster propaganda)
# ---------------------------------------------------------------------------

REALISTIC_SHARED_POS = (
    "score_9, score_8_up, score_7_up, rating_safe, solo, one person, "
    "photorealistic portrait, highly detailed realistic skin, pores, subtle stubble or weathered lines, "
    "cinematic volumetric lighting, sharp focus, artistic composition, low key dramatic light, "
    "grim Catholic military theocracy atmosphere, believable combat veteran or recruit, "
    "subtle retro-futuristic low-tech details, no modern screens or lasers"
)

REALISTIC_SHARED_NEG = (
    "score_6, score_5, score_4, cartoon, anime, manga, illustration, cel shaded, "
    "3d render plastic, blurry, soft focus, deformed face, mutated hands, extra fingers, "
    "text, caption, logo, watermark, multiple people, crowd, modern sci-fi gadgets, "
    "neon cyberpunk, glowing screens, high-tech armor, clean glossy, beauty retouch"
)

# Army specific realistic clauses (palette + uniform feel + subtle gadgets)
_REALISTIC_ARMY_CLAUSES: dict[str, str] = {
    "confederacion": (
        "olive drab military uniform with celeste blue accents and cream details, warm black leather and brass, "
        "state-issue line uniform, religious insignia or small brass crucifix, "
        "limited tech: analog radio headset or handset, iron sights rifle or subfusil, "
        "tactical vest or assault vest, unit patches, dignified but gritty"
    ),
    "ejercito_rojo": (
        "worn faded red military uniform with black patches and tape repairs, red black and bone cream palette, "
        "revolutionary symbols or faded insignia, scars visible, "
        "makeshift gear, analog binoculars or pistol, underground grit, revolutionary fervor in bearing"
    ),
    "punteros": (
        "worn faded red military uniform with black patches, revolutionary symbols, "
        "street level practical clothes over uniform, red black cream"
    ),
}

# Optional light artistic enhancement
_ARTISTIC_TOUCH = "artistic yet photoreal, subtle painterly detail in shadows and highlights, high fidelity"

# Limited futuristic gadget flavor (respect anatema + canon)
_GADGET_CLAUSE = "subtle low-tech gadgets only: worn analog comms, mechanical iron rifle, sanctified relic badge or ribbon, canvas webbing"

# Engine defaults (same res/seed logic as main for comparability)
WIDTH = 832
HEIGHT = 1344
STEPS = 28
CFG = 7.0
SAMPLER = "dpmpp_2m"
SCHEDULER = "karras"
DENOISE = 1.0

# Pony needs different emphasis and clip skip often
PONY_MODEL_HINTS = ("pony",)

def _deterministic_seed(slug: str) -> int:
    digest = hashlib.sha256(slug.encode()).digest()
    return int.from_bytes(digest[:4], "big") & 0x7FFFFFFF

def _is_pony(model: str) -> bool:
    m = (model or "").lower()
    return any(h in m for h in PONY_MODEL_HINTS)

def _build_subject_block(record: dict[str, Any]) -> str:
    """Reuse mappings to get consistent description."""
    subject = _map_subject(record)
    rank = _map_rank(record)
    especialidad = _map_especialidad(record)
    aspectos = _map_aspectos(record)
    rasgos = _map_rasgos(record)
    vestidura = _map_vestidura(record)

    parts = [subject, rank]
    if especialidad:
        parts.append(especialidad)
    if vestidura:
        parts.append(vestidura)
    parts.extend(aspectos)
    parts.extend(rasgos)
    return ", ".join([p for p in parts if p])

def build_realistic_prompt(
    record: dict[str, Any],
    model: str = "zavyfantasiaxlPDXL_v20.safetensors",
    artistic: bool = True,
) -> dict[str, Any]:
    """Build a realistic portrait job dict.

    Returns same shape as portrait_prompt.build_prompt for compatibility with generators.
    """
    slug = record.get("slug", "unknown")
    army = _army(record)
    nombre = record.get("nombre", slug)

    army_clause = _REALISTIC_ARMY_CLAUSES.get(army, _REALISTIC_ARMY_CLAUSES["confederacion"])

    subject_block = _build_subject_block(record)

    # Model specific prefix
    if _is_pony(model):
        # Pony likes source_pony + detailed descriptors + scores already in base
        model_prefix = "source_pony, rating_safe, "
    else:
        model_prefix = ""

    pos_parts = [
        REALISTIC_SHARED_POS,
        model_prefix + army_clause,
        subject_block,
        _GADGET_CLAUSE,
    ]
    if artistic:
        pos_parts.append(_ARTISTIC_TOUCH)

    positive = ", ".join([p for p in pos_parts if p])

    # For pony we can be a bit more tolerant in neg or keep strict
    negative = REALISTIC_SHARED_NEG

    seed = _deterministic_seed(slug)

    return {
        "slug": slug,
        "nombre": nombre,
        "army": army,
        "positive": positive,
        "negative": negative,
        "width": WIDTH,
        "height": HEIGHT,
        "seed": seed,
        "filename_prefix": f"syv_realistic_{slug}",
        "model": model,
        "steps": 4 if "lightning" in model.lower() and "4step" in model.lower() else (8 if "lightning" in model.lower() else STEPS),
        "cfg": 1.5 if "lightning" in model.lower() else CFG,  # lightning typical low cfg
        "sampler": "dpmpp_sde" if "lightning" in model.lower() else SAMPLER,
        "scheduler": "karras",
        "denoise": DENOISE,
        "style": "realistic",
    }


if __name__ == "__main__":
    # Quick self test with a mock record
    mock = {
        "slug": "test-sargento",
        "nombre": "Test Sargento",
        "tags": ["lealtad/confederacion", "rango/sargento", "especialidad/combate/lider", "equipo/vestidura/uniforme_linea"],
        "edad": 40,
        "genero": "m",
        "atributos": {"cuerpo": 5, "mente": 5, "alma": 5},
        "aspectos": ["veterano"],
        "rasgos": [],
    }
    job = build_realistic_prompt(mock)
    print("SLUG:", job["slug"])
    print("MODEL:", job["model"])
    print("SEED:", job["seed"])
    print("POS[:200]:", job["positive"][:200])
    print("STEPS/CFG:", job["steps"], job["cfg"])