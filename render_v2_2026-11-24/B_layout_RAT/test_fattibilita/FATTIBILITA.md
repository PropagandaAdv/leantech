# Lavoro B – Layout intralogistico 5000 CPH con RAT 30°: esito della Fase 0

**Esito: BLOCCATO – mancano i file indispensabili.** Non e' stato prodotto nessun render del layout.

## Verifica degli input (24/11/2026)
| Input richiesto | Presente? | Dove ho cercato |
|---|---|---|
| Layout DWG 5000 CPH (sfondo bianco) | **No** | repository, `input/`, cartella Drive condivisa, allegati della sessione, intero filesystem |
| File 3D RAT 30° (3 configurazioni) | **No** | idem |
| WeTransfer del 23/11 (4 invii) | **No** | idem |
| Screenshot `image019.png` / `image020.png` | **No** | idem. Il contenuto del feedback e' riportato nel prompt e applicato al lavoro A |
| File STEP dei nastri | Si' | `input/` (7 STEP + PDF accumulo) |

La cartella Drive condivisa (`10X-h8_9g6yfsX6dOp_-7qporr4obrYcg`) contiene solo gli 8 file dei nastri gia' usati.

## Perche' non procedo con una ricostruzione
- Il layout e' nel DWG: senza di esso non conosco disposizione, lunghezze, raccordi e posizione del RAT. Ricostruirlo "a occhio" produrrebbe un layout inventato, non quello del cliente.
- Il RAT 30° e' un elemento **brevettato**: ruote inclinate, geometria dei banchi e angolo di deviazione vanno presi dal suo modello 3D. Un modello mio sarebbe un'invenzione e non lo presenterei al cliente come il suo prodotto.

## Cosa mi serve (in ordine di priorita')
1. **File 3D del RAT 30°** nelle tre configurazioni (banco singolo con 3 file di ruote, doppio, triplo): STEP, o formato equivalente.
2. **Layout 5000 CPH**: il DWG (anche solo 2D) e lo screenshot con la cornice rossa della zona RAT (email del 17/11).
3. Il contenuto dei **4 WeTransfer del 23/11**, se contiene modelli 3D del layout: in tal caso uso quelli.
4. Facoltativo: dimensioni/modello di riferimento dei colli, altrimenti uso scatole di cartone di misure diverse, senza loghi (`[ASSUNZIONE]`).

## Piano appena i file sono disponibili
1. Se esiste un 3D completo del layout: lo uso. Se e' solo 2D: importo il DWG come riferimento in pianta e ricostruisco i tratti con i modelli STEP gia' disponibili (sezione W=340) o con estrusioni semplificate, inserendo il RAT 3D reale nelle posizioni del DWG. Le parti ricostruite vengono segnalate come tali nel report.
2. Immagine di prova a bassa risoluzione della vista a volo d'angelo, con fonte della geometria, fedelta' e tempi.
3. Inquadrature L1–L5 (e L6 se la geometria lo consente), stesso stile e materiali dei render dei nastri (profilo v2).
4. Animazione L1 → L2 → L5 e tre clip brevi (L3, L4, L5); GLB del RAT nelle tre configurazioni.

## Tempi indicativi (stime, da confermare sulla geometria reale; CPU a 4 core, senza GPU)
| Prodotto | Stima |
|---|---|
| Immagine Full HD | 3–6 min |
| Master 4K | 12–20 min |
| Clip da 3–4 s a 25 fps (75–100 frame, Full HD, 32 sample) | 1,5–2,5 h ciascuna |
| Animazione continua da 12–15 s | 5–8 h |
