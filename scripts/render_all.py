"""Render di tutte le viste. Uso:
   python3 scripts/render_all.py [--only PX0000380493] [--views 34alta,laterale] [--res 1920x1080] [--samples 128] [--masters] [--transparent]
   Colori reti: env RETE_ACC / RETE_FRE / RETE_STD (hex) oppure config/colors.json. Esempio:
   RETE_ACC='#d98a00' python3 scripts/render_all.py --only PX0000380493"""
import argparse, time, os, sys, json; sys.path.insert(0, os.path.dirname(__file__))
from scene import *

NAMES = {"PX0000381686": "assieme", "PX0000380493": "nastri", "PX0000381687": "nastri", "PX0000381735": "nastri", "PX0000381782": "nastri", "PX0000381771": "ftc", "PX0000381774": "ftc"}
RETE = {"PX0000380493": "RETE_ACC", "PX0000381687": "RETE_FRE", "PX0000381735": "RETE_STD", "PX0000381782": "RETE_STD"}

def fit_dist(tgt, az, el, lens, corners, aspect=16/9, margin=0.95):
    a, e = math.radians(az), math.radians(el); dirv = np.array([math.cos(e)*math.sin(a), -math.cos(e)*math.cos(a), math.sin(e)])
    f = -dirv; r = np.cross(f, [0, 0, 1]); r /= np.linalg.norm(r); u = np.cross(r, f); tx = 18.0 / lens; ty = tx / aspect
    d = 0.05
    while d < 200:
        loc = tgt + dirv * d; v = corners - loc; z = v @ f
        if (z > 0.02).all() and (np.abs(v @ r) / z / tx < margin).all() and (np.abs(v @ u) / z / ty < margin).all(): return d
        d *= 1.03
    return d

def belt_top(d, fams, fid, V, name):
    i = fams.index(name) if name in fams else None
    return V[d["F"][fid == i].ravel()] if i is not None else None

def views_for(code, d, fams, fid):
    V, F = d["V"], d["F"]; lo, hi = V.min(0), V.max(0); c = (lo + hi) / 2; ext = hi - lo
    corners = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
    out = []
    def add(name, az, el, lens, tgt=None, dist=None, fit=True, dof=None, margin=0.95, aspect=16/9):
        t = c if tgt is None else np.array(tgt)
        dd = fit_dist(t, az, el, lens, corners, aspect=aspect, margin=margin) if (fit and dist is None) else dist
        out.append(dict(name=name, az=az, el=el, lens=lens, tgt=t, dist=dd, dof=dof, aspect=aspect))
    kind = NAMES[code]
    if kind == "assieme":
        add("34alta", 62, 30, 35); add("34bassa", 55, 8, 35, margin=0.97); add("laterale", 90, 1.5, 50, aspect=4.0); add("alto", 90, 88, 40, aspect=4.0)
        # giunzioni tra nastri: confini lungo Y tra i prodotti rete
        P, FP, prods = d["P"], d["FP"], d["prods"]; rng = []
        for fam in ("RETE_STD", "RETE_ACC", "RETE_FRE"):
            if fam not in fams: continue
            m = fid == fams.index(fam)
            for pi in np.unique(FP[m]):
                vv = V[F[m & (FP == pi)].ravel()]; rng.append((vv[:, 1].min(), vv[:, 1].max(), fam))
        rng.sort(); js = [(rng[i][1] + rng[i+1][0]) / 2 for i in range(len(rng) - 1)]
        zt = float(np.percentile(V[F[fid == fams.index("RETE_STD")].ravel()][:, 2], 99)) if "RETE_STD" in fams else c[2]
        if js: add("34hero", 58, 24, 35, tgt=(c[0], float(np.mean(js)), zt - 0.3), dist=5.0, fit=False)
        for k, y in enumerate(js[:3]): add(f"giunzione{k+1}", 50 + 25 * (k % 2), 22, 85, tgt=(c[0], y, zt - 0.02), dist=2.0, fit=False)
    elif kind == "nastri":
        add("34", 40, 22, 50); add("laterale", 90, 2, 50)
        y_head = lo[1]; zt = float(np.percentile(V[F[fid == fams.index(RETE[code])].ravel()][:, 2], 99))
        add("testata", 52, 16, 85, tgt=(c[0] + 0.12, y_head + 0.28, c[2] + 0.1), dist=1.6, fit=False, dof=None)
        add("rete", 28, 38, 85, tgt=(c[0], c[1] + (0.0 if ext[1] < 3 else 0.0), zt), dist=0.9, fit=False)
        if code == "PX0000381782": add("fuga", 9, 9, 28, tgt=(c[0], lo[1] + 4.0, lo[2] + 0.7), dist=5.2, fit=False)
    elif kind == "ftc":
        add("34", 38, 22, 70); 
        # sensore: baricentro delle facce di plastica sensore/verde, altrimenti centro
        sel = [fams.index(f) for f in ("PL_SENSORE", "PL_VERDE") if f in fams]
        cc = V[F[np.isin(fid, sel)].ravel()].mean(0) if sel else c
        add("dettaglio", 40, 18, 100, tgt=cc, dist=0.45, fit=False)
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--only"); ap.add_argument("--views"); ap.add_argument("--skip", default=""); ap.add_argument("--no-render", action="store_true"); ap.add_argument("--res", default="1920x1080")
    ap.add_argument("--samples", type=int, default=128); ap.add_argument("--masters", action="store_true"); ap.add_argument("--transparent", action="store_true")
    ap.add_argument("--out", default="output"); ap.add_argument("--save-blend", action="store_true"); ap.add_argument("--show-arrow", action="store_true")
    a = ap.parse_args()
    codes = [a.only] if a.only else list(NAMES)
    for code in codes:
        t0 = time.time(); reset(); M = make_materials(); d, objs = build_objects(code, M, hide_arrow=not a.show_arrow)
        fams, fid, _ = facemat.face_families(code, {k: d[k] for k in d}); d["P"] = d["prods"]
        V = d["V"]; lo, hi = V.min(0), V.max(0); Rr = float(np.linalg.norm(hi - lo)); studio(lo, hi, size_ref=Rr); cyc = make_cyc(max(Rr, 1.0), lo[2])
        res = tuple(int(x) for x in a.res.split("x")); tag = "4K" if res[0] >= 3840 else ("FHD" if res[0] >= 1920 else f"{res[0]}")
        for v in views_for(code, d, fams, fid):
            if a.views and v["name"] not in a.views.split(","): continue
            if v["name"] in a.skip.split(","): continue
            if a.no_render: continue
            for o in [o for o in bpy.data.objects if o.type == "CAMERA"]: bpy.data.objects.remove(o)
            ar, e = math.radians(v["az"]), math.radians(v["el"]); t = v["tgt"]
            loc = (t[0] + v["dist"] * math.cos(e) * math.sin(ar), t[1] - v["dist"] * math.cos(e) * math.cos(ar), t[2] + v["dist"] * math.sin(e))
            cam_look(loc, tuple(t), v["lens"], v["dof"]); place_cyc(cyc, v["az"], t, lo[2])
            sub = os.path.join(a.out, "renders", NAMES[code]); os.makedirs(sub, exist_ok=True)
            base = os.path.join(sub, f"{code}_{v['name']}_{tag}"); t1 = time.time()
            if os.path.exists(base + (".png" if a.masters else ".jpg")) and not os.environ.get("FORCE"): print(f"{code} {v['name']} {tag} gia' presente, salto", flush=True); continue
            vres = (res[0], int(res[0] / v["aspect"])) if v["aspect"] != 16/9 else res
            render(base + (".png" if a.masters else ".jpg"), vres, a.samples, False, "PNG" if a.masters else "JPEG", "16" if a.masters else "8")
            if a.masters:
                im = bpy.data.images.load(os.path.abspath(base + ".png")); im.scale(1920, int(1920 / (vres[0] / vres[1])))
                im.file_format = "JPEG"; im.filepath_raw = os.path.abspath(base.replace("_4K", "_FHD") + ".jpg"); im.save(); bpy.data.images.remove(im)
            print(f"{code} {v['name']} {tag} {time.time()-t1:.0f}s", flush=True)
            if a.transparent:
                render(base + "_alpha.png", vres, a.samples, True, "PNG", "8")
        if a.save_blend:
            os.makedirs(os.path.join(a.out, "blender"), exist_ok=True); bpy.ops.wm.save_as_mainfile(filepath=os.path.join(a.out, "blender", f"{code}.blend"), compress=True)
        print(code, f"totale {time.time()-t0:.0f}s", flush=True)
main()
