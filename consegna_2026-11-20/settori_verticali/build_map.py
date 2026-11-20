#!/usr/bin/env python3
"""Mappa dei settori: LEANTECH al centro, 6 verticali (2 colonne x 3 righe). HTML+CSS, SVG aria-hidden per le linee."""
import html
e = html.escape
V = [("V01", "PARCEL & EXPRESS"), ("V02", "FASHION, E-COMMERCE & 3PL"), ("V03", "PHARMA & COSMETICS"),
     ("V04", "COLD CHAIN"), ("V05", "GROCERY & GDO"), ("V06", "OEM & SYSTEM INTEGRATOR")]
tiles = "".join(
    f'<li class="sm-t sm-{c.lower()}"><a href="#{c.lower()}"><span class="sm-c">{c}</span><span class="sm-n">{e(n)}</span></a></li>'
    for c, n in V)
# linee: tile edge (34 / 66) -> centro (40 / 60, y=50); centri riga 1/6, 3/6, 5/6
ys = [100/6, 50, 500/6]
lines = ""
for i, y in enumerate(ys):
    lines += f'<line x1="34" y1="{y:.2f}" x2="40" y2="50"/><line x1="66" y1="{y:.2f}" x2="60" y2="50"/>'
CSS = """
#settori-map{--m-ink:#0C2434;--m-text:#4A5560;--m-line:#6E8494;--m-soft:#C7D5DE;--m-accent:#1D8AC9;font-family:var(--e-global-typography-text-font-family,Roboto),Roboto,sans-serif;width:100%}
#settori-map *{box-sizing:border-box}
#settori-map ul{list-style:none;margin:0;padding:0}
.sm-g{position:relative;display:grid;grid-template-columns:34% 6% 20% 6% 34%;grid-template-rows:repeat(3,1fr);min-height:420px;align-items:stretch}
.sm-tl{display:contents}
.sm-svg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}
.sm-svg line{stroke:var(--m-line);stroke-width:1.5;vector-effect:non-scaling-stroke;opacity:.75}
.sm-center{grid-column:3;grid-row:1/4;align-self:center;z-index:1;background:var(--m-ink);color:#fff;border-radius:14px;padding:26px 12px;text-align:center;font-size:clamp(16px,2vw,24px);font-weight:700;letter-spacing:.12em}
.sm-t{margin:10px 0;display:flex;z-index:1}
.sm-t a{display:flex;flex-direction:column;justify-content:center;gap:8px;width:100%;padding:18px 22px;background:#F8F9FA;border:1px solid var(--m-soft);border-radius:14px;color:var(--m-ink);text-decoration:none;transition:border-color .15s,box-shadow .15s}
.sm-t a:hover,.sm-t a:focus{border-color:var(--m-accent);box-shadow:0 4px 14px rgba(12,36,52,.10);color:var(--m-ink);background:#F8F9FA}
.sm-t a:focus-visible{outline:3px solid var(--m-ink);outline-offset:2px}
.sm-c{font-size:12px;font-weight:700;letter-spacing:.1em;color:var(--m-text)}
.sm-n{font-size:clamp(15px,1.7vw,20px);font-weight:700;line-height:1.25;letter-spacing:.02em}
.sm-v01{grid-column:1;grid-row:1}.sm-v03{grid-column:1;grid-row:2}.sm-v05{grid-column:1;grid-row:3}
.sm-v02{grid-column:5;grid-row:1}.sm-v04{grid-column:5;grid-row:2}.sm-v06{grid-column:5;grid-row:3}
@media (max-width:767px){
.sm-g{display:flex;flex-direction:column;gap:12px;min-height:0}
.sm-svg{display:none}
.sm-center{order:-1;grid-column:auto;padding:20px 12px;font-size:20px}
.sm-t{margin:0}
}
"""
doc = (f'<style>{CSS.strip()}</style><div id="settori-map" role="group" aria-label="Le sei verticali dell’intralogistica">'
       f'<div class="sm-g"><svg class="sm-svg" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true" focusable="false">{lines}</svg>'
       f'<div class="sm-center">LEANTECH</div><ul class="sm-tl" role="list">{tiles}</ul></div></div>')
open("map.html", "w", encoding="utf-8").write(doc)
print(len(doc), "bytes")
