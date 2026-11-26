"""Animazione continua del layout: L1 (intero) -> L2 (zona RAT) -> L5-like (triplo banco), con collo che attraversa il RAT a 30 gradi.
Riusa la scena di layout_build.py. Uso: layout_anim.py [--fps 25] [--res 1920x1080] [--samples 12] [--dir work/anim_main] [--only 0,100]"""
import sys, os, math, time, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ap = argparse.ArgumentParser(); ap.add_argument("--fps", type=int, default=25); ap.add_argument("--res", default="1920x1080"); ap.add_argument("--samples", type=int, default=12)
ap.add_argument("--dir", default="work/anim_main"); ap.add_argument("--only", default=""); A = ap.parse_args()
src = open(os.path.join(HERE, "layout_build.py")).read().split("res = tuple(")[0]
sys.argv = ["layout_build.py", "--views", "L1", "--out", "work/anim_tmp"]; exec(compile(src, os.path.join(HERE, "layout_build.py"), "exec"))
fps = A.fps; os.makedirs(A.dir, exist_ok=True)
P0, P1, P2 = VIEWS["L1"], VIEWS["L2"], VIEWS["L6"]
T = [("hold", 1.0), ("move", 5.0, P0, P1), ("hold", 0.5), ("move", 4.0, P1, P2), ("hold", 2.5)]
total = sum(t[1] for t in T); N = int(round(total * fps)); T_BOX = (total - 2.4, total - 0.2)
ease = lambda u: u * u * u * (u * (6 * u - 15) + 10)
def pose(t):
    tt = 0.0; last = P0
    for seg in T:
        if t <= tt + seg[1] + 1e-9:
            if seg[0] == "hold": return last
            u = ease(min(max((t - tt) / seg[1], 0), 1)); a, b = seg[2], seg[3]
            return dict(az=a["az"] + (b["az"] - a["az"]) * u, el=a["el"] + (b["el"] - a["el"]) * u, lens=a["lens"] + (b["lens"] - a["lens"]) * u,
                        tgt=np.array(a["tgt"], float) + (np.array(b["tgt"], float) - np.array(a["tgt"], float)) * u, dist=math.exp(math.log(a["dist"]) + (math.log(b["dist"]) - math.log(a["dist"])) * u))
        tt += seg[1]; last = seg[3] if seg[0] == "move" else last
    return last
box = bpy.data.objects["collo_deviato"]; base_c = np.array([JX[0] - 0.05, 0.05]); S = np.array([JX[0] - 0.30, -0.25]); Dv = np.array([math.cos(math.radians(30)), math.sin(math.radians(30))]) * 0.80
print(f"frame totali {N} ({total:.1f}s a {fps} fps)", flush=True); res = tuple(int(x) for x in A.res.split("x")); idx = [int(x) for x in A.only.split(",")] if A.only else range(N); t0 = time.time(); done = 0
for i in idx:
    out = os.path.join(A.dir, f"frame_{i:04d}.jpg")
    if os.path.exists(out): continue
    t = i / fps; v = pose(t); u = ease(min(max((t - T_BOX[0]) / (T_BOX[1] - T_BOX[0]), 0), 1)); pc = S + Dv * u
    box.location = (pc[0] - base_c[0], pc[1] - base_c[1], 0.0)
    ar, e = math.radians(v["az"]), math.radians(v["el"]); tg = v["tgt"]
    loc = (tg[0] + v["dist"] * math.cos(e) * math.sin(ar), tg[1] - v["dist"] * math.cos(e) * math.cos(ar), tg[2] + v["dist"] * math.sin(e))
    for o in [o for o in bpy.data.objects if o.type == "CAMERA"]: bpy.data.objects.remove(o)
    cam_look(loc, tuple(tg), v["lens"]); place_cyc(cyc, v["az"], tg, 0.0); t1 = time.time()
    render(out, res, A.samples, False, "JPEG", "8"); done += 1; print(f"frame {i}/{N-1} {time.time()-t1:.0f}s", flush=True)
print("FRAMES_DONE", done, f"{time.time()-t0:.0f}s", flush=True)
