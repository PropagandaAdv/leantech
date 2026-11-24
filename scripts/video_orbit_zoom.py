"""Video assieme PX0000381686: partenza da 34alta, orbita 360 (camera + luci + ciclorama girano insieme: effetto piatto girevole),
pausa, zoom fino a 34hero. Un frame per file (riprendibile).
Uso: video_orbit_zoom.py [--fps 25] [--orbit 10] [--hold 1] [--zoom 5] [--res 1920x1080] [--samples 32] [--frames-dir DIR] [--only 0,100,...]"""
import argparse, os, sys, math, time; sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("PROFILE", "v2"); os.environ.setdefault("FRENO_VARIANT", "a")
from render_all import *

ap = argparse.ArgumentParser(); ap.add_argument("--fps", type=int, default=25); ap.add_argument("--orbit", type=float, default=10); ap.add_argument("--hold", type=float, default=1)
ap.add_argument("--zoom", type=float, default=5); ap.add_argument("--res", default="1920x1080"); ap.add_argument("--samples", type=int, default=32)
ap.add_argument("--frames-dir", default="work/video_frames"); ap.add_argument("--only", default=""); a = ap.parse_args()
code = "PX0000381686"; os.makedirs(a.frames_dir, exist_ok=True)
reset(); M = make_materials(); d, objs = build_objects(code, M, hide_arrow=True)
fams, fid, _ = facemat.face_families(code, {k: d[k] for k in d}); d["P"] = d["prods"]
V = d["V"]; lo, hi = V.min(0), V.max(0); Rr = float(np.linalg.norm(hi - lo)); studio(lo, hi, size_ref=Rr); cyc = make_cyc(max(Rr, 1.0), lo[2])
vs = {v["name"]: v for v in views_for(code, d, fams, fid)}; A0, H0 = vs["34alta"], vs["34hero"]
corners = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]); c = (lo + hi) / 2
# luci agganciate a un Empty al centro: ruotano con la camera durante l'orbita
emp = bpy.data.objects.new("lightrig", None); bpy.context.scene.collection.objects.link(emp); emp.location = tuple(c)
for o in bpy.data.objects:
    if o.type == "LIGHT": o.parent = emp; o.matrix_parent_inverse = emp.matrix_world.inverted()
sc = bpy.context.scene; sc.render.use_persistent_data = True
n_o, n_h, n_z = [int(round(x * a.fps)) for x in (a.orbit, a.hold, a.zoom)]; N = n_o + n_h + n_z
ss = lambda t: t * t * (3 - 2 * t)                 # ease in/out
sss = lambda t: t * t * t * (t * (6 * t - 15) + 10)  # ease in/out piu' morbido (zoom)
# distanza camera in orbita: mai sotto quella di 34alta, tirata indietro solo dove serve per non tagliare l'assieme; smussata (periodica)
az0, el0, D0 = A0["az"], A0["el"], A0["dist"]; K = 720
need = np.array([max(D0, fit_dist(c, az0 + 360.0 * k / K, el0, A0["lens"], corners, margin=0.95)) for k in range(K)])
w = 36; kern = np.ones(2 * w + 1) / (2 * w + 1); sm = np.convolve(np.concatenate([need[-w:], need, need[:w]]), kern, mode="valid")[:K]
dist_theta = np.maximum(sm, need)
def pose(i):
    if i < n_o:
        th = ss(i / n_o) * 360.0; k = (th / 360.0 * K) % K; k0 = int(k) % K; k1 = (k0 + 1) % K; dd = dist_theta[k0] * (1 - (k - int(k))) + dist_theta[k1] * (k - int(k))
        if i == 0: dd = D0
        return dict(az=az0 + th, el=el0, dist=float(dd), tgt=np.array(A0["tgt"], float), lens=A0["lens"], light=th)
    if i < n_o + n_h: return dict(az=az0, el=el0, dist=D0, tgt=np.array(A0["tgt"], float), lens=A0["lens"], light=0.0)
    s_ = sss((i - n_o - n_h + 1) / n_z); tg0, tg1 = np.array(A0["tgt"], float), np.array(H0["tgt"], float)
    return dict(az=az0 + (H0["az"] - az0) * s_, el=el0 + (H0["el"] - el0) * s_, dist=float(math.exp(math.log(D0) + (math.log(H0["dist"]) - math.log(D0)) * s_)), tgt=tg0 + (tg1 - tg0) * s_, lens=A0["lens"], light=0.0)
res = tuple(int(x) for x in a.res.split("x")); idx = [int(x) for x in a.only.split(",")] if a.only else list(range(N))
print(f"frame totali {N} ({a.orbit}s orbita + {a.hold}s pausa + {a.zoom}s zoom a {a.fps} fps)", flush=True); t0 = time.time(); done = 0
for i in idx:
    out = os.path.join(a.frames_dir, f"frame_{i:04d}.jpg")
    if os.path.exists(out): continue
    p = pose(i); ar, e = math.radians(p["az"]), math.radians(p["el"]); t = p["tgt"]
    loc = (t[0] + p["dist"] * math.cos(e) * math.sin(ar), t[1] - p["dist"] * math.cos(e) * math.cos(ar), t[2] + p["dist"] * math.sin(e))
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]: bpy.data.objects.remove(o)
    cam_look(loc, tuple(t), p["lens"]); place_cyc(cyc, p["az"], t, lo[2]); emp.rotation_euler = (0, 0, math.radians(p["light"]))
    t1 = time.time(); render(out, res, a.samples, False, "JPEG", "8"); done += 1
    print(f"frame {i}/{N-1} {time.time()-t1:.0f}s  az {p['az']%360:.1f} dist {p['dist']:.1f}", flush=True)
print("FRAMES_DONE", done, f"{time.time()-t0:.0f}s")
