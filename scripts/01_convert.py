"""STEP -> GLB (one file at a time, memory-safe). Usage: 01_convert.py [code ...]"""
import sys, glob, os, time, cascadio
codes = sys.argv[1:] or ["PX0000381771","PX0000381774","PX0000381735","PX0000381687","PX0000380493","PX0000381782","PX0000381686"]
for c in codes:
    src = glob.glob(f"input/{c}-*.[sS][tT][eE][pP]")[0]
    out = f"work/{c}.glb"
    t = time.time()
    # 0.1 mm linear deflection, 0.5 rad angular; keep one primitive per part (names preserved)
    cascadio.step_to_glb(src, out, 0.1, 0.5, merge_primitives=False, use_parallel=True)
    print(c, f"{time.time()-t:.0f}s", f"{os.path.getsize(out)/1e6:.1f} MB", flush=True)
