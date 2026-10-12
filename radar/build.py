#!/usr/bin/env python3
"""AlfaDocs Radar – genera index.html e feed.xml da articoli.json.
Uso: python3 build.py"""
import json, html, pathlib, datetime
from email.utils import format_datetime

ROOT = pathlib.Path(__file__).parent
D = json.loads((ROOT / "articoli.json").read_text(encoding="utf-8"))
A, LEAD = D["articoli"], D["lead"]
e = lambda s: html.escape(str(s), quote=True)
MESI = "gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre".split()
def it_date(s):
    d = datetime.date.fromisoformat(s); return f"{d.day} {MESI[d.month-1]} {d.year}"
CATS = ["Normativa", "Mercato", "Scientifica", "Tecnologia e privacy", "Professione", "Eventi"]
SITE = "https://alfadocs-radar.vercel.app"
LOGO = "https://www.alfadocs.com/hubfs/Alfadocs%20Rebrand/Alfadocs_Logo_Main.svg"

# Articoli più recenti in alto (per data della fonte)
A = sorted(A, key=lambda a: a["data_fonte"], reverse=True)
posts = []
for i, a in enumerate(A):
    cls = a["categoria"].split()[0]
    posts.append(f'''      <li class="post" id="{e(a["slug"])}" data-cat="{e(a["categoria"])}">
        <div class="post__meta"><span class="cat cat--{cls}">{e(a["categoria"])}</span><time datetime="{a["data_fonte"]}">{it_date(a["data_fonte"])}</time><span>· {e(a["fonte"])}</span></div>
        <h2>{e(a["titolo"])}</h2>
        <p>{e(a["sintesi"])}</p>
        <div class="impact"><b>Cosa significa per il tuo studio</b><p class="impact__text">{e(a["impatto"])}</p>
          <div class="unlock"><button class="btn btn--primary" type="button" data-open-lead>Sblocca gratis</button></div></div>
        <a class="source" href="{e(a["url"])}" target="_blank" rel="noopener">Leggi la fonte ufficiale</a>
      </li>''')
counts = {c: sum(a["categoria"] == c for a in A) for c in CATS}
chips = '<button class="chip" type="button" data-filter="" aria-pressed="true">Tutte<span>' + str(len(A)) + '</span></button>' + "".join(
    f'<button class="chip" type="button" data-filter="{e(c)}" aria-pressed="false">{e(c)}<span>{n}</span></button>' for c, n in counts.items() if n)

jsonld = {"@context": "https://schema.org", "@graph": [
    {"@type": "Organization", "@id": "https://www.alfadocs.com/#organization", "name": "AlfaDocs", "url": "https://www.alfadocs.com/", "logo": LOGO},
    {"@type": "Blog", "name": "AlfaDocs Radar", "url": SITE + "/", "inLanguage": "it", "publisher": {"@id": "https://www.alfadocs.com/#organization"},
     "blogPost": [{"@type": "BlogPosting", "headline": a["titolo"], "description": a["sintesi"], "datePublished": D["aggiornato"],
                   "url": f"{SITE}/#{a['slug']}", "articleSection": a["categoria"], "isBasedOn": a["url"], "inLanguage": "it",
                   "publisher": {"@id": "https://www.alfadocs.com/#organization"}} for a in A]}]}
lead_cfg = {k: v for k, v in LEAD.items() if not k.startswith("_")}

css = (ROOT / "base.css").read_text(encoding="utf-8") + (ROOT / "radar.css").read_text(encoding="utf-8")
desc = "Le notizie del mondo odontoiatrico riassunte ogni mattina per i dentisti: normativa, mercato, studi scientifici, tecnologia ed eventi, con link alle fonti ufficiali."
page = f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AlfaDocs Radar – Le notizie per i dentisti, ogni mattina</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}/">
<link rel="alternate" type="application/rss+xml" title="AlfaDocs Radar" href="{SITE}/feed.xml">
<meta property="og:type" content="website"><meta property="og:locale" content="it_IT"><meta property="og:site_name" content="AlfaDocs Radar">
<meta property="og:title" content="AlfaDocs Radar – Le notizie per i dentisti, ogni mattina"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{SITE}/">
<meta name="theme-color" content="#6761e5">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{css}</style>
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False).replace("</", "<\\/")}</script>
</head>
<body>
<header class="header">
  <div class="container header__inner">
    <a class="header__brand" href="https://www.alfadocs.com/" aria-label="AlfaDocs"><img src="{LOGO}" alt="AlfaDocs" width="140" height="32"><span>Radar</span></a>
    <button class="btn btn--primary" type="button" data-open-lead>Iscriviti gratis</button>
  </div>
</header>
<main>
  <section class="hero hero--radar">
    <div class="container hero__grid">
      <div>
        <span class="eyebrow">AlfaDocs Radar · Notizie per dentisti</span>
        <h1>Le notizie che contano per il tuo <em class="serif">studio dentistico</em>, ogni mattina</h1>
        <p class="lead">Normativa, mercato, studi scientifici, tecnologia ed eventi: selezioniamo le notizie del settore odontoiatrico, le riassumiamo in poche righe e ti spieghiamo cosa cambiano per il tuo studio. Sempre con il link alla fonte ufficiale.</p>
        <p class="today">Aggiornato il {it_date(D["aggiornato"])} · {len(A)} notizie</p>
      </div>
      <aside class="hero__side">
        <span class="eyebrow">Gratis</span>
        <h2>Ricevi il Radar ogni mattina</h2>
        <p>Le notizie del giorno nella tua email alle 6:30, in 3 minuti di lettura.</p>
        <ul><li>Solo notizie verificate, con fonte</li><li>Cosa significano per il tuo studio</li><li>Accesso a tutti gli approfondimenti</li></ul>
        <button class="btn btn--primary" type="button" data-open-lead>Iscriviti gratis</button>
      </aside>
    </div>
  </section>
  <section class="feed" aria-label="Notizie">
    <div class="container">
      <div class="filters" role="toolbar" aria-label="Filtra per categoria">{chips}</div>
      <ol class="news" id="news">
{chr(10).join(posts)}
      </ol>
      <p class="note">Le notizie sono riassunte da fonti pubbliche e non sostituiscono i testi originali: fa sempre fede la fonte ufficiale indicata. I contenuti scientifici hanno scopo informativo e non costituiscono indicazioni cliniche.</p>
    </div>
  </section>
  <section class="cta">
    <div class="container"><div class="cta__box">
      <span class="eyebrow">Passa all'azione</span>
      <h2>Gestisci lo studio con <em class="serif">AlfaDocs</em></h2>
      <p>Il software gestionale in cloud per studi dentistici: agenda, cartella clinica, fatturazione e marketing in un'unica piattaforma.</p>
      <a class="btn btn--primary" href="https://www.alfadocs.com/">Scopri AlfaDocs</a>
    </div></div>
  </section>
</main>
<footer class="footer"><div class="container"><img src="{LOGO}" alt="AlfaDocs" width="110" height="25"><span>© {datetime.date.today().year} AlfaDocs · Radar · <a href="feed.xml">Feed RSS</a></span></div></footer>

<dialog class="lead" id="lead" aria-labelledby="lead-title">
  <div class="lead__head">
    <button class="lead__close" type="button" id="lead-close" aria-label="Chiudi">×</button>
    <span class="eyebrow">Gratis per i dentisti</span>
    <h2 id="lead-title">Ricevi AlfaDocs Radar ogni mattina</h2>
    <p>Sblocca tutti gli approfondimenti e ricevi le notizie del giorno via email.</p>
  </div>
  <form id="lead-form" novalidate>
    <div class="field"><label for="f-nome">Nome *</label><input id="f-nome" name="firstname" autocomplete="given-name" required></div>
    <div class="field"><label for="f-cognome">Cognome *</label><input id="f-cognome" name="lastname" autocomplete="family-name" required></div>
    <div class="field"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
    <div class="field"><label for="f-tel">Telefono</label><input id="f-tel" name="phone" type="tel" autocomplete="tel" pattern="[0-9+ ()\\-]{{6,}}"></div>
    <div class="field"><label for="f-studio">Nome dello studio *</label><input id="f-studio" name="company" autocomplete="organization" required></div>
    <div class="field"><label for="f-ruolo">Ruolo *</label>
      <select id="f-ruolo" name="jobtitle" required><option value="">Seleziona</option><option>Dentista titolare</option><option>Dentista collaboratore</option><option>Direttore sanitario</option><option>Segreteria / ASO</option><option>Altro</option></select></div>
    <label class="consent"><input type="checkbox" name="privacy" required> <span>Ho letto l'<a href="{e(LEAD["privacy_url"])}" target="_blank" rel="noopener">informativa privacy</a> e acconsento al trattamento dei dati per ricevere AlfaDocs Radar. *</span></label>
    <label class="consent"><input type="checkbox" name="marketing"> <span>Acconsento a ricevere comunicazioni commerciali da AlfaDocs (facoltativo).</span></label>
    <p class="lead__error" id="lead-error" hidden></p>
    <button class="btn btn--primary" type="submit" id="lead-submit">Iscriviti e sblocca</button>
  </form>
</dialog>
<script type="application/json" id="lead-config">{json.dumps(lead_cfg, ensure_ascii=False)}</script>
<script>
(function () {{
  const $ = (s) => document.querySelector(s), $$ = (s) => [...document.querySelectorAll(s)];
  const CFG = JSON.parse($("#lead-config").textContent);
  const KEY = "alfadocs-radar-lead";
  const hasLead = () => {{ try {{ return !!localStorage.getItem(KEY); }} catch (e) {{ return false; }} }};
  const posts = $$(".post");

  // Approfondimenti: i primi N liberi, gli altri sbloccati dopo l'iscrizione
  function applyLock() {{ posts.forEach((p, i) => p.classList.toggle("locked", !hasLead() && i >= CFG.articoli_liberi)); }}

  // Filtri per categoria (anche da URL: #cat=Normativa)
  function filter(cat) {{
    $$(".chip").forEach((c) => c.setAttribute("aria-pressed", c.dataset.filter === cat));
    posts.forEach((p) => (p.hidden = !!cat && p.dataset.cat !== cat));
  }}
  $$(".chip").forEach((c) => c.addEventListener("click", () => {{
    filter(c.dataset.filter);
    history.replaceState(null, "", c.dataset.filter ? "#cat=" + encodeURIComponent(c.dataset.filter) : location.pathname);
  }}));
  const m = location.hash.match(/^#cat=(.+)$/); if (m) filter(decodeURIComponent(m[1]));

  // Form lead
  const dlg = $("#lead"), form = $("#lead-form"), err = $("#lead-error");
  let origin = "";
  $$("[data-open-lead]").forEach((b) => b.addEventListener("click", () => {{
    const post = b.closest(".post"); origin = post ? post.querySelector("h2").textContent : "header";
    err.hidden = true; dlg.showModal ? dlg.showModal() : dlg.setAttribute("open", "");
    setTimeout(() => $("#f-nome").focus(), 50);
  }}));
  const closeDlg = () => (dlg.close ? dlg.close() : dlg.removeAttribute("open"));
  $("#lead-close").addEventListener("click", closeDlg);
  dlg.addEventListener("click", (e) => {{ if (e.target === dlg) closeDlg(); }});

  function utm() {{
    const p = new URLSearchParams(location.search), o = {{}};
    ["utm_source","utm_medium","utm_campaign","utm_content","utm_term","gclid","fbclid"].forEach((k) => p.get(k) && (o[k] = p.get(k)));
    return o;
  }}
  async function sendLead(data) {{
    const jobs = [];
    if (CFG.hubspot_portal_id && CFG.hubspot_form_guid) {{
      const fields = ["firstname","lastname","email","phone","company","jobtitle"].filter((n) => data[n]).map((name) => ({{ name, value: data[name] }}));
      const hutk = (document.cookie.match(/hubspotutk=([^;]+)/) || [])[1];
      jobs.push(fetch(`https://api.hsforms.com/submissions/v3/integration/submit/${{CFG.hubspot_portal_id}}/${{CFG.hubspot_form_guid}}`, {{
        method: "POST", headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify({{ fields, context: {{ pageUri: location.href, pageName: document.title, ...(hutk ? {{ hutk }} : {{}}) }},
          legalConsentOptions: {{ consent: {{ consentToProcess: true, text: "Consenso al trattamento dei dati per ricevere AlfaDocs Radar",
            communications: CFG.hubspot_subscription_type_id ? [{{ value: data.marketing === "si", subscriptionTypeId: Number(CFG.hubspot_subscription_type_id), text: "Comunicazioni commerciali AlfaDocs" }}] : [] }} }} }})
      }}).then((r) => {{ if (!r.ok) throw new Error("HubSpot " + r.status); }}));
    }}
    if (CFG.webhook_url) jobs.push(fetch(CFG.webhook_url, {{ method: "POST", mode: "no-cors", body: new URLSearchParams(data) }}));
    if (!jobs.length) console.warn("[AlfaDocs Radar] Nessuna destinazione lead configurata", data);
    await Promise.all(jobs);
  }}
  form.addEventListener("submit", async (e) => {{
    e.preventDefault();
    if (!form.checkValidity()) {{ err.textContent = "Compila tutti i campi obbligatori (*) con dati validi."; err.hidden = false; form.reportValidity(); return; }}
    const fd = Object.fromEntries(new FormData(form));
    const data = {{ ...fd, privacy: "si", marketing: fd.marketing ? "si" : "no", origine: origin, pagina: location.href, data: new Date().toISOString(), ...utm() }};
    const btn = $("#lead-submit"); btn.disabled = true; btn.textContent = "Invio in corso…";
    try {{
      await sendLead(data);
      try {{ localStorage.setItem(KEY, "1"); }} catch (e2) {{}}
      (window.dataLayer = window.dataLayer || []).push({{ event: "generate_lead", form: "radar_dentisti", origine: origin }});
      form.reset(); closeDlg(); applyLock();
    }} catch (e2) {{ err.textContent = "Invio non riuscito. Controlla la connessione e riprova."; err.hidden = false; }}
    finally {{ btn.disabled = false; btn.textContent = "Iscriviti e sblocca"; }}
  }});
  applyLock();
}})();
</script>
</body>
</html>
'''
(ROOT / "index.html").write_text(page, encoding="utf-8")

# Feed RSS in uscita
now = datetime.datetime.combine(datetime.date.fromisoformat(D["aggiornato"]), datetime.time(6, 30), datetime.timezone(datetime.timedelta(hours=2)))
items = "".join(f'''
  <item><title>{e(a["titolo"])}</title><link>{SITE}/#{a["slug"]}</link><guid isPermaLink="false">{e(a["slug"])}</guid>
    <category>{e(a["categoria"])}</category><pubDate>{format_datetime(now)}</pubDate>
    <description>{e(a["sintesi"] + " Fonte: " + a["fonte"] + " – " + a["url"])}</description></item>''' for a in A)
(ROOT / "feed.xml").write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>AlfaDocs Radar</title><link>{SITE}/</link><language>it</language>
  <description>{e(desc)}</description><lastBuildDate>{format_datetime(now)}</lastBuildDate>{items}
</channel></rss>
''', encoding="utf-8")
if not ((LEAD["hubspot_portal_id"] and LEAD["hubspot_form_guid"]) or LEAD["webhook_url"]):
    print("ATTENZIONE: nessuna destinazione lead -> i lead NON vengono salvati")
print(f"index.html + feed.xml generati: {len(A)} articoli")
