"""Miniature per prodotto (evidenziato in rosso su modello fantasma). Uso: 05_thumbs.py [codici-file ...]"""
import sys, re, json, glob, os; sys.path.insert(0, "scripts")
from lib import *
codes = sys.argv[1:] or ["PX0000381686"]
done = set(os.listdir("work/thumbs"))
meta = {}
for code in codes:
    d = load(code); V, N, F, FP, prods = d["V"], d["N"], d["F"], d["FP"], d["prods"]
    cnt = np.bincount(FP, minlength=len(prods))
    todo = []
    for pi, name in enumerate(prods):
        key = re.sub(r"[^A-Za-z0-9=_.-]", "_", name)
        if f"{key}.png" in done: continue
        todo.append((pi, name, key))
    if not todo: continue
    reset(); sc = setup_cycles(10, (480, 270))
    lo, hi = V.min(0), V.max(0)
    w = bpy.data.worlds.new("w"); w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.95, 0.95, 0.95, 1); sc.world = w
    red = flat_mat("r", (0.55, 0.12, 0.08), 0.5)
    cam = camera((0, -1, 1), (0, 0, 0), 35)
    for pi, name, key in todo:
        m = FP == pi
        if not m.any(): continue
        # niente fantasma per i prodotti: nascondi solo la mesh del prodotto in rosso sopra
        ob = mesh_obj("p", V, N, F[m]); ob.data.materials.append(red)
        vi = np.unique(F[m].ravel()); pv = V[vi]; plo, phi = pv.min(0), pv.max(0); c = (plo + phi) / 2
        dist = max(np.linalg.norm(phi - plo) * 1.5, 0.08)
        az, el = math.radians(50), math.radians(25)
        loc = (c[0] + dist * math.cos(el) * math.sin(az), c[1] - dist * math.cos(el) * math.cos(az), c[2] + dist * math.sin(el))
        cam.location = loc; cam.rotation_euler = (mathutils.Vector(c) - mathutils.Vector(loc)).to_track_quat("-Z", "Y").to_euler()
        sc.render.filepath = f"work/thumbs/{key}.png"; bpy.ops.render.render(write_still=True)
        bpy.data.objects.remove(ob, do_unlink=True)
        meta[key] = dict(name=name, file=code, faces=int(m.sum()), size_mm=((phi - plo) * 1000).round(0).tolist(), ctr_mm=(c * 1000).round(0).tolist())
        done.add(f"{key}.png"); print(code, name, flush=True)
    json.dump(meta, open(f"work/thumbs_meta_{code}.json", "w"))
