"""Struttura compatta per codice (da work/<codice>.npz): bbox totale e riepilogo per prodotto -> reports/<codice>_struttura.json
Assi in metri->mm, sistema glTF: X larghezza, Y verticale, Z lunghezza."""
import json, glob, re, numpy as np
for p in sorted(glob.glob("work/PX*.npz")):
    code = re.search(r"(PX\d+)", p).group(1); d = np.load(p)
    V, F, FP, FC, prods, cols = d["V"], d["F"], d["FP"], d["FC"], d["prods"], d["cols"]
    lo, hi = V.min(0) * 1000, V.max(0) * 1000; out = []
    for pi, name in enumerate(prods):
        m = FP == pi; v = V[np.unique(F[m].ravel())] * 1000
        out.append(dict(product=str(name), faces=int(m.sum()), bbox_min=v.min(0).round(1).tolist(), bbox_max=v.max(0).round(1).tolist(),
                        cad_colors=[[int(x) for x in cols[c]] for c in np.unique(FC[m])]))
    out.sort(key=lambda r: -r["faces"])
    json.dump(dict(file=code, products=len(out), faces=int(len(F)), bbox_mm=dict(min=lo.round(1).tolist(), max=hi.round(1).tolist(), size=(hi - lo).round(1).tolist()), items=out),
              open(f"reports/{code}_struttura.json", "w"), indent=1)
    print(code, len(out), "prodotti", (hi - lo).round(0).tolist())
