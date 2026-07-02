#!/usr/bin/env python3
"""Galería 5 personajes × 5 estilos = 25 imágenes (Z-Image Turbo).
Zona estética: entre cartoon y foto — realismo gráfico tipo Sin City / serigrafía,
paletas limitadas (SyV + kdx). Escribe results.json para la galería HTML."""
import sys, time, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from generate_zimage_panorama import post, wait, UNET, CLIP, VAE

SESSION = HERE.parent / "prompts/inbox/20260629-galeria-estilos"
SESSION.mkdir(parents=True, exist_ok=True)

# ---- 5 personajes (SyV) ----
CHARS = [
 {"key":"luisa","name":"Luisa la Pescadora","desc":
  "a weathered 40-year-old mestiza fisherwoman, hair in a tight bun, tired downcast eyes, mended shawl, worn rosary"},
 {"key":"sor-clara","name":"Sor Clara","desc":
  "a young beautiful 22-year-old nun, pale serene delicate face, black and white wimple and habit, holding a rosary, devout calm gaze"},
 {"key":"sgt-vega","name":"Sargento Vega","desc":
  "a 45-year-old veteran soldier, weathered scarred face, grey stubble, worn military cap, olive drab uniform, hard tired eyes"},
 {"key":"cap-olmos","name":"Capitán Olmos","desc":
  "a 60-year-old grizzled veteran captain, deeply lined weathered stern face, worn decorated officer uniform with peaked cap, commanding gaze"},
 {"key":"vera-sniper","name":"Vera «la Sombra»","desc":
  "a 30-year-old female sniper, cold focused eyes, face half-wrapped in a worn scarf, lean, ragged camouflage clothing, holding a scoped rifle"},
]

# ---- 5 estilos sutiles (realismo gráfico, paleta limitada) ----
STYLES = [
 {"key":"serigrafia-syv","label":"Serigrafía SyV 4 colores","cfg":1.5,"lead":
  "Four-color silkscreen propaganda screenprint, strictly limited palette of olive drab green, pale sky blue, "
  "cream off-white and warm near-black, bold flat color areas, heavy halftone dots, screenprint grain, high contrast"},
 {"key":"noir-duotone","label":"Noir duotono (Sin City)","cfg":1.6,"lead":
  "High-contrast graphic-novel noir illustration in Sin City style, stark warm-black and cream duotone with a single "
  "pale sky-blue accent, heavy inked shadows, halftone dot shading, dramatic chiaroscuro"},
 {"key":"kdx-naranja","label":"Serigrafía kdx naranja","cfg":1.5,"lead":
  "Bold silkscreen poster, limited palette of warm near-black, burnt orange, cream and teal, flat color areas, "
  "halftone texture, propaganda aesthetic, high contrast, stylized realism"},
 {"key":"riso-3color","label":"Risograph 3 tintas","cfg":1.6,"lead":
  "Three-color risograph print in warm black, olive green and amber, visible paper grain and halftone, slight ink "
  "misregistration, graphic poster, Sin City contrast, stylized realism"},
 {"key":"gouache-poster","label":"Gouache poster","cfg":1.4,"lead":
  "Limited-palette gouache propaganda poster, muted olive drab, celeste, cream and warm black, painterly flat shapes, "
  "subtle grain, stylized graphic realism, between photo and illustration"},
]

WORLD = "somber dystopian militarized catholic world, perpetual rain, worn analog low-tech aesthetic, no text, no lettering"


def wf(prompt, seed, cfg, prefix):
    return {
      "1":{"class_type":"UnetLoaderGGUF","inputs":{"unet_name":UNET}},
      "2":{"class_type":"ModelSamplingAuraFlow","inputs":{"shift":3.0,"model":["1",0]}},
      "3":{"class_type":"CLIPLoader","inputs":{"clip_name":CLIP,"type":"lumina2","device":"default"}},
      "4":{"class_type":"CLIPTextEncode","inputs":{"text":prompt,"clip":["3",0]}},
      "5":{"class_type":"ConditioningZeroOut","inputs":{"conditioning":["4",0]}},
      "6":{"class_type":"EmptySD3LatentImage","inputs":{"width":704,"height":960,"batch_size":1}},
      "7":{"class_type":"KSampler","inputs":{"seed":seed,"steps":8,"cfg":cfg,"sampler_name":"res_multistep",
           "scheduler":"simple","denoise":1.0,"model":["2",0],"positive":["4",0],"negative":["5",0],"latent_image":["6",0]}},
      "8":{"class_type":"VAELoader","inputs":{"vae_name":VAE}},
      "9":{"class_type":"VAEDecode","inputs":{"samples":["7",0],"vae":["8",0]}},
      "10":{"class_type":"SaveImage","inputs":{"filename_prefix":prefix,"images":["9",0]}},
    }


def main():
    results=[]
    n=0; total=len(CHARS)*len(STYLES)
    for c in CHARS:
        for s in STYLES:
            n+=1
            seed = 60000 + n
            prompt = f"{s['lead']}. {c['desc']}, {WORLD}."
            prefix = f"zgaleria/{c['key']}__{s['key']}"
            t0=time.time()
            pid=post(wf(prompt, seed, s["cfg"], prefix))
            imgs=wait(pid)
            fn = imgs[0]["filename"] if imgs else None
            sub = imgs[0].get("subfolder","") if imgs else ""
            print(f"[{n}/{total}] {c['key']} · {s['key']} {time.time()-t0:.0f}s -> {fn}", flush=True)
            results.append({"char":c["key"],"char_name":c["name"],"style":s["key"],
                            "style_label":s["label"],"seed":seed,"filename":fn,"subfolder":sub,
                            "prompt":prompt})
            (SESSION/"results.json").write_text(json.dumps(
                {"chars":CHARS,"styles":STYLES,"results":results}, ensure_ascii=False, indent=1))
    ok=sum(1 for r in results if r["filename"])
    print(f"\nLISTO {ok}/{total}")


if __name__ == "__main__":
    main()
