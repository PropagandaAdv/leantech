#!/usr/bin/env python3
"""Genera il template Elementor della pagina /patrimonio-tecnico/ e il blocco riusabile.
Output: pt_page.json (array top-level), pt_block.json (blocco brevetto riusabile)."""
import json, random, html
random.seed(20261120)
def rid(): return "%08x" % random.getrandbits(32)
B = "https://leantech.propagandaadv.com/wp-content/uploads/2026/10/"
FONT = {"typography_font_family": "Roboto", "typography_typography": "custom"}
def px(n): return {"size": n, "unit": "px"}
def pad(t, r, b, l, m=False): return {"top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "unit": "px", "isLinked": False}
def gap(n): return {"column": str(n), "row": str(n), "size": n, "unit": "px", "isLinked": True}
def W(t, settings): return {"id": rid(), "elType": "widget", "widgetType": t, "settings": settings, "elements": []}
def C(settings, kids, inner=False): return {"id": rid(), "elType": "container", "settings": settings, "elements": kids, "isInner": inner}
def heading(title, tag="h2", color="#1E1E1E", size=38, msize=26, weight="700", extra=None):
    s = dict(FONT, header_size=tag, title=title, title_color=color, typography_font_size=px(size), typography_font_size_mobile=px(msize),
             typography_font_weight=weight, typography_line_height={"size": 1.2, "unit": "em"})
    if extra: s.update(extra)
    return W("heading", s)
def eyebrow(t, color="#1D8AC9"):
    return W("heading", dict(FONT, header_size="p", title=t, title_color=color, typography_font_size=px(14), typography_font_size_mobile=px(12),
                             typography_font_weight="600", typography_letter_spacing={"size": 2.5, "unit": "px"}))
def text(htmlp, color="#4A5560", size=19, width=None):
    s = dict(FONT, editor=htmlp, text_color=color, typography_font_size=px(size), typography_line_height={"size": 1.6, "unit": "em"})
    if width: s.update(width={"size": width, "unit": "%"}, width_mobile={"size": 100, "unit": "%"})
    return W("text-editor", s)
def section(eid, bg, kids):
    return C({"_element_id": eid, "background_background": "classic", "background_color": bg, "boxed_width": px(1280),
              "flex_direction": "column", "flex_direction_mobile": "column", "flex_gap": gap(48),
              "padding": pad(112, 48, 112, 48), "padding_mobile": pad(64, 20, 56, 20)}, kids)
def head_box(kids):
    return C({"animation": "fadeInUp", "animation_delay": 0, "animation_duration": "fast", "content_width": "full", "flex_direction": "column", "flex_gap": gap(16)}, kids, True)

# ---------------------------------------------------------------- HERO (stile /contattaci/)
hero = C({"_element_id": "sec-patrimonio-hero", "background_background": "video", "background_color": "#0C2434", "boxed_width": px(1280),
          "flex_align_items": "flex-start", "flex_direction": "row", "flex_direction_mobile": "column", "flex_direction_tablet": "column", "flex_gap": gap(56),
          "min_height": {"size": 50, "unit": "vh"},
          "padding": pad(160, 48, 96, 48), "padding_mobile": pad(110, 20, 64, 20), "padding_tablet": pad(140, 32, 80, 32),
          "background_video_link": B + "lt-sistema-nastro-maglia-dall-alto-loop.mp4",
          "background_video_fallback": {"url": B + "lt-sistema-nastro-maglia-dall-alto-loop-poster.webp"}},
         [C({"animation": "fadeInUp", "animation_delay": 0, "animation_duration": "fast", "content_width": "full", "flex_align_items": "flex-start",
             "flex_direction": "column", "flex_gap": gap(22), "width": {"size": 50, "unit": "%"}, "width_mobile": {"size": 100, "unit": "%"}, "width_tablet": {"size": 100, "unit": "%"}},
            [eyebrow("PATRIMONIO TECNICO", "#5FB8E8"),
             heading("Innovazione brevettata", "h1", "#FFFFFF", 54, 30, "700", {"typography_font_size_tablet": px(42), "typography_letter_spacing": {"size": -0.5, "unit": "px"}}),
             text("<p>Leantech ha depositato due brevetti: uno per l’intralogistica e uno per il clean design.</p>", "#C7D5DE")], True)])

# ---------------------------------------------------------------- STEPPER RAT 30° (HTML accessibile)
SLIDES = [
 ("VIDEO INTRALOGISTICA – IN PRODUZIONE", "Smistamento colli", "video"),
 ("LAYOUT 5000 CPH – DWG su sfondo bianco", "Il layout complessivo da 5000 CPH", "layout"),
 ("LAYOUT con cornice rossa sulla zona da ingrandire", "La zona del layout da ingrandire", "layout-cornice"),
 ("INGRANDIMENTO della zona, con cornice rossa", "Ingrandimento della zona", "zoom"),
 ("RENDER RAT 30° – BANCO SINGOLO a 3 file di ruote", "RAT 30°: banco singolo a 3 file di ruote", "render-singolo"),
 ("RENDER RAT 30° – DOPPIO BANCO", "RAT 30°: doppio banco", "render-doppio"),
 ("RENDER RAT 30° – TRIPLO BANCO", "RAT 30°: triplo banco", "render-triplo"),
]
e = html.escape
slides_html = ""
for i, (ph, cap, key) in enumerate(SLIDES, 1):
    slides_html += (f'<li class="pt-s" role="group" aria-roledescription="slide" aria-label="{i} di {len(SLIDES)}" data-step="{key}" data-file="">'
                    f'<figure><div class="pt-media"><div class="pt-ph" role="img" aria-label="Segnaposto: {e(ph)}">[{e(ph)}]</div></div>'
                    f'<figcaption>{e(cap)}</figcaption></figure></li>')
STEP_CSS = """
#pt-rat{--pt-ink:#0C2434;--pt-text:#4A5560;--pt-line:#6E8494;--pt-soft:#C7D5DE;--pt-accent:#1D8AC9;font-family:var(--e-global-typography-text-font-family,Roboto),Roboto,sans-serif;color:var(--pt-text);width:100%}
#pt-rat *{box-sizing:border-box}
#pt-rat ol,#pt-rat ul{list-style:none;margin:0;padding:0}
.pt-stage{position:relative;overflow:hidden;border-radius:16px;background:#F8F9FA;border:1px solid var(--pt-soft)}
.pt-track{display:flex;transition:transform .5s ease}
.pt-s{flex:0 0 100%;min-width:0}
.pt-s figure{margin:0}
.pt-media{aspect-ratio:16/9;background:#fff;display:flex;align-items:center;justify-content:center}
.pt-media img,.pt-media video{display:block;width:100%;height:100%;object-fit:contain}
.pt-ph{width:calc(100% - 48px);height:calc(100% - 48px);border:2px dashed var(--pt-line);border-radius:12px;display:flex;align-items:center;justify-content:center;text-align:center;padding:16px;font-size:18px;font-weight:600;color:var(--pt-ink)}
.pt-s figcaption{padding:14px 20px;font-size:16px;color:var(--pt-ink);border-top:1px solid var(--pt-soft);background:#fff}
.pt-ctl{display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin-top:16px}
.pt-ctl button{font:inherit;font-size:14px;font-weight:600;color:var(--pt-ink);background:#fff;border:2px solid var(--pt-line);border-radius:8px;padding:9px 16px;min-height:44px;cursor:pointer;white-space:normal;text-transform:none;letter-spacing:normal;-webkit-appearance:none;appearance:none}
.pt-ctl button:hover,.pt-ctl button:focus{background:#fff;color:var(--pt-ink);border-color:var(--pt-accent)}
.pt-ctl button:focus-visible{outline:3px solid var(--pt-ink);outline-offset:2px}
.pt-dots{display:flex;gap:8px;margin:0 8px}
.pt-dots button{width:44px;min-height:44px;padding:0;border-radius:8px;font-size:14px}
.pt-dots button[aria-current="true"]{background:var(--pt-ink);color:#fff;border-color:var(--pt-ink)}
.pt-dots button[aria-current="true"]:hover,.pt-dots button[aria-current="true"]:focus{background:var(--pt-ink);color:#fff}
.pt-st{font-size:14px;color:var(--pt-text)}
@media (max-width:767px){.pt-ph{font-size:15px}.pt-ctl{gap:8px}.pt-dots{order:3;width:100%;margin:0}}
@media (prefers-reduced-motion:reduce){.pt-track{transition:none}}
"""
STEP_JS = r"""(function(){var R=document.getElementById('pt-rat');if(!R||R.__pt){return;}R.__pt=1;
var tr=R.querySelector('.pt-track'),sl=[].slice.call(R.querySelectorAll('.pt-s')),dots=R.querySelector('.pt-dots'),st=R.querySelector('.pt-st'),bp=R.querySelector('.pt-pp'),
rm=window.matchMedia('(prefers-reduced-motion: reduce)'),n=sl.length,i=0,timer=null,auto=!rm.matches,live=R.querySelector('.pt-stage');
sl.forEach(function(s,k){var b=document.createElement('button');b.type='button';b.textContent=String(k+1);b.setAttribute('aria-label','Vai al passaggio '+(k+1)+' di '+n);b.addEventListener('click',function(){go(k,true);});dots.appendChild(b);});
function go(k,user){i=(k+n)%n;tr.style.transform='translateX(-'+(i*100)+'%)';
sl.forEach(function(s,j){s.setAttribute('aria-hidden',j===i?'false':'true');[].forEach.call(s.querySelectorAll('a,button,video'),function(x){x.tabIndex=j===i?0:-1;});});
[].forEach.call(dots.children,function(b,j){if(j===i){b.setAttribute('aria-current','true');}else{b.removeAttribute('aria-current');}});
st.textContent='Passaggio '+(i+1)+' di '+n;if(user){stop();}}
function tick(){go(i+1,false);}
function start(){if(timer||!auto){return;}timer=setInterval(tick,4500);setpp();}
function stop(){if(timer){clearInterval(timer);timer=null;}auto=false;setpp();}
function setpp(){bp.textContent=auto?'Metti in pausa':'Avvia scorrimento';bp.setAttribute('aria-pressed',auto?'false':'true');live.setAttribute('aria-live',auto?'off':'polite');}
R.querySelector('.pt-prev').addEventListener('click',function(){go(i-1,true);});
R.querySelector('.pt-next').addEventListener('click',function(){go(i+1,true);});
bp.addEventListener('click',function(){if(auto){stop();}else{auto=true;start();}});
R.addEventListener('mouseenter',function(){if(timer){clearInterval(timer);timer=null;}});R.addEventListener('mouseleave',function(){if(auto){start();}});
R.addEventListener('focusin',function(){if(timer){clearInterval(timer);timer=null;}});R.addEventListener('focusout',function(){if(auto){start();}});
go(0,false);setpp();if(auto){start();}})();"""
stepper = (f'<style>{STEP_CSS.strip()}</style><div id="pt-rat" role="group" aria-roledescription="carousel" aria-label="Dal layout al dettaglio: RAT 30°">'
           f'<div class="pt-stage" aria-live="off"><ol class="pt-track">{slides_html}</ol></div>'
           f'<div class="pt-ctl"><button type="button" class="pt-prev">← Precedente</button><button type="button" class="pt-pp" aria-pressed="false">Metti in pausa</button>'
           f'<button type="button" class="pt-next">Successivo →</button><div class="pt-dots" role="group" aria-label="Passaggi"></div><span class="pt-st" aria-hidden="true"></span></div></div>'
           f'<script>{STEP_JS.strip()}</script>')

sec_rat = section("rat-30", "#FFFFFF", [
    head_box([eyebrow("INTRALOGISTICA"),
              heading("LAYOUT FUNZIONALE PER GESTIONE COLLI ETEROGENEI DA 5000 CPH"),
              text("<p>La proposta che presentiamo si basa sulla presenza di un nostro trasferitore angolare denominato RAT 30° sviluppato per l’intralogistica per il quale abbiamo depositato un apposito brevetto a tutela della funzionalità.</p>", width=92)]),
    W("html", {"html": stepper})])

# ---------------------------------------------------------------- SERIE CD (blocco riusabile)
CD_CSS = ("#pt-cd{--pt-ink:#0C2434;--pt-line:#6E8494;font-family:var(--e-global-typography-text-font-family,Roboto),Roboto,sans-serif;width:100%}"
          "#pt-cd *{box-sizing:border-box}#pt-cd ul{list-style:none;margin:0;padding:0}"
          ".pt-g{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.pt-g li{margin:0}"
          ".pt-g .pt-w{grid-column:1/-1}"
          ".pt-g figure{margin:0}.pt-g .pt-ph2{aspect-ratio:16/9;border:2px dashed var(--pt-line);border-radius:12px;background:#fff;display:flex;align-items:center;justify-content:center;text-align:center;padding:16px;font-size:16px;font-weight:600;color:var(--pt-ink)}"
          ".pt-g .pt-w .pt-ph2{aspect-ratio:21/9}.pt-g figcaption{padding-top:10px;font-size:14px;color:#4A5560}"
          "@media (max-width:767px){.pt-g{grid-template-columns:1fr}}")
cd_items = [("VIDEO 360° SERIE CD – IN PRODUZIONE", "Rotazione 360° dell’assieme, poi zoom sul dettaglio", True),
            ("RENDER SERIE CD – 34alta (PROVVISORIO)", "Assieme, vista 3/4 alta", False),
            ("RENDER SERIE CD – 34hero (PROVVISORIO)", "Assieme, vista hero", False),
            ("RENDER SERIE CD – giunzione3 (PROVVISORIO)", "Dettaglio della giunzione", False)]
cd_html = "".join(f'<li{" class=\"pt-w\"" if w else ""}><figure><div class="pt-ph2" role="img" aria-label="Segnaposto: {e(t)}">[{e(t)}]</div><figcaption>{e(c)}</figcaption></figure></li>' for t, c, w in cd_items)
cd_widget = f'<style>{CD_CSS}</style><div id="pt-cd"><ul class="pt-g">{cd_html}</ul></div>'
sec_cd = section("serie-cd", "#F8F9FA", [
    head_box([eyebrow("CLEAN DESIGN"),
              heading("Serie CD – Clean Design"),
              text("<p>Presentiamo la nuova serie di trasporti identificabili dalla sigla CD che offrono condizioni di alta pulibilità; uniamo efficienza alla qualità estetica e funzionale, pur mantenendo una ottima competitività. I profili delle fiancate sono utilizzati nella realizzazione di nastri trasportatori con piano di scorrimento in tela oppure rete modulare, ed anche in questo caso è stato depositato un apposito brevetto a tutela della tipologia di profilo.</p>", width=92)]),
    W("html", {"html": cd_widget})])

# ---------------------------------------------------------------- CTA
cta = C({"_element_id": "sec-cta-brevetti", "background_background": "classic", "background_color": "#0C2434", "boxed_width": px(1280),
         "flex_align_items": "center", "flex_direction": "column", "flex_direction_mobile": "column", "flex_gap": gap(24),
         "padding": pad(96, 48, 96, 48), "padding_mobile": pad(56, 20, 56, 20)},
        [W("button", {"background_color": "#1D8AC9", "border_radius": {"bottom": "8", "isLinked": True, "left": "8", "right": "8", "top": "8", "unit": "px"},
                      "button_text_color": "#ffffff", "link": {"is_external": False, "nofollow": False, "url": "https://leantech.propagandaadv.com/contattaci/"},
                      "text": "PARLIAMO DEL PROGETTO", "text_padding": pad(17, 34, 17, 34), "text_padding_mobile": pad(16, 22, 16, 22),
                      "typography_font_family": "Roboto", "typography_font_size": px(15), "typography_font_weight": "600", "typography_typography": "custom", "align": "center"})])

SCRIPT_HTML = open("/tmp/claude-0/-home-user-leantech/f9e2ae74-9989-5dcd-bea7-08aaa0fbcc9f/scratchpad/pt/vc_script.html", encoding="utf-8").read()
script_box = C({"padding": {"top": "0", "right": "0", "bottom": "0", "left": "0", "unit": "px", "isLinked": True}, "content_width": "full"}, [W("html", {"html": SCRIPT_HTML})])

page = [hero, sec_rat, sec_cd, cta, script_box]
json.dump(page, open("pt_page.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump([sec_cd], open("pt_block.json", "w", encoding="utf-8"), ensure_ascii=False)
open("stepper.html", "w", encoding="utf-8").write(stepper); open("cd.html", "w", encoding="utf-8").write(cd_widget)
print(len(json.dumps(page, ensure_ascii=False)), "bytes pagina;", len(json.dumps([sec_cd], ensure_ascii=False)), "bytes blocco")
