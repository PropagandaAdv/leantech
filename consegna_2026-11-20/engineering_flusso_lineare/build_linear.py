#!/usr/bin/env python3
"""Diagramma di flusso LINEARE del processo di commessa (Leantech / Engineering).
Uso: python3 -I build_linear.py videos.json out.html
Nessun pannello/accordion: tutto visibile. JS solo per il lightbox video (opzionale).
"""
import json, sys, html
e = html.escape
VID = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}

# chiave: (testo del box, id video | None)
T = {
 "1":  "Gestione commessa: operazioni burocratiche, trattativa con i clienti",
 "2":  "Proposta ordine cliente",
 "3":  "Verifica proposta rispetto a Budget da parte della direzione",
 "4":  "Aggiornamento elenco commesse e attivazione della nuova commessa sul gestionale",
 "5":  "Disegno del layout commessa da parte dell’Ufficio Tecnico",
 "6":  "Approvazione progetto da parte del cliente (se necessarie si effettuano modifiche, rimanendo nei limiti di Budget)",
 "7":  "Progettazione distinte base da parte dell’Ufficio Tecnico interno (per ogni gruppo e sottogruppo)",
 "8":  "Inserimento distinte di base sul gestionale",
 "9":  "Ordine cliente (sul gestionale)",
 "10": "Assegnazione materiali a commessa",
 "11": "Controllo fisico a magazzino delle disponibilità",
 "11a": "Prelievo materiali da magazzino centrale (carico su commessa)",
 "11b": "Ordine fornitore (acquisto materiali imputati direttamente alla commessa)",
 "12": "Rettifiche/modifiche alla commessa derivanti da nuovi accordi o varianti in corso d’opera",
 "13": "Revisione ordine cliente (revisione manuale, tramite gestionale, per ogni gruppo e sottogruppo modificato)",
 "13a": "Rilancio dell’ordine cliente per i materiali aggiuntivi",
 "13b": "Rilancio assegnazione materiali a commessa",
 "13c": "Controllo fisico a magazzino",
 "14": "Ulteriori rettifiche/modifiche alla commessa",
 "15": "Completamento commessa",
 "16": "Scarico da commessa e carico a magazzino centrale degli articoli non utilizzati (solo se riutilizzabili per altre commesse)",
}
ARW = ('<span class="lf-arr" aria-hidden="true"><svg viewBox="0 0 28 16" focusable="false"><path d="M1 8h22M17 2l7 6-7 6" '
       'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>')

def box(i, arrow=True):
    v = VID.get(i)
    play = ''
    if v:
        play = (f'<button type="button" class="lf-play" data-video="{e(v["video"])}" data-poster="{e(v["poster"])}" '
                f'data-label="{e(v["label"])}" aria-label="Guarda il video: {e(T[i])}"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
                f'<circle cx="12" cy="12" r="11" fill="currentColor"/><path d="M9.5 7.5v9l7-4.5z" fill="#fff"/></svg></button>')
    return f'<li class="lf-b">{e(T[i])}{play}{ARW if arrow else ""}</li>'

def out(text, arrow=False, cls=""):
    return f'<li class="lf-o {cls}">{e(text)}{ARW if arrow else ""}</li>'

def row(*c, cls=""):
    return f'<ol class="lf-row {cls}">' + "".join(c) + '</ol>'

def fork(*items, cls=""):
    return f'<li class="lf-fork {cls}"><ul class="lf-col">' + "".join(items) + '</ul></li>'

def pair(chip, b):
    return '<li>' + row(chip, b, cls="lf-pair") + '</li>'

DN = '<span class="lf-dn" aria-hidden="true"><svg viewBox="0 0 16 28" focusable="false"><path d="M8 1v22M2 17l6 7 6-7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'

lane1 = ('<section class="lf-lane lf-client" aria-labelledby="lf-l1"><h3 id="lf-l1" class="lf-lh">Cliente</h3>'
         + row(box("1", arrow=False)) + '</section>')
lane2 = ('<section class="lf-lane" aria-labelledby="lf-l2"><h3 id="lf-l2" class="lf-lh">Leantech</h3><div class="lf-flow">'
  + row(box("2"), box("3"), fork(out("Rifiuto ordine cliente"), out("Approvazione ordine cliente", True)), box("4", False)) + DN
  + row(box("5"), box("6"), box("7"), box("8", False)) + DN
  + row(box("9"), box("10"), box("11"),
        fork(pair(out("Articoli disponibili e fisicamente presenti a magazzino", True), box("11a", False)),
             pair(out("Articoli non disponibili", True), box("11b", False)), cls="lf-wide")) + DN
  + row(box("12"), box("13"), fork(out("Modifiche riduttive"), out("Modifiche integrative"))) + DN
  + row(box("13a"), box("13b"), box("13c"), out("Prelievo da magazzino centrale oppure ordine fornitore, come sopra", False)) + DN
  + row(box("14", False), '<li class="lf-loop"><span aria-hidden="true">↻</span> Il ciclo può ripetersi: si torna alle rettifiche/modifiche alla commessa</li>') + DN
  + row(box("15"), box("16", False))
  + '</div></section>')

LEG = ('<ul class="lf-leg" aria-label="Legenda"><li><i></i>Attività</li><li><i class="d"></i>Esito, decisione o stato</li></ul>')
DLG = ('<dialog class="lf-dlg" aria-label="Video"><div class="lf-dv"></div><button type="button" class="lf-x" aria-label="Chiudi il video">×</button></dialog>')

CSS = """
#lf-processo{--lf-ink:#0C2434;--lf-text:#4A5560;--lf-line:#6E8494;--lf-soft:#C7D5DE;--lf-accent:#1D8AC9;font-family:var(--e-global-typography-text-font-family,Roboto),Roboto,sans-serif;color:var(--lf-text);width:100%}
#lf-processo *{box-sizing:border-box}
#lf-processo ol,#lf-processo ul{list-style:none;margin:0;padding:0}
.lf-leg{display:flex;gap:24px;margin:0 0 22px!important;font-size:14px;color:var(--lf-ink)}
.lf-leg li{display:inline-flex;align-items:center;gap:8px}
.lf-leg i{display:inline-block;width:34px;height:18px;border:2px solid var(--lf-line);border-radius:5px;background:#fff}
.lf-leg i.d{border-style:dashed;background:transparent}
.lf-lane{background:#fff;border:1px solid var(--lf-soft);border-left:5px solid var(--lf-accent);border-radius:16px;padding:22px 26px 26px;margin:0 0 18px}
.lf-client{border-left-color:var(--lf-ink)}
.lf-lh{margin:0 0 16px;font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--lf-ink)}
.lf-flow{display:flex;flex-direction:column;gap:14px}
.lf-row{display:flex;align-items:center;gap:34px}
.lf-row>li{flex:1 1 0;min-width:0;position:relative}
.lf-row>li.lf-wide{flex:2.4 1 0}
.lf-client .lf-row>li{flex:0 1 25%}
.lf-b{border:2px solid var(--lf-line);border-radius:12px;background:#fff;color:var(--lf-ink);font-size:14px;line-height:1.4;font-weight:600;padding:13px 14px;min-height:56px;display:flex;align-items:center;gap:8px;position:relative}
.lf-o{border:2px dashed var(--lf-line);border-radius:12px;color:var(--lf-ink);font-size:13.5px;line-height:1.4;padding:11px 12px;min-height:44px;display:flex;align-items:center;position:relative}
.lf-col{display:flex;flex-direction:column;gap:12px}
.lf-pair{gap:34px}
.lf-arr{position:absolute;right:-30px;top:50%;transform:translateY(-50%);width:26px;height:16px;color:var(--lf-accent);display:block}
.lf-arr svg{display:block;width:100%;height:100%}
.lf-dn{display:block;height:24px;color:var(--lf-accent);text-align:center}
.lf-dn svg{width:14px;height:24px}
.lf-loop{font-size:14px;font-weight:600;color:var(--lf-ink);border-top:2px solid var(--lf-accent);padding-top:10px}
.lf-loop span{font-size:20px;color:var(--lf-accent);margin-right:4px}
.lf-play{flex:0 0 auto;margin-left:auto;width:32px;height:32px;padding:0;border:0;background:transparent;color:var(--lf-accent);cursor:pointer;border-radius:50%;line-height:0;white-space:normal;text-transform:none;letter-spacing:normal;-webkit-appearance:none;appearance:none}
.lf-play svg{width:32px;height:32px}
.lf-play:hover,.lf-play:focus{background:transparent;color:var(--lf-ink)}
.lf-play:focus-visible,.lf-x:focus-visible{outline:3px solid var(--lf-ink);outline-offset:2px}
.lf-dlg{border:0;padding:0;border-radius:14px;overflow:hidden;width:min(960px,92vw);background:#06141d}
.lf-dlg::backdrop{background:rgba(6,20,29,.82)}
.lf-dv{aspect-ratio:16/9;position:relative}
.lf-dv video{display:block;width:100%;height:100%;object-fit:cover;background:#06141d}
.lf-x{position:absolute;top:10px;right:10px;width:44px;height:44px;border-radius:50%;border:2px solid #fff;background:rgba(12,36,52,.85);color:#fff;font-size:26px;line-height:1;padding:0;cursor:pointer;-webkit-appearance:none;appearance:none}
.lf-x:hover,.lf-x:focus{background:rgba(12,36,52,.85);color:#fff}
@media (max-width:1023px){
.lf-lane{padding:18px 14px 20px}
.lf-row{flex-direction:column;align-items:stretch;gap:30px}
.lf-row>li,.lf-row>li.lf-wide,.lf-client .lf-row>li{flex:none}
.lf-pair{gap:30px}
.lf-col{margin-left:16px;gap:28px}
.lf-arr{right:auto;left:50%;top:auto;bottom:-27px;transform:translateX(-50%) rotate(90deg)}
.lf-leg{flex-wrap:wrap;gap:10px 20px}
}
@media (prefers-reduced-motion:reduce){#lf-processo *{scroll-behavior:auto!important;transition:none!important}}
"""

JS = r"""(function(){var R=document.getElementById('lf-processo');if(!R||R.__lf){return;}R.__lf=1;
var d=R.querySelector('.lf-dlg'),h=R.querySelector('.lf-dv'),x=R.querySelector('.lf-x'),rm=window.matchMedia('(prefers-reduced-motion: reduce)'),last=null;
if(!d||typeof d.showModal!=='function'){[].forEach.call(R.querySelectorAll('.lf-play'),function(b){b.hidden=true;});return;}
function close(){var v=h.querySelector('video');if(v){try{v.pause();v.removeAttribute('src');v.load();}catch(e){}}h.innerHTML='';if(d.open){d.close();}if(last){last.focus();}}
[].forEach.call(R.querySelectorAll('.lf-play'),function(b){b.addEventListener('click',function(){last=b;h.innerHTML='';
var v=document.createElement('video');v.muted=true;v.loop=true;v.setAttribute('playsinline','');v.setAttribute('muted','');v.preload='none';v.setAttribute('aria-label',b.getAttribute('data-label')||'');
v.poster=b.getAttribute('data-poster')||'';if(rm.matches){v.controls=true;}h.appendChild(v);d.setAttribute('aria-label',b.getAttribute('data-label')||'Video');d.showModal();
v.src=b.getAttribute('data-video');if(!rm.matches){var p=v.play();if(p&&p.catch){p.catch(function(){});}}x.focus();});});
x.addEventListener('click',close);d.addEventListener('cancel',function(e){e.preventDefault();close();});
d.addEventListener('click',function(e){if(e.target===d){close();}});})();"""

doc = (f'<style>{CSS.strip()}</style><div id="lf-processo" role="group" aria-label="Il processo di commessa Leantech">{LEG}{lane1}{lane2}{DLG}</div>'
       f'<script>{JS.strip()}</script>')
open(sys.argv[2] if len(sys.argv) > 2 else "pc_linear.html", "w", encoding="utf-8").write(doc)
print(len(doc), "bytes")
