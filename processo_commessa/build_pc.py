#!/usr/bin/env python3
"""Genera il widget HTML "Il processo di commessa" (Leantech / Engineering).
Uso: python3 -I build_pc.py videos.json out.html
videos.json: {"5": {"video": "URL.mp4", "poster": "URL.webp", "label": "descrizione"}, ...}
"""
import json, sys, html

PHASES = {
 1: ("Ordine e approvazione",
     "Dalla trattativa all’attivazione della commessa: la proposta d’ordine viene verificata rispetto al Budget e, se approvata, la commessa viene attivata sul gestionale."),
 2: ("Engineering",
     "Layout, approvazione del progetto e progettazione delle distinte base, poi inserite sul gestionale."),
 3: ("Materiali",
     "Dall’ordine cliente all’assegnazione dei materiali a commessa, con controllo fisico a magazzino: prelievo se disponibili, ordine fornitore se non lo sono."),
 4: ("Varianti in corso d’opera",
     "Nuovi accordi o varianti portano a rettifiche e a una revisione dell’ordine: il ciclo può ripetersi."),
 5: ("Chiusura",
     "Completamento della commessa e rientro a magazzino degli articoli non utilizzati, se riutilizzabili."),
}

# id: (numero mostrato, titolo, descrizione, fase, corsia_cliente)
N = {
 "1":  ("01", "Gestione commessa", "Il Committente gestisce gli aspetti burocratici e la trattativa con i propri clienti: da qui prende avvio la commessa.", 1, True),
 "2":  ("02", "Proposta ordine cliente", "Dalla trattativa nasce la proposta d’ordine del cliente, che viene sottoposta a Leantech.", 1, False),
 "3":  ("03", "Verifica proposta rispetto a Budget da parte della direzione", "La direzione verifica la proposta rispetto al Budget. L’esito è l’approvazione oppure il rifiuto dell’ordine cliente.", 1, False),
 "4":  ("04", "Aggiornamento elenco commesse e attivazione della nuova commessa sul gestionale", "Con l’ordine approvato, l’elenco commesse viene aggiornato e la nuova commessa viene attivata sul gestionale.", 1, False),
 "5":  ("05", "Disegno del layout commessa da parte dell’Ufficio Tecnico", "L’Ufficio Tecnico disegna il layout della commessa.", 2, False),
 "6":  ("06", "Approvazione progetto da parte del Committente e del cliente", "Il progetto viene approvato dal Committente e dal cliente. Se necessario si effettuano modifiche, rimanendo nei limiti di Budget.", 2, False),
 "7":  ("07", "Progettazione distinte base da parte dell’Ufficio Tecnico interno", "L’Ufficio Tecnico interno progetta le distinte base, per ogni gruppo e sottogruppo.", 2, False),
 "8":  ("08", "Inserimento distinte di base sul gestionale", "Le distinte base vengono inserite sul sistema gestionale.", 2, False),
 "9":  ("09", "Ordine cliente (sul gestionale)", "L’ordine cliente viene gestito sul gestionale.", 3, False),
 "10": ("10", "Assegnazione materiali a commessa", "I materiali vengono assegnati alla commessa.", 3, False),
 "11": ("11", "Controllo fisico a magazzino delle disponibilità", "Si controlla fisicamente a magazzino la disponibilità degli articoli. Da qui il percorso si divide: articoli disponibili oppure non disponibili.", 3, False),
 "11a": ("11a", "Prelievo materiali da magazzino centrale (carico su commessa)", "Gli articoli disponibili e fisicamente presenti a magazzino vengono prelevati dal magazzino centrale e caricati sulla commessa.", 3, False),
 "11b": ("11b", "Ordine fornitore (acquisto materiali imputati direttamente alla commessa)", "Per gli articoli non disponibili si effettua l’ordine al fornitore: i materiali acquistati sono imputati direttamente alla commessa.", 3, False),
 "12": ("12", "Rettifiche/modifiche alla commessa derivanti da nuovi accordi o varianti in corso d’opera", "Nuovi accordi o varianti in corso d’opera possono portare rettifiche o modifiche alla commessa.", 4, False),
 "13": ("13", "Revisione ordine cliente", "L’ordine cliente viene rivisto manualmente tramite gestionale, per ogni gruppo e sottogruppo modificato. Le modifiche possono essere riduttive o integrative.", 4, False),
 "13a": ("13a", "Rilancio dell’ordine cliente per i materiali aggiuntivi", "Con una modifica integrativa l’ordine cliente viene rilanciato per i materiali aggiuntivi.", 4, False),
 "13b": ("13b", "Rilancio assegnazione materiali a commessa", "Si rilancia l’assegnazione dei materiali alla commessa.", 4, False),
 "13c": ("13c", "Controllo fisico a magazzino", "Si ripete il controllo fisico a magazzino. Poi, come in Fase 3: prelievo da magazzino centrale oppure ordine fornitore.", 4, False),
 "14": ("14", "Ulteriori rettifiche/modifiche alla commessa", "Ulteriori rettifiche o modifiche possono intervenire in seguito: il ciclo può ripetersi.", 4, False),
 "15": ("15", "Completamento commessa", "La commessa viene completata. Segue la chiusura, con lo scarico degli articoli non utilizzati.", 5, False),
 "16": ("16", "Scarico da commessa e carico a magazzino centrale degli articoli non utilizzati", "Gli articoli non utilizzati vengono scaricati dalla commessa e caricati a magazzino centrale, solo se riutilizzabili per altre commesse.", 5, False),
}
ORDER = list(N.keys())

VID = {}
if len(sys.argv) > 1:
    VID = json.load(open(sys.argv[1]))

e = html.escape

def node(i, nx=False):
    num, title, desc, ph, client = N[i]
    v = VID.get(i)
    attrs = f'data-id="{i}" data-ph="{ph}"'
    if v:
        attrs += f' data-video="{e(v["video"])}" data-poster="{e(v["poster"])}" data-label="{e(v["label"])}"'
    cls = "pc-n" + (" nx" if nx else "") + (" is-client" if client else "")
    lane = '<span class="pc-lane">Cliente / Committente</span>' if client else ''
    return (f'<li class="{cls}" {attrs}><button type="button" class="pc-b" aria-expanded="false" aria-controls="pc-d-{i}">'
            f'<span class="pc-num">{num}</span>{lane}<span class="pc-t">{e(title)}</span></button>'
            f'<div class="pc-d" id="pc-d-{i}"><p class="pc-desc">{e(desc)}</p><div class="pc-v"></div></div></li>')

def out(text, nx=False, extra=""):
    return f'<li class="pc-o{" nx" if nx else ""}{extra}"><span>{e(text)}</span></li>'

def row(*cells, cls=""):
    return f'<ol class="pc-row {cls}">' + "".join(cells) + '</ol>'

def cell(inner, cls=""):
    return f'<li class="pc-cell {cls}">{inner}</li>'

DN = '<span class="pc-dn" aria-hidden="true"></span>'

flows = {}
flows[1] = row(
    node("1", True), node("2", True), node("3", True),
    cell('<ul class="pc-col">' + out("Rifiuto ordine cliente") + out("Approvazione ordine cliente", True) + '</ul>'),
    node("4"))
flows[2] = row(node("5", True), node("6", True), node("7", True), node("8"))
flows[3] = row(
    node("9", True), node("10", True), node("11", True),
    cell('<ul class="pc-col">'
         '<li>' + row(out("Articoli disponibili e fisicamente presenti a magazzino", True), node("11a"), cls="pc-sub") + '</li>'
         '<li>' + row(out("Articoli non disponibili", True), node("11b"), cls="pc-sub") + '</li>'
         '</ul>', "pc-wide"))
flows[4] = (
    row(node("12", True), node("13", True),
        cell('<ul class="pc-col">' + out("Modifiche riduttive") + out("Modifiche integrative", False, " pc-dnx") + '</ul>'))
    + DN +
    row(node("13a", True), node("13b", True), node("13c", True),
        out("Come in Fase 3: prelievo da magazzino centrale oppure ordine fornitore"))
    + DN +
    row(node("14"), '<li class="pc-loop"><span aria-hidden="true">↻</span> Il ciclo può ripetersi: si torna al passaggio 12</li>'))
flows[5] = row(node("15", True), node("16"))

phases_html = ""
for p in range(1, 6):
    t, s = PHASES[p]
    phases_html += (f'<li class="pc-phase{" pc-cycle" if p == 4 else ""}" id="pc-f{p}">'
                    f'<header class="pc-ph"><p class="pc-k">Fase {p} di 5</p><h3>{e(t)}</h3><p class="pc-s">{e(s)}</p></header>'
                    f'<div class="pc-flow">{flows[p]}</div></li>')

CSS = """
#processo-commessa{--pc-ink:#0C2434;--pc-text:#4A5560;--pc-line:#6E8494;--pc-soft:#C7D5DE;--pc-accent:#1D8AC9;--pc-accent2:#5FB8E8;--pc-bg:#F8F9FA;font-family:var(--e-global-typography-text-font-family,Roboto),Roboto,sans-serif;color:var(--pc-text);width:100%}
#processo-commessa *{box-sizing:border-box}
#processo-commessa ol,#processo-commessa ul{list-style:none;margin:0;padding:0}
#processo-commessa p{margin:0}
.pc-legend{display:flex;flex-wrap:wrap;gap:12px 28px;font-size:14px;margin:0 0 28px;color:var(--pc-ink)}
.pc-legend span{display:inline-flex;align-items:center;gap:8px}
.pc-legend i{display:inline-block;width:34px;height:18px;border-radius:5px;border:2px solid var(--pc-line);background:#fff}
.pc-legend i.d{border-style:dashed;background:transparent}
.pc-legend i.c{border-color:var(--pc-accent)}
.pc-phases{display:flex;flex-direction:column;gap:22px}
.pc-phase{display:grid;grid-template-columns:210px 1fr;gap:32px;padding:26px;background:#fff;border:1px solid var(--pc-soft);border-radius:16px;border-left:5px solid var(--pc-accent)}
.pc-k{font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--pc-ink)}
.pc-ph h3{margin:6px 0 8px;font-size:21px;line-height:1.2;font-weight:700;color:var(--pc-ink)}
.pc-s{font-size:14px;line-height:1.55}
.pc-flow{display:flex;flex-direction:column;gap:18px;min-width:0}
.pc-row{display:flex;align-items:center;gap:30px}
.pc-row>li{flex:1 1 0;min-width:0;position:relative}
.pc-row>li.pc-wide{flex:2.3 1 0}
.pc-col{display:flex;flex-direction:column;gap:14px}
.pc-sub{gap:30px}
.nx::after{content:"→" / "";position:absolute;right:-26px;top:50%;transform:translateY(-50%);width:22px;text-align:center;font-size:20px;line-height:1;color:var(--pc-accent)}
.pc-b{display:flex;flex-direction:column;align-items:flex-start;gap:7px;width:100%;min-height:44px;text-align:left;font:inherit;font-size:14px;line-height:1.35;color:var(--pc-ink);background:#fff;border:2px solid var(--pc-line);border-radius:12px;padding:12px;cursor:pointer}
.pc-b,.pc-nav button,.pc-play{white-space:normal;text-transform:none;letter-spacing:normal;text-decoration:none;transition:none;-webkit-appearance:none;appearance:none}
.pc-b:hover,.pc-b:focus,.pc-b:active{background:#fff;color:var(--pc-ink);border-color:var(--pc-accent);text-decoration:none}
.pc-b[aria-expanded="false"]:focus:not(:hover):not(:focus-visible){border-color:var(--pc-line)}
.pc-b:focus-visible,.pc-panel button:focus-visible{outline:3px solid var(--pc-ink);outline-offset:2px}
.pc-b[aria-expanded="true"]{border-color:var(--pc-accent);box-shadow:0 0 0 3px rgba(29,138,201,.28)}
.is-prev .pc-b{border-color:var(--pc-accent)}
.is-prev.nx::after{font-weight:700;color:var(--pc-ink)}
.is-client .pc-b{border-color:var(--pc-accent)}
.pc-num{font-size:12px;font-weight:700;letter-spacing:.08em;color:#fff;background:var(--pc-ink);border-radius:6px;padding:2px 7px}
.pc-lane{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--pc-ink)}
.pc-t{font-weight:600}
.pc-o{border:2px dashed var(--pc-line);border-radius:12px;padding:11px 12px;font-size:13.5px;line-height:1.35;color:var(--pc-ink);min-height:44px;display:flex;align-items:center}
.pc-loop{font-size:14px;font-weight:600;color:var(--pc-ink);border-top:2px solid var(--pc-accent);padding-top:10px}
.pc-loop span{font-size:20px;color:var(--pc-accent);margin-right:4px}
.pc-cycle .pc-flow{border-left:3px dashed var(--pc-accent);padding-left:18px}
.pc-dn{display:block;height:14px;text-align:center;position:relative}
.pc-dn::after{content:"↓" / "";position:absolute;right:11%;top:-4px;font-size:20px;color:var(--pc-accent)}
.pc-d{margin-top:8px;font-size:14px;line-height:1.55}
.pc-v{display:none}
.pc-panel{margin:0;border-radius:16px;background:var(--pc-ink);color:#fff;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);overflow:hidden}
.pc-panel[hidden]{display:none}
.pc-phase>.pc-panel{grid-column:1/-1;margin-top:4px}
.pc-pv{background:#06141d;aspect-ratio:16/9;position:relative}
.pc-pv:empty{display:none}
.pc-pv:empty+.pc-pb{grid-column:1/-1}
.pc-pb{padding:26px 28px;display:flex;flex-direction:column;gap:10px}
.pc-pk{font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#C7D5DE}
.pc-pt{margin:0;font-size:22px;line-height:1.25;font-weight:700;color:#fff}
.pc-pd{font-size:16px;line-height:1.6;color:#fff}
.pc-nav{display:flex;gap:12px;margin-top:8px}
.pc-nav button{font:inherit;font-size:14px;font-weight:600;color:#fff;background:transparent;border:2px solid #C7D5DE;border-radius:8px;padding:9px 16px;min-height:44px;cursor:pointer}
.pc-nav button:hover,.pc-nav button:active{background:#fff;color:var(--pc-ink);border-color:#C7D5DE}
.pc-nav button:focus:not(:hover){background:transparent;color:#fff}
.pc-nav button:disabled{opacity:.45;cursor:default;background:transparent;color:#fff}
#processo-commessa video{display:block;width:100%;height:100%;object-fit:cover;background:#06141d}
.pc-play{position:absolute;right:14px;bottom:14px;width:48px;height:48px;border-radius:50%;border:2px solid #fff;background:rgba(12,36,52,.85);cursor:pointer;padding:0}
.pc-play:hover,.pc-play:focus{background:rgba(12,36,52,.85)}
.pc-play::before{content:"";position:absolute;left:19px;top:13px;border-left:15px solid #fff;border-top:10px solid transparent;border-bottom:10px solid transparent}
.pc-js .pc-d{display:none}
.pc-js .pc-d .pc-desc{display:block}
.pc-js .pc-n.is-open .pc-d{display:block}
.pc-js .pc-n.is-open .pc-v{display:block;aspect-ratio:16/9;margin-top:10px;position:relative;border-radius:10px;overflow:hidden;background:#06141d}
.pc-js .pc-n.is-open .pc-v:empty{display:none}
@media (min-width:1024px){.pc-js .pc-n.is-open .pc-d{display:none}}
@media (max-width:1023px){
.pc-phase{display:block;padding:20px 16px;border-left-width:5px}
.pc-ph{margin-bottom:16px}
.pc-row{flex-direction:column;align-items:stretch;gap:26px}
.pc-row>li,.pc-row>li.pc-wide{flex:none}
.pc-sub{gap:22px}
.pc-col{margin-left:0;gap:22px}
.pc-col .pc-col,.pc-wide .pc-col{margin-left:14px}
.nx::after{content:"↓" / "";right:auto;left:50%;top:auto;bottom:-27px;transform:translateX(-50%)}
.pc-dn::after{right:auto;left:50%;transform:translateX(-50%)}
.pc-cycle .pc-flow{padding-left:12px}
.pc-panel{display:none}
}
@media (prefers-reduced-motion:reduce){#processo-commessa *{scroll-behavior:auto!important;transition:none!important}}
"""

JS = r"""
(function(){var R=document.getElementById('processo-commessa');if(!R||R.__pc){return;}R.__pc=1;R.classList.add('pc-js');
var mq=window.matchMedia('(min-width:1024px)'),rm=window.matchMedia('(prefers-reduced-motion: reduce)');
var nodes=[].slice.call(R.querySelectorAll('.pc-n')),panel=R.querySelector('.pc-panel'),pv=panel.querySelector('.pc-pv'),pk=panel.querySelector('.pc-pk'),pt=panel.querySelector('.pc-pt'),pd=panel.querySelector('.pc-pd'),bp=panel.querySelector('.pc-prev'),bn=panel.querySelector('.pc-next');
var cur=-1,vid=null,vhost=null;
function stop(){if(vid){try{vid.pause();vid.removeAttribute('src');vid.load();}catch(x){}}if(vhost){vhost.innerHTML='';}vid=null;vhost=null;}
function mount(host,n,auto){stop();var u=n.getAttribute('data-video');if(!u){return;}vhost=host;
var v=document.createElement('video');v.muted=true;v.defaultMuted=true;v.loop=true;v.setAttribute('playsinline','');v.setAttribute('muted','');v.preload='none';v.setAttribute('aria-label',n.getAttribute('data-label')||'');
var po=n.getAttribute('data-poster');if(po){v.poster=po;}
host.appendChild(v);vid=v;
function go(){v.src=u;var p=v.play();if(p&&p.catch){p.catch(function(){});}var b=host.querySelector('.pc-play');if(b){b.remove();}}
if(auto&&!rm.matches){go();}else{var b=document.createElement('button');b.type='button';b.className='pc-play';b.setAttribute('aria-label','Riproduci il video');b.addEventListener('click',go);host.appendChild(b);}}
function txt(n){return{t:n.querySelector('.pc-t').textContent,d:n.querySelector('.pc-desc').textContent,ph:n.getAttribute('data-ph'),num:n.querySelector('.pc-num').textContent};}
function open(i,user){var n=nodes[i];if(!n){return;}var dsk=mq.matches;
nodes.forEach(function(x,k){var on=k===i;x.classList.toggle('is-prev',k===i-1);x.classList.toggle('is-open',!dsk&&on);var b=x.querySelector('.pc-b');b.setAttribute('aria-expanded',on?'true':'false');b.setAttribute('aria-controls',dsk?'pc-panel':'pc-d-'+x.getAttribute('data-id'));});
cur=i;
if(dsk){var d=txt(n);panel.hidden=false;n.closest('.pc-phase').appendChild(panel);
pk.textContent='Fase '+d.ph+' di 5 · Passaggio '+d.num;pt.textContent=d.t;pd.textContent=d.d;bp.disabled=i===0;bn.disabled=i===nodes.length-1;
mount(pv,n,!!user);}
else{panel.hidden=true;mount(n.querySelector('.pc-v'),n,!!user);}}
function toggleMobile(i){if(cur===i&&nodes[i].classList.contains('is-open')){nodes[i].classList.remove('is-open');nodes[i].querySelector('.pc-b').setAttribute('aria-expanded','false');stop();cur=-1;}else{open(i,true);}}
nodes.forEach(function(n,i){n.querySelector('.pc-b').addEventListener('click',function(){if(mq.matches){open(i,true);}else{toggleMobile(i);}});});
bp.addEventListener('click',function(){if(cur>0){open(cur-1,true);nodes[cur].querySelector('.pc-b').focus();}});
bn.addEventListener('click',function(){if(cur<nodes.length-1){open(cur+1,true);nodes[cur].querySelector('.pc-b').focus();}});
R.addEventListener('keydown',function(ev){var b=ev.target.closest&&ev.target.closest('.pc-b');if(!b){return;}var i=nodes.indexOf(b.parentNode),k=-1;
if(ev.key==='ArrowRight'||ev.key==='ArrowDown'){k=Math.min(i+1,nodes.length-1);}else if(ev.key==='ArrowLeft'||ev.key==='ArrowUp'){k=Math.max(i-1,0);}else if(ev.key==='Home'){k=0;}else if(ev.key==='End'){k=nodes.length-1;}
if(k>=0){ev.preventDefault();nodes[k].querySelector('.pc-b').focus();}});
var last=mq.matches;function onmq(){if(mq.matches!==last){last=mq.matches;stop();open(cur<0?0:cur,false);}}
if(mq.addEventListener){mq.addEventListener('change',onmq);}else if(mq.addListener){mq.addListener(onmq);}
open(0,false);if(!mq.matches){nodes[0].classList.remove('is-open');nodes[0].querySelector('.pc-b').setAttribute('aria-expanded','false');}
})();
"""

PANEL = ('<aside class="pc-panel" id="pc-panel" role="region" aria-live="polite" aria-label="Dettaglio del passaggio selezionato" hidden>'
         '<div class="pc-pv"></div><div class="pc-pb"><p class="pc-pk"></p><h4 class="pc-pt"></h4><p class="pc-pd"></p>'
         '<div class="pc-nav"><button type="button" class="pc-prev">← Precedente</button><button type="button" class="pc-next">Successivo →</button></div></div></aside>')

LEGEND = ('<div class="pc-legend" aria-label="Legenda"><span><i></i>Attività principale (Leantech)</span>'
          '<span><i class="c"></i>Attività del Cliente / Committente</span>'
          '<span><i class="d"></i>Esito, decisione o stato</span></div>')

doc = (f'<style>{CSS.strip()}</style>'
       f'<div id="processo-commessa" role="group" aria-label="Il processo di commessa Leantech">{LEGEND}'
       f'<ol class="pc-phases">{phases_html}</ol>{PANEL}</div>'
       f'<script>{JS.strip()}</script>')
open(sys.argv[2] if len(sys.argv) > 2 else "pc_widget.html", "w", encoding="utf-8").write(doc)
print(len(doc), "bytes", len(ORDER), "nodi")
