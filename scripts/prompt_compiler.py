#!/usr/bin/env python3
"""Compilador determinista ficha → prompt (SyV / Z-Image Turbo).

El corazón: traducir los stats cuerpo/mente/alma (escala 1-6, 3 = promedio) a
descriptores visuales en inglés, con estas leyes (de la investigación):

  · CENTRO = SILENCIO. stat 3 → no se dice nada (band 0 = "").
  · ASIMETRÍA. la distancia al centro es la intensidad; low y high no son
    espejos: low describe carencia, high describe presencia/impacto.
  · CANAL POR ATRIBUTO. cuerpo → el cuerpo · mente → mirada/rostro (NO lentes)
    · alma → aura/porte + peso emocional.
  · POOL + ELECCIÓN DETERMINISTA. cada banda es un pool; se elige por hash de
    (slug+atributo) → mismo input siempre igual, pero distintos personajes varían.
  · GATING POR CONTEXTO. el pool de cuerpo se filtra por rol (facción) antes de elegir.

Uso:
  python3 prompt_compiler.py            # demo sobre el casting
  python3 prompt_compiler.py <slug>     # un personaje: descriptores + prompt completo
"""
from __future__ import annotations
import hashlib, re, sys
from pathlib import Path

PERSONAJES = Path(__file__).resolve().parent.parent.parent / "syv-pj/resources/personajes"

# ---------- pools por banda (band = stat - 3, clamp -2..+3) ----------
CUERPO = {
    -2: ["frail, gaunt frame", "scrawny, bony build", "sickly, wasted frame"],
    -1: ["slight, lean frame", "wiry, spare build", "thin, light frame"],
     0: [""],
     1: {"laborer": ["solid, work-hardened build"], "soldier": ["fit, trained build"],
         "authority": ["heavyset, sturdy build"], "mystic": ["lean, weathered build"],
         "default": ["solid, athletic build"]},
     2: {"laborer": ["powerful, work-thickened build, broad back"], "soldier": ["muscular, athletic, broad-shouldered"],
         "authority": ["imposing, broad, heavyset frame"], "mystic": ["strong, sinewy build"],
         "default": ["muscular, broad-shouldered"]},
     3: {"authority": ["ox-built, hulking, imposing bulk"], "soldier": ["hulking, powerfully muscled"],
         "laborer": ["massive, thick-limbed, powerful"], "default": ["massive, imposing, powerfully built"]},
}
MENTE = {
    -2: ["vacant dull gaze, slack expression"],
    -1: ["plain simple expression, unfocused eyes"],
     0: [""],
     1: ["alert attentive eyes, sharp focus"],
     2: ["sharp analytical gaze, intelligent eyes, faint calculating look"],
     3: ["piercing intelligent gaze, penetrating analytical stare, brilliant focused eyes"],
}
ALMA = {
    -2: ["hollow forgettable presence, eyes that avoid yours"],
    -1: ["quiet anodyne bearing, weary downcast eyes"],
     0: [""],
     1: ["warm magnetic presence, engaged gaze"],
     2: ["commanding presence, regal bearing, intense steady gaze"],
     3: ["overwhelming magnetic aura, luminous commanding gaze, gravity bends toward them"],
}
# alma alta tiñe la LUZ; alma baja la apaga
ALMA_LIGHT = {2: "lit with a subtle hero rim light", 3: "haloed by dramatic rim light",
              -1: "flat even light", -2: "dim flat light, sinking into the background"}

EQUIPO_LEX = {
    "rosario": "a worn rosary", "red_de_pesca": "a fishing net", "chal_remendado": "a mended darned shawl",
    "espada_consagrada": "a consecrated sword", "medallon": "a blessed medallion",
    "binoculares": "scratched binoculars", "pistola": "an old pistol at the belt",
}
FACTION_SCENE = {
    "laborer": "on rotting rain-soaked docks, perpetual drizzle, worn analog low-tech world",
    "soldier": "at a muddy fortified encampment, grey overcast, militarized dystopia",
    "authority": "in a damp candle-lit stone hall, oppressive theocratic gloom",
    "mystic": "among misty swamp reeds and dim ritual light",
    "default": "in a worn dystopian setting, perpetual rain",
}


def role_of(faccion: str) -> str:
    f = (faccion or "").lower()
    if any(k in f for k in ("pescador", "gremio", "obrero", "portuari", "muelle")): return "laborer"
    if any(k in f for k in ("inquisic", "iglesia", "clero", "sacerd", "umbanda", "orixa")): return "authority"
    if any(k in f for k in ("fuerzas", "confedera", "ejercito", "resistencia", "militar", "soldado")): return "soldier"
    if any(k in f for k in ("shipibo", "conibo", "chaman", "pantano")): return "mystic"
    return "default"


def _band(stat: int) -> int:
    return max(-2, min(3, int(stat) - 3))


def _pick(pool: list[str], slug: str, attr: str) -> str:
    if not pool:
        return ""
    h = int(hashlib.md5(f"{slug}:{attr}".encode()).hexdigest(), 16)
    return pool[h % len(pool)]


def _resolve(table, band, role):
    cell = table[band]
    if isinstance(cell, dict):
        return cell.get(role, cell["default"])
    return cell


def descriptors(stats: dict, faccion: str, slug: str) -> dict:
    role = role_of(faccion)
    bc, bm, ba = _band(stats["cuerpo"]), _band(stats["mente"]), _band(stats["alma"])
    return {
        "role": role,
        "cuerpo": _pick(_resolve(CUERPO, bc, role), slug, "cuerpo"),
        "mente": _pick(_resolve(MENTE, bm, role), slug, "mente"),
        "alma": _pick(_resolve(ALMA, ba, role), slug, "alma"),
        "light": ALMA_LIGHT.get(ba, "natural light"),
        "bands": (bc, bm, ba),
    }


def compose(ficha: dict) -> str:
    slug = ficha["slug"]
    d = descriptors(ficha["atributos"], ficha["faccion"], slug)
    sujeto = f"{'woman' if ficha.get('genero') == 'f' else 'man'}, {ficha.get('edad', '')} years old"
    apar = ", ".join(ficha.get("apariencia", [])[:3])
    equipo = ", ".join(EQUIPO_LEX.get(e, e.replace("_", " ")) for e in ficha.get("equipo", [])[:3])
    aspecto = ", ".join(x for x in (d["cuerpo"], d["mente"], d["alma"]) if x)
    escena = FACTION_SCENE.get(d["role"], FACTION_SCENE["default"])
    foto = f"shot on an 85mm lens, Kodak Portra 400 tones, {d['light']}"
    textura = "visible pores and fine skin texture, candid documentary realism, photoreal"
    parts = [p for p in (f"a {sujeto}", apar, aspecto, equipo, escena, foto, textura) if p]
    return ". ".join(parts) + "."


# ---------- lector de ficha (frontmatter mínimo, sin deps) ----------
def load_ficha(slug: str) -> dict:
    txt = (PERSONAJES / f"{slug}.md").read_text()
    fm = txt.split("---", 2)[1]
    def scalar(k, default=""):
        m = re.search(rf"^{k}:\s*(.+)$", fm, re.M)
        return m.group(1).strip() if m else default
    def block_ints(name):
        m = re.search(rf"^{name}:\n((?:\s+\w+:\s*\d+\n)+)", fm, re.M)
        d = {}
        if m:
            for ln in m.group(1).splitlines():
                kk = re.match(r"\s+(\w+):\s*(\d+)", ln)
                if kk: d[kk.group(1)] = int(kk.group(2))
        return d
    def list_items(name):
        m = re.search(rf"^{name}:\n((?:\s+-\s*.+\n?)+)", fm, re.M)
        out = []
        if m:
            for ln in m.group(1).splitlines():
                v = re.match(r"\s+-\s*(.+)", ln)
                if v:
                    out.append(re.sub(r'["\[\]]', "", v.group(1)).strip())
        return out
    return {
        "slug": slug, "faccion": scalar("faccion"), "genero": scalar("genero"),
        "edad": scalar("edad"), "atributos": block_ints("atributos"),
        "apariencia": list_items("apariencia"), "equipo": list_items("equipo"),
    }


def main():
    if len(sys.argv) > 1:
        slugs = [sys.argv[1]]
    else:
        slugs = ["luisa-pescadora", "baltasar-quevedo-inquisidor", "anibal-painemal-comandante",
                 "iracema-chaman-pantano", "yara-sacerdotisa-orixa"]
    for slug in slugs:
        f = load_ficha(slug)
        a = f["atributos"]
        d = descriptors(a, f["faccion"], slug)
        print(f"\n=== {slug}  ({f['faccion']} · {d['role']}) ===")
        print(f"  stats  cuerpo={a.get('cuerpo')} mente={a.get('mente')} alma={a.get('alma')}  bands={d['bands']}")
        print(f"  cuerpo → {d['cuerpo'] or '(silencio)'}")
        print(f"  mente  → {d['mente'] or '(silencio)'}")
        print(f"  alma   → {d['alma'] or '(silencio)'}   luz: {d['light']}")
        if len(slugs) == 1:
            print(f"\n  PROMPT:\n  {compose(f)}")


if __name__ == "__main__":
    main()
