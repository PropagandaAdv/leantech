# Consegna 20/11 – file da caricare / sorgenti

Questi file non si possono caricare nella Media Library tramite il connettore (limite: upload da file locale non disponibile). Vanno caricati a mano da WordPress → Media → Aggiungi.

## 1. Hero Settori (`settori_hero/`)
- `lea-settori-hero-1920.mp4` – 1920×1080, 34 s, 7,4 MB, H.264 `+faststart`, senza audio (da LEA_SLOW_DEF_003.mp4, 3840×2160, 89 MB)
- `lea-settori-hero-mobile-960.mp4` – 960 px, 3,0 MB
- `lea-settori-hero-poster.webp` – poster 1920 px, 176 KB
Dopo il caricamento: in /settori/ il contenitore hero (`sec-hero`) ha già lo stile video; va sostituito solo il link del video di sfondo (Elementor → hero → Sfondo → Video) e il poster (fallback).

## 2. Render serie CD provvisori (`render_serie_CD_webp/`)
WebP ≤ 500 KB (1920 px, dai FHD). I 4K non erano disponibili. Da usare nei segnaposto della sezione "Serie CD" di /patrimonio-tecnico/ e nella card del Digital Showroom.

## 3. Logo Clevertech (`header_clevertech/`)
PNG originale scaricato da https://www.clevertech-group.com/assets/img/clevertech/logo.png (già caricato in Media Library, ID 420, alt "Clevertech").

## Sorgenti
- `engineering_flusso_lineare/` – generatore (`build_linear.py`), HTML finale e JSON della sezione inserita in /engeneering/.
- `patrimonio_tecnico/` – generatore (`build_pt.py`) e JSON della pagina e del blocco brevetto.
