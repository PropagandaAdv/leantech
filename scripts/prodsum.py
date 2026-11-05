import sys, numpy as np
code = sys.argv[1]; d = np.load(f"work/{code}.npz")
V, F, FP, FC, prods, cols = d["V"], d["F"], d["FP"], d["FC"], d["prods"], d["cols"]
rows = []
for pi, name in enumerate(prods):
    m = FP == pi
    vi = np.unique(F[m].ravel()); v = V[vi] * 1000
    lo, hi = v.min(0), v.max(0); c = np.bincount(FC[m], minlength=len(cols)).argmax()
    ncol = len(np.unique(FC[m]))
    rows.append((m.sum(), name, (hi - lo).round(0), ((lo + hi) / 2).round(0), tuple(cols[c]), ncol))
rows.sort(key=lambda r: -r[0])
for n, name, sz, ctr, c, nc in rows: print(f"{n:6d} {name[:34]:34s} sz{sz.tolist()} ctr{ctr.tolist()} col{c} nc{nc}")
