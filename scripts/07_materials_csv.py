import sys, glob, re, csv, numpy as np, collections; sys.path.insert(0, "scripts")
from materials_rules import classify
rows = collections.OrderedDict()
for p in sorted(glob.glob("work/PX*.npz")):
    code = re.search(r"(PX\d+)", p).group(1)
    if code == "PX0000381686": continue     # assieme senza colori CAD: stesse parti dei nastri
    d = np.load(p); FP, FC, prods, cols = d["FP"], d["FC"], d["prods"], d["cols"]
    key = FP.astype(np.int64) * 1000 + FC
    u, cnt = np.unique(key, return_counts=True)
    for k, c in zip(u, cnt):
        prod, col = str(prods[k // 1000]), tuple(int(x) for x in cols[k % 1000])
        e = rows.setdefault((prod, col), [0, set()]); e[0] += int(c); e[1].add(code)
out = []
for (prod, col), (n, files) in rows.items():
    fam, conf, note = classify(prod, col)
    out.append([prod, "%d,%d,%d" % col, fam, conf, note, n, " ".join(sorted(files))])
out.sort(key=lambda r: (r[2], -r[5]))
with open("reports/materials_map.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["componente", "colore_CAD", "famiglia_materiale", "confidenza", "nota", "facce_totali", "presente_in"]); w.writerows(out)
c = collections.Counter(); cc = collections.Counter()
for r in out: c[r[2]] += 1; cc[r[3]] += 1
print(dict(c)); print(dict(cc), len(out), "righe")
