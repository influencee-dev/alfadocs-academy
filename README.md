# AlfaDocs Academy – Marketing per studi medici e dentistici

Landing con le 13 video lezioni del corso, nello stile di alfadocs.com, ottimizzata per SEO e motori AI.

## File
- `index.html` – la pagina da pubblicare (generata, non modificarla a mano)
- `lezioni.json` – **tutti i contenuti**: titoli, descrizioni, video, FAQ, title e meta description
- `template.html` – grafica e struttura
- `build.py` – rigenera `index.html`

## Modificare contenuti o video
1. Modifica `lezioni.json`
   - `id`: la parte finale del link YouTube (`https://youtu.be/ID`); i video devono essere pubblici o non in elenco
   - `data_pubblicazione` (es. `2025-03-14`) e `durata` (es. `12 min`): facoltativi, aiutano la SEO dei video
   - `sito.url`: l'indirizzo definitivo della pagina (attiva il canonical)
2. Esegui `python3 build.py`
3. Carica su GitHub: Vercel ripubblica da solo

## Vedere la pagina
I video YouTube non partono se apri il file con doppio clic (`file://`).
Usa Vercel/GitHub Pages oppure in locale: `python3 -m http.server` → http://localhost:8000
