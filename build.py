#!/usr/bin/env python3
"""Genera index.html da template.html + lezioni.json.
Uso: python3 build.py   (poi carica index.html su GitHub/Vercel)"""
import json, html, datetime, pathlib

ROOT = pathlib.Path(__file__).parent
data = json.loads((ROOT / "lezioni.json").read_text(encoding="utf-8"))
sito, lezioni, faq = data["sito"], data["lezioni"], data["faq"]
e = lambda s: html.escape(s, quote=True)
url = sito["url"].rstrip("/")
thumb = lambda i: f"https://i.ytimg.com/vi/{i}/hqdefault.jpg"

# <head>: title, description, canonical, Open Graph
head = [
    f'<title>{e(sito["titolo_pagina"])}</title>',
    f'<meta name="description" content="{e(sito["meta_description"])}">',
    '<meta name="robots" content="index, follow, max-image-preview:large, max-video-preview:-1">',
    '<meta name="theme-color" content="#6761e5">',
    '<meta property="og:type" content="website">',
    '<meta property="og:locale" content="it_IT">',
    '<meta property="og:site_name" content="AlfaDocs Academy">',
    f'<meta property="og:title" content="{e(sito["titolo_pagina"])}">',
    f'<meta property="og:description" content="{e(sito["meta_description"])}">',
    f'<meta property="og:image" content="{thumb(lezioni[0]["id"])}">',
    '<meta name="twitter:card" content="summary_large_image">',
]
if url:
    head += [f'<link rel="canonical" href="{e(url)}/">', f'<meta property="og:url" content="{e(url)}/">']

# Schede lezione: testo statico nell'HTML, video caricato al click
cards = []
for n, l in enumerate(lezioni, 1):
    meta = f"Lezione {n} di {len(lezioni)}" + (f" · {e(l['durata'])}" if l.get("durata") else "")
    cards.append(f'''        <li class="card" id="lezione-{n}" data-id="{e(l["id"])}">
          <div class="video">
            <a class="facade" href="https://www.youtube.com/watch?v={e(l["id"])}" aria-label="Riproduci: {e(l["titolo"])}">
              <img src="{thumb(l["id"])}" alt="{e(l["titolo"])}" width="480" height="360" loading="{"eager" if n <= 2 else "lazy"}">
              <span class="play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>
            </a>
            <span class="badge">Lezione {n}</span>
          </div>
          <div class="card__body">
            <span class="card__tag">{meta}</span>
            <h3>{e(l["titolo"])}</h3>
            <p>{e(l["descrizione"])}</p>
            <label class="check"><input type="checkbox"> Lezione completata</label>
          </div>
        </li>''')

faq_html = "\n".join(
    f'''        <details{" open" if i == 0 else ""}>
          <summary>{e(f["domanda"])}</summary>
          <p>{e(f["risposta"])}</p>
        </details>''' for i, f in enumerate(faq))

# Dati strutturati (schema.org) per Google e motori AI
page_url = (url + "/") if url else None
org = {"@type": "Organization", "@id": "https://www.alfadocs.com/#organization", "name": "AlfaDocs",
       "url": "https://www.alfadocs.com/",
       "logo": "https://www.alfadocs.com/hubfs/Alfadocs%20Rebrand/Alfadocs_Logo_Main.svg",
       "sameAs": ["https://www.facebook.com/alfadocs", "https://www.linkedin.com/company/alfadocs"]}
videos = []
for n, l in enumerate(lezioni, 1):
    v = {"@type": "VideoObject", "name": l["titolo"], "description": l["descrizione"],
         "thumbnailUrl": thumb(l["id"]), "embedUrl": f"https://www.youtube-nocookie.com/embed/{l['id']}",
         "contentUrl": f"https://www.youtube.com/watch?v={l['id']}", "inLanguage": "it",
         "publisher": {"@id": org["@id"]}}
    if l.get("data_pubblicazione"): v["uploadDate"] = l["data_pubblicazione"]
    if page_url: v["url"] = f"{page_url}#lezione-{n}"
    videos.append({"@type": "ListItem", "position": n, "item": v})
course = {"@type": "Course", "name": "Marketing per dentisti",
          "description": sito["intro"], "inLanguage": "it", "isAccessibleForFree": True,
          "provider": {"@id": org["@id"]},
          "audience": {"@type": "Audience", "audienceType": "Dentisti e titolari di studi dentistici"},
          "teaches": [l["titolo"] for l in lezioni],
          "offers": {"@type": "Offer", "price": 0, "priceCurrency": "EUR", "category": "Free"},
          "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Online", "inLanguage": "it"}}
if page_url: course["url"] = page_url
graph = [org, course,
         {"@type": "ItemList", "name": "Lezioni del corso", "numberOfItems": len(lezioni), "itemListElement": videos},
         {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f["domanda"],
            "acceptedAnswer": {"@type": "Answer", "text": f["risposta"]}} for f in faq]}]
jsonld = ('<script type="application/ld+json">\n'
          + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1).replace("</", "<\\/")
          + "\n</script>")

lead = data["lead"]
lead_cfg = {k: v for k, v in lead.items() if not k.startswith("_")}
lead_json = ('<script type="application/json" id="lead-config">'
             + json.dumps(lead_cfg, ensure_ascii=False).replace("</", "<\\/") + "</script>")
gtm = ""
if lead.get("gtm_id"):
    g = e(lead["gtm_id"])
    gtm = ("<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
           "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
           f"j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{g}');</script>")

out = (ROOT / "template.html").read_text(encoding="utf-8")
for k, v in {"HEAD": "\n".join(head), "JSONLD": jsonld, "LESSONS": "\n".join(cards), "FAQ": faq_html,
             "N": str(len(lezioni)), "INTRO": e(sito["intro"]), "FIRST_ID": e(lezioni[0]["id"]),
             "FIRST_TITLE": e(lezioni[0]["titolo"]), "LEAD_CONFIG": lead_json, "GTM_HEAD": gtm, "PRIVACY_URL": e(lead["privacy_url"]), "YEAR": str(datetime.date.today().year)}.items():
    out = out.replace("{{" + k + "}}", v)
assert "{{" not in out, "segnaposto non sostituito"
(ROOT / "index.html").write_text(out, encoding="utf-8")
if not ((lead["hubspot_portal_id"] and lead["hubspot_form_guid"]) or lead["webhook_url"]):
    print("ATTENZIONE: nessuna destinazione lead in lezioni.json -> i lead NON vengono salvati")
print(f"index.html generato: {len(lezioni)} lezioni, {len(faq)} FAQ" + ("" if url else " (manca sito.url: canonical non impostato)"))
