"""Classificazione componente -> famiglia materiale. Chiave: (prodotto, colore CAD della faccia)."""
import re

# --- assegnazioni esplicite per prodotto (confidenza alta: riconosciuti da forma/posizione) ---
EXPLICIT = {
    # fiancate estruse (profilo curvo lungo quanto il nastro) -> alluminio 6061
    **{p: ("ALU6061", "alta", "fiancata estrusa") for p in ["PX0000381738","PX0000381688","PX0000380494","PX0000381785","PX0000381784"]},
    # guide laterali estruse (profilo doppio con cave)
    **{p: ("ALU6061", "media", "guida laterale estrusa") for p in ["PX0000345764","PX0000355394","PX0000362940","PX0000364651","PX0000016332","D00000150440"]},
    # reti modulari: anello di rete modellato come lamiera
    "PX0000381743_Default<A macchina>": ("RETE_STD", "alta", "rete trasferimento 750"),
    "PX0000381794_Default<A macchina>": ("RETE_STD", "alta", "rete trasferimento 10000"),
    "PX0000381010_Default<A macchina>": ("RETE_ACC", "alta", "rete accumulo (rullini folli NON modellati nel CAD)"),
    "PX0000381706_Default<A macchina>": ("RETE_FRE", "alta", "rete freno/lancio (pattini gomma NON modellati nel CAD)"),
    # motoriduttori
    "PX0000055997_T=270°": ("MOTORE", "alta", "motoriduttore"),
    "PX0000381700": ("MOTORE", "alta", "motoriduttore"),
    # pignoni / ruote dentate in plastica tecnica
    "A00000016640_Default<A macchina>": ("PL_PIGNONE", "alta", "pignoni rete"),
    "A00000010855": ("PL_PIGNONE", "media", "pignoni rete (rinvio)"),
    # piedini di livellamento: base in gomma
    "A00000006524": ("GOMMA", "alta", "base piedino"), "A00000006523": ("GOMMA", "alta", "base piedino"),
    # cavi fotocellule
    "PX0000104202": ("PL_CAVO", "alta", "cavi sensori"),
    # tappi guida azzurri
    "CLEV00242614_Default<A macchina>": ("PL_BLU", "alta", "testate guide laterali"),
    # piano di scorrimento sotto rete
    **{p: ("PL_NAVY", "media", "piano scorrimento UHMW (colore da CAD)") for p in ["PX0000381739","PX0000381689","PX0000380495","PX0000381786","PX0000133112"]},
    # pattini/strisce di usura di ritorno
    **{p: ("PL_GRIGIO", "media", "strisce usura ritorno") for p in ["PX0000381740","PX0000381690","PX0000380501","PX0000381788","PX0000381787"]},
    "CLEV00011980_Default<A macchina>": ("PL_NERO", "media", "strisce usura/supporti"),
    # sensori FTC
    "PX0000031139": ("PL_SENSORE", "media", "corpo fotocellula"),
    "D00000088150_Default<A macchina>": ("PL_VERDE", "media", "sensore verde"),
    "PX0000034876": ("INOX", "media", "staffa FTC"),
    "A00000022417": ("INOX", "media", "piastra"),
    "A00000017567": ("INOX", "bassa", "boccole senza colore CAD"),
    "A00000022014": ("PL_NERO", "media", "tappi quadri"),
    "A00000003857": ("INOX", "bassa", "tamburo/rullo (colore CAD grigio generico)"),
    "A00000008654": ("PL_NERO", "bassa", "rulli di ritorno"),
    "A00000008216": ("PL_NERO", "media", "rulli/pulegge di ritorno"),
    "A00000006521": ("PL_NERO", "media", "supporti flangiati cuscinetto"),
}
RED_STRIP = {"CLEV00023115_Default<A macchina>"}   # strisce rosse sulle guide
ARROW_ID = (255, 255, 255)                          # freccia direzione sulle reti ACC/FRE (faccia bianca 250x375 mm)

def classify(prod, col, nfaces_hint=0):
    """col = (r,g,b) CAD della faccia. Ritorna (famiglia, confidenza, nota)."""
    if prod in RED_STRIP: return ("PL_ROSSO", "bassa", "strisce rosse su guide")
    if prod in ("PX0000381010_Default<A macchina>", "PX0000381706_Default<A macchina>") and tuple(col) == ARROW_ID:
        return ("FRECCIA", "alta", "freccia di direzione (decal CAD, 1 mm)")
    if prod in EXPLICIT:
        f, c, n = EXPLICIT[prod]; return (f, c, n)
    r, g, b = col
    if (r, g, b) == (-1, -1, -1): return ("INOX", "bassa", "nessun colore CAD")
    if (r, g, b) == (0, 179, 237): return ("PL_BLU", "media", "azzurro CAD")
    if (r, g, b) in [(144,136,128),(134,134,134),(96,87,78)]: return ("INOX", "media", "lamiera/barra metallica (colore CAD acciaio)")
    if max(r, g, b) <= 100 and not (b > r + 80): return ("PL_NERO", "media", "colore CAD scuro -> plastica nera")
    if (r, g, b) in [(192,192,192),(152,164,220)]: return ("ALU6061", "media", "estruso (colore CAD alluminio)")
    if (r, g, b) in [(255,255,0),(255,255,55),(255,55,255),(255,55,55),(255,255,255),(55,55,255),(0,134,134),(134,255,255),(154,159,154),(0,146,8),(151,163,218),(86,95,105)] :
        return ("INOX_VITE", "media", "viteria/minuteria (colore CAD di servizio)")
    return ("INOX", "bassa", "default")
