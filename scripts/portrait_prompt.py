#!/usr/bin/env python3
"""Build a ComfyUI propaganda-poster prompt from a syv-pj soldier record.

Pure function — no network or ComfyUI dependencies. Import or call directly.

Mapping catalog
---------------
ARMY (lealtad/* tag)
  lealtad/confederacion  → Confederación palette + golden halo + crucifix
  lealtad/ejercito_rojo  → woodcut linocut texture + red + revolutionary fervor
  lealtad/punteros       → treated as ejercito_rojo (allied faction)

SUBJECT (edad + genero + atributos)
  edad + genero          → "a NN year old man/woman"
  cuerpo 2-3             → lean wiry
  cuerpo 4-5             → athletic build
  cuerpo 6-7             → broad barrel-chested
  mente 2-3              → tired glazed eyes
  mente 4-5              → alert focused eyes
  mente 6-7              → sharp piercing eyes
  alma 2-3               → withdrawn hollow presence
  alma 4-5               → composed steady demeanor
  alma 6-7               → commanding iron gaze straight spine

RANK (rango tag)
  recluta / simpatizante → young plain
  soldado_linea / militante_resistencia / marinero → enlisted chevrons
  cabo                   → NCO corporal chevrons
  sargento               → NCO sergeant stripes
  cabecilla / lider      → commander stance
  novicio                → inquisitor crusader initiate
  inquisidor             → inquisitor crusader officer
  sacerdote / capellan   → clergy bearing

ESPECIALIDAD (especialidad/* tag)
  combate/fusilero       → rifle shouldered, infantry stance
  combate/asalto         → assault vest, breach-ready stance
  combate/tirador        → scoped marksman rifle, steady aim
  combate/zapador        → sapper, explosives rigging
  combate/lider          → commander posture, baton or radio
  combate/cruzado        → consecrated sword, crusader iconography
  investigacion/espia    → covert plain clothes, collar turned up
  investigacion/interrogador → cold cruel expression, gloved hands
  oficio/medico          → red-cross medic kit, field dressing
  oficio/*               → occupation visible in bearing (default)
  paranormal/*           → ritual bearing, mystical aura (skipped for poster style)

ASPECTOS (aspecto/* tags)
  veterano               → weathered calm face, visible scars
  terco                  → stubborn set jaw, locked gaze
  religioso              → serene expression, crucifix visible
  cobarde                → hunched shoulders, darting eyes
  ojo_de_aguila          → piercing eagle gaze
  tirador                → steady aim, measured stance
  tactico                → focused tactical bearing
  vanguardia             → aggressive forward lean
  instinto               → alert tense posture
  instinto_de_supervivencia → alert tense posture
  manos_asperas          → rough calloused hands visible
  manos_temblorosas      → tense shaking hands
  expresion_trance       → vacant trance gaze
  rodilla_vencida        → stoic bearing despite injury

RASGOS (rasgo/* tags)
  cicatriz_perturbadora  → disturbing facial scar, battle damage
  tatuaje_de_unidad      → unit tattoo on neck
  mirada_cansada         → heavy-lidded tired eyes, fatigue lines
  constitucion_robusta   → robust powerful build, broad frame
  fe_obstinada           → iron devotion in bearing
  duda_teologica         → slight uncertainty in eyes
  paranoia_vigilancia    → hypervigilant darting gaze
  silencio_sagrado       → eerie composed silence
  afinidad_animal        → (no visual mapping)
  trance_psiquico        → unfocused distant gaze

VESTIDURA (equipo/vestidura/* tags)
  uniforme_rojo          → worn red military uniform
  uniforme_linea         → olive drab military uniform, state-issue
  uniforme_tactico_rojo  → red tactical uniform
  uniforme_gris_dns      → grey uniform
  chaleco / chaleco_asalto → tactical assault vest
  sotana                 → long dark cassock
  habito                 → monastic habit
  galera                 → formal fedora hat
  capucha                → hood obscuring face
  chaqueta_de_cuero      → worn leather jacket
"""

from __future__ import annotations

import hashlib
import re
from typing import Any

# ---------------------------------------------------------------------------
# Shared base prompts (locked style — do not edit)
# ---------------------------------------------------------------------------

SHARED_POS = (
    "score_9, score_8_up, score_7_up, rating_safe, solo, one person, "
    "(vintage screenprint propaganda poster:1.3), Shepard Fairey OBEY style, "
    "riso print, (limited color palette:1.2), flat bold shapes, "
    "(heavy halftone grain:1.2), distressed ink texture, retro lithograph "
    "stencil poster, heroic low-angle bust portrait, centered composition, "
    "dramatic flat lighting, grim Catholic military theocracy, aged paper "
    "texture, plain flat background"
)

SHARED_NEG = (
    "score_6, score_5, score_4, glossy, smooth shading, modern cartoon, "
    "3d render, cel shaded anime, photorealistic, photograph, blurry, soft "
    "focus, uncolored, monochrome, greyscale, anime, manga, furry, chibi, "
    "multiple people, crowd, duplicate, inset, second face, thumbnail, "
    "picture in picture, framed poster on wall, text, caption, letters, "
    "words, signature, watermark, logo, deformed face, mutated hands, "
    "extra fingers"
)

# Per-army style clauses appended to SHARED_POS
_ARMY_CLAUSES: dict[str, str] = {
    "confederacion": (
        "clean crisp silkscreen flat color, olive drab green and celeste blue "
        "and cream and warm black palette, dignified ordered state propaganda, "
        "golden halo behind the head, brass crucifix"
    ),
    "ejercito_rojo": (
        "rough hand-carved woodcut linocut texture, ink splatter, "
        "worn red military uniform, red and black and bone cream palette, "
        "revolutionary fervor"
    ),
    # punteros are allied to the Ejército Rojo
    "punteros": (
        "rough hand-carved woodcut linocut texture, ink splatter, "
        "worn red military uniform, red and black and bone cream palette, "
        "revolutionary fervor"
    ),
}

# Inquisitor supplement (iglesia + inquisicion + cruzado/novicio/inquisidor)
_INQUISITOR_CLAUSE = (
    "inquisitor crusader, dark cassock and red sash, consecrated sword"
)

# ---------------------------------------------------------------------------
# Engine parameters
# ---------------------------------------------------------------------------

WIDTH = 832
HEIGHT = 1344
STEPS = 30
CFG = 7.0
SAMPLER = "dpmpp_2m"
SCHEDULER = "karras"
DENOISE = 1.0
MODEL = "zavyfantasiaxlPDXL_v20.safetensors"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SLUG_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")


def _slug(wikilink: str) -> str:
    """Extract bare slug from a [[slug|display]] wikilink."""
    m = _SLUG_RE.match(wikilink.strip())
    if m:
        raw = m.group(1)
        # strip path prefix (e.g. "4_diegesis/personajes/slug" -> "slug")
        return raw.split("/")[-1]
    return wikilink.strip()


def _tags_of(record: dict[str, Any], prefix: str) -> list[str]:
    """Return tag suffixes matching a given prefix."""
    full = f"{prefix}/"
    return [t[len(full):] for t in record.get("tags", []) if t.startswith(full)]


def _army(record: dict[str, Any]) -> str:
    """Resolve lealtad tag to army key; default to confederacion."""
    armies = _tags_of(record, "lealtad")
    if armies:
        return armies[0]
    return "confederacion"


def _deterministic_seed(slug: str) -> int:
    """Stable seed from slug (sha256, lower 32 bits, always positive)."""
    digest = hashlib.sha256(slug.encode()).digest()
    return int.from_bytes(digest[:4], "big") & 0x7FFFFFFF


# ---------------------------------------------------------------------------
# Mapping catalogs
# ---------------------------------------------------------------------------

def _map_subject(record: dict[str, Any]) -> str:
    """age + gender + attributes → portrait subject phrase."""
    edad = record.get("edad", 30)
    genero = record.get("genero", "m")
    gender_word = "woman" if genero == "f" else "man"

    attrs = record.get("atributos", {})
    cuerpo = attrs.get("cuerpo", 4)
    mente = attrs.get("mente", 4)
    alma = attrs.get("alma", 4)

    if cuerpo <= 3:
        build = "lean wiry build"
    elif cuerpo <= 5:
        build = "athletic build"
    else:
        build = "broad barrel-chested build"

    if mente <= 3:
        eyes = "tired glazed eyes"
    elif mente <= 5:
        eyes = "alert focused eyes"
    else:
        eyes = "sharp piercing eyes"

    if alma <= 3:
        presence = "withdrawn hollow presence"
    elif alma <= 5:
        presence = "composed steady demeanor"
    else:
        presence = "commanding iron gaze straight spine"

    return f"a {edad} year old {gender_word}, {build}, {eyes}, {presence}"


def _map_rank(record: dict[str, Any]) -> str:
    """rango tag → rank/insignia descriptor."""
    rangos = _tags_of(record, "rango")
    rango = rangos[0] if rangos else ""

    rank_map = {
        "recluta": "raw young conscript, plain uniform no insignia",
        "simpatizante": "anonymous plain civilian sympathizer",
        "soldado_linea": "enlisted soldier, basic rank insignia",
        "militante_resistencia": "resistance militant, no formal insignia",
        "marinero": "enlisted marine, naval collar insignia",
        "cabo": "NCO corporal, two chevrons on collar",
        "sargento": "NCO sergeant, three stripes on shoulder",
        "cabecilla": "commander, confident bearing, command authority",
        "lider": "leader, commanding stance, authority insignia",
        "novicio": "inquisitor initiate, rank sash and cassock",
        "inquisidor": "inquisitor officer, rank regalia and cassock",
        "sacerdote": "military chaplain, clerical collar, sacred vestments",
        "capellan": "military chaplain, clerical collar, sacred vestments",
        "puntero": "street-level organizer, worn civilian clothes",
        "pai_de_santo": "spiritual leader, ritual vestments",
        "meraya": "shaman, ritual adornments",
        "tratante": "trader, practical working clothes",
    }
    return rank_map.get(rango, "soldier, standard bearing")


def _map_especialidad(record: dict[str, Any]) -> str:
    """especialidad/* tag → role/gear descriptor."""
    esps = _tags_of(record, "especialidad")
    esp = esps[0] if esps else ""

    esp_map = {
        "combate/fusilero": "rifle shouldered, infantry parade stance, cartridge belt",
        "combate/asalto": "assault vest, breach-ready aggressive stance, submachine gun",
        "combate/tirador": "scoped marksman rifle, steady measured aim, binoculars",
        "combate/zapador": "sapper explosives rigging, demolition charges visible, combat knife",
        "combate/lider": "commander posture, radio or baton, directing hand gesture",
        "combate/cruzado": "consecrated sword raised, crusader iconography, holy warrior",
        "investigacion/espia": "covert plain clothes, collar turned up, concealed bearing",
        "investigacion/interrogador": "cold cruel expression, gloved hands, intimidating stare",
        "oficio/medico": "red-cross medic armband, field dressing kit, aid bag",
        "oficio/pescador": "weathered fisherman gear, rope and net",
        "oficio/tratante": "merchant bearing, coat with hidden pockets",
        "paranormal/curandero": "ritual healer bearing, herb bundle",
        "paranormal/medium": "distant trance bearing, ritual focus",
    }
    return esp_map.get(esp, "")


def _map_aspectos(record: dict[str, Any]) -> list[str]:
    """aspectos[] + aspecto/* tags → demeanor descriptors."""
    aspecto_tags = _tags_of(record, "aspecto")

    # also parse raw wikilinks in aspectos field (belt-and-suspenders)
    raw_aspectos = record.get("aspectos", [])
    slugs = [_slug(a) for a in raw_aspectos]

    combined = set(aspecto_tags + slugs)

    demeanor_map = {
        "veterano": "weathered calm scarred face, veteran composure",
        "veterano_de_campo": "weathered calm scarred face, field-worn veteran",
        "terco": "stubborn set jaw, locked resolute gaze",
        "religioso": "serene devout expression, crucifix held",
        "cobarde": "hunched shoulders, darting nervous eyes",
        "ojo_de_aguila": "piercing eagle gaze, hawk-eye intensity",
        "tirador": "steady measured aim, marksman focus",
        "tactico": "focused tactical bearing, calculating look",
        "vanguardia": "aggressive forward lean, assault-ready",
        "instinto": "alert tense posture, instinctive readiness",
        "instinto_de_supervivencia": "hyper-alert survival instinct, tense readiness",
        "manos_asperas": "rough calloused hands prominently visible",
        "manos_temblorosas": "tense trembling hands, barely controlled",
        "expresion_trance": "vacant trance gaze, otherworldly stillness",
        "rodilla_vencida": "stoic bearing despite visible fatigue",
    }

    result = []
    for tag in sorted(combined):
        if tag in demeanor_map:
            result.append(demeanor_map[tag])
    return result


def _map_rasgos(record: dict[str, Any]) -> list[str]:
    """rasgos[] + rasgo/* tags → physical mark descriptors."""
    rasgo_tags = _tags_of(record, "rasgo")

    raw_rasgos = record.get("rasgos", [])
    slugs = [_slug(r) for r in raw_rasgos]

    combined = set(rasgo_tags + slugs)

    marks_map = {
        "cicatriz_perturbadora": "disturbing deep facial scar, battle damage across cheek",
        "tatuaje_de_unidad": "unit tattoo visible on neck",
        "mirada_cansada": "heavy-lidded tired eyes, fatigue lines under eyes",
        "constitucion_robusta": "robust powerful build, broad muscular frame",
        "fe_obstinada": "iron faith devotion in expression, unyielding bearing",
        "duda_teologica": "slight uncertainty in eyes, hidden inner conflict",
        "paranoia_vigilancia": "hypervigilant darting suspicious gaze",
        "silencio_sagrado": "eerie composed silence in expression",
        "trance_psiquico": "unfocused distant psychic gaze",
        "afinidad_animal": "",  # no strong visual mapping for poster style
        "tatuaje_linaje_guarani": "guaraní lineage tattoo on face or neck",
    }

    result = []
    for tag in sorted(combined):
        mapped = marks_map.get(tag, "")
        if mapped:
            result.append(mapped)
    return result


def _map_vestidura(record: dict[str, Any]) -> str:
    """equipo/vestidura/* tags → uniform/clothing descriptor."""
    vestiduras = _tags_of(record, "equipo/vestidura")

    vest_map = {
        "uniforme_rojo": "worn red military uniform",
        "uniforme_linea": "olive drab state-issue military uniform",
        "uniforme_tactico_rojo": "red tactical combat uniform",
        "uniforme_gris_dns": "grey security forces uniform",
        "chaleco": "tactical vest",
        "chaleco_asalto": "heavy assault vest",
        "sotana": "long dark clerical cassock",
        "habito": "monastic religious habit",
        "galera": "formal fedora hat worn with authority",
        "capucha": "hood partially obscuring face",
        "chaqueta_de_cuero": "worn battered leather jacket",
        "chal_remendado": "patched worn shawl",
        "delantal_manchado": "stained work apron",
        "tocado_de_plumas": "feathered ceremonial headdress",
    }

    parts = []
    for v in vestiduras:
        if v in vest_map:
            parts.append(vest_map[v])
    return ", ".join(parts) if parts else "civilian clothes"


def _is_inquisition(record: dict[str, Any]) -> bool:
    """True if record is iglesia/inquisicion cruzado."""
    faccion = record.get("faccion", "")
    subfaccion = record.get("subfaccion", "")
    rangos = _tags_of(record, "rango")
    esps = _tags_of(record, "especialidad")
    return (
        faccion == "iglesia"
        and subfaccion == "inquisicion"
        and (
            any(r in ("novicio", "inquisidor") for r in rangos)
            or "combate/cruzado" in esps
        )
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_prompt(record: dict[str, Any]) -> dict[str, Any]:
    """Build a ComfyUI job dict from a soldier record.

    Parameters
    ----------
    record : dict
        Parsed frontmatter from a syv-pj personaje .md file.

    Returns
    -------
    dict with keys:
        slug, positive, negative, width, height, seed, filename_prefix,
        model, steps, cfg, sampler, scheduler, denoise
    """
    slug = record.get("slug", "unknown")
    army = _army(record)

    # Build positive prompt parts
    army_clause = _ARMY_CLAUSES.get(army, _ARMY_CLAUSES["confederacion"])

    subject = _map_subject(record)
    rank = _map_rank(record)
    especialidad = _map_especialidad(record)
    aspectos = _map_aspectos(record)
    rasgos = _map_rasgos(record)
    vestidura = _map_vestidura(record)

    # Assemble subject+role block
    subject_parts = [subject, rank]
    if especialidad:
        subject_parts.append(especialidad)
    if vestidura:
        subject_parts.append(vestidura)
    subject_parts.extend(aspectos)
    subject_parts.extend(rasgos)
    subject_block = ", ".join(subject_parts)

    # Assemble full positive
    pos_parts = [SHARED_POS, army_clause, subject_block]
    if _is_inquisition(record):
        pos_parts.append(_INQUISITOR_CLAUSE)

    positive = ", ".join(pos_parts)
    seed = _deterministic_seed(slug)

    return {
        "slug": slug,
        "nombre": record.get("nombre", slug),
        "army": army,
        "positive": positive,
        "negative": SHARED_NEG,
        "width": WIDTH,
        "height": HEIGHT,
        "seed": seed,
        "filename_prefix": f"syv_portrait_{slug}",
        "model": MODEL,
        "steps": STEPS,
        "cfg": CFG,
        "sampler": SAMPLER,
        "scheduler": SCHEDULER,
        "denoise": DENOISE,
    }
