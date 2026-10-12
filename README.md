# AlfaDocs Academy – Landing corso

Landing page con i 13 video del corso, nello stile di alfadocs.com.

## Modificare i video
Apri `index.html` e cerca `const LESSONS` (in fondo al file).
Ogni riga è una lezione:

```js
{ id: "YN0ccSHU9pQ", title: "Marketing vs Comunicazione", duration: "", description: "..." },
```

- `id`: la parte finale del link YouTube (`https://youtu.be/ID`)
- I video devono essere **pubblici** o **non in elenco** (non privati)

## Vedere la pagina
YouTube blocca i video se la pagina viene aperta con doppio clic dal computer (`file://`).
Per vederla funzionante:
- **GitHub Pages:** Settings → Pages → Branch `main` / root → Save
- **Vercel:** New Project → importa il repo → Deploy (nessuna configurazione)
- **In locale:** dalla cartella esegui `python3 -m http.server` e apri http://localhost:8000
