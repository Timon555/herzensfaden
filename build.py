#!/usr/bin/env python3
"""Static site builder for herzensfaden.com.
Wraps each content/<slug>.html partial in the shared head/header/footer
and writes a plain, deployable <slug>.html to the project root.
Run:  python3 build.py
"""
import os, json, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))

# Basis-URL der veröffentlichten Seite – ohne Schrägstrich am Ende.
# Läuft die Seite unter einer eigenen Domain, hier eintragen,
# z. B. "https://www.herzensfaden.com".
BASE_URL = "https://timon555.github.io/herzensfaden"

# Vorschaubild fürs Teilen (Open Graph / Twitter) – absolute URL.
OG_IMAGE = BASE_URL + "/assets/img/home-hero.jpg"

# (slug, <title>, meta description, nav key)
PAGES = [
    ("index",            "Herzensfaden – Brigitte Meissner | Hebamme & Craniosacral-Therapie Winterthur",
     "Brigitte Meissner – Hebamme, Craniosacral-Therapeutin und Autorin in Winterthur. Geburten verarbeiten, Mutter-Kind-Bindung fördern, Belastungen reduzieren.", "start"),
    ("ueber-mich",       "Über Brigitte Meissner – Hebamme & Referentin | Herzensfaden",
     "Brigitte Renate Meissner: Hebamme, Pflegefachfrau, Craniosacral-Therapeutin, Autorin und Mitgründerin des Netzwerks Verarbeitung Geburt.", "ueber"),
    ("praxis",           "Praxis in Winterthur – Craniosacral, Hebamme, Geburtsverarbeitung | Herzensfaden",
     "Meine Praxis in Winterthur: Craniosacral-Therapie, Fussreflexzonen, Bachblüten, Geburtsverarbeitung und Bindungsheilung – krankenkassenanerkannt.", "praxis"),
    ("kurse-fachpersonen","Fortbildungen für Fachpersonen – Mütter & Babys | Herzensfaden",
     "Fortbildungsreihe in drei Modulen (14 Tage) für Hebammen und Fachpersonen rund um Mutter und Kind. E-log anerkannt. Termine 2026 in Winterthur und als Zoom-Webinar.", "fortbildungen"),
    ("kurse-eltern",     "Kurse für Mütter & Eltern – Bindung heilen | Herzensfaden",
     "Bindung und Belastung heilen mit Babys nach schweren Geburten. Lernen Sie die drei Schritte von Brigitte Meissner kennen: Herzensfaden, Babyheilbad und Heilgespräch.", "eltern"),
    ("babyheilbad",      "Babyheilbad – das Bindungsbad nach Brigitte Meissner | Herzensfaden",
     "Das Babyheilbad ist ein heilsames Bindungsbad, das Belastungen von Babys nach schwierigen Geburten oder frühen Trennungen auffangen kann. Merkblatt zum Download.", "eltern"),
    ("buecher",          "Bücher von Brigitte Meissner bestellen | Herzensfaden",
     "Vier Bücher von Brigitte Meissner rund um Geburtsverarbeitung, Kaiserschnitt und Mutter-Kind-Bindung. Bestellung für die Schweiz und Deutschland/Österreich.", "buecher"),
    ("poster-postkarten","Rosa Herzensfaden – Poster & Postkarten | Herzensfaden",
     "Die rosa Herzensfaden Postkarten und Poster von Brigitte Meissner – einfühlsame Motive für Schwangerschaft, Geburt, Trennungen und Sternenkinder.", "karten"),
    ("kontakt",          "Kontakt & Anmeldung | Herzensfaden – Brigitte Meissner",
     "Kontakt und Anmeldung bei Brigitte Meissner in Winterthur. Anmeldung bitte telefonisch unter +41 52 203 37 37. Wegbeschreibung zur Praxis und hilfreiche Adressen.", "kontakt"),
    ("impressum",        "Impressum & Datenschutz | Herzensfaden",
     "Impressum, Datenschutz und rechtliche Hinweise von Herzensfaden – Brigitte Meissner, Winterthur.", "none"),
]

# Top navigation (label, file)
NAV = [
    ("Über mich",     "ueber-mich.html",          "ueber"),
    ("Praxis",        "praxis.html",              "praxis"),
    ("Fortbildungen", "kurse-fachpersonen.html",  "fortbildungen"),
    ("Eltern & Babys","kurse-eltern.html",        "eltern"),
    ("Bücher",        "buecher.html",             "buecher"),
    ("Postkarten",    "poster-postkarten.html",   "karten"),
]

BRAND_MARK = (
    '<svg viewBox="0 0 40 46" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    '<path d="M20 27c0 6-7 7-6 12 1 4 9 3 7-3" stroke="#c5356f" stroke-width="2.2" '
    'stroke-linecap="round" fill="none"/>'
    '<g transform="translate(7.5 2.5) scale(.78)">'
    '<path d="M23.6 0c-3.4 0-6.3 2.7-7.6 5.6C14.7 2.7 11.8 0 8.4 0 3.8 0 0 3.8 0 8.4 '
    '0 17.8 9.5 20.3 16 30.1 22.1 20.3 32 17.5 32 8.4 32 3.8 28.2 0 23.6 0z" fill="#eb458d"/>'
    '</g></svg>'
)

def brand(link=True, cls="brand"):
    inner = (f'<span class="mark">{BRAND_MARK}</span>'
             '<span class="word"><b>Herzensfaden</b><small>Brigitte Meissner</small></span>')
    if link:
        return f'<a class="{cls}" href="index.html" aria-label="Herzensfaden – Startseite">{inner}</a>'
    return f'<div class="{cls}">{inner}</div>'

def nav_links(active):
    items = []
    for label, href, key in NAV:
        cur = ' aria-current="page"' if key == active else ''
        items.append(f'<a href="{href}"{cur}>{label}</a>')
    return '\n        '.join(items)

def header(active):
    return f'''<a class="skip" href="#main">Zum Inhalt springen</a>
<header class="site-header">
  <div class="wrap nav">
    {brand()}
    <button class="nav-toggle" aria-label="Menü öffnen" aria-expanded="false" aria-controls="menu"><span></span></button>
    <div class="nav-menu" id="menu">
      <nav class="nav-links" aria-label="Hauptnavigation">
        {nav_links(active)}
      </nav>
      <a class="btn nav-cta" href="kontakt.html">Termin &amp; Anmeldung</a>
    </div>
  </div>
</header>'''

FOOTER = f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        {brand(cls="brand")}
        <p>Hebamme, Craniosacral-Therapeutin und Autorin in Winterthur. Geburten verarbeiten helfen – Bindung fördern – Belastungen reduzieren.</p>
      </div>
      <div class="footer-col">
        <h4>Angebote</h4>
        <ul>
          <li><a href="praxis.html">Praxis &amp; Therapie</a></li>
          <li><a href="kurse-fachpersonen.html">Fortbildungen</a></li>
          <li><a href="kurse-eltern.html">Kurse für Eltern</a></li>
          <li><a href="babyheilbad.html">Babyheilbad</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Shop &amp; Wissen</h4>
        <ul>
          <li><a href="buecher.html">Bücher</a></li>
          <li><a href="poster-postkarten.html">Poster &amp; Postkarten</a></li>
          <li><a href="ueber-mich.html">Über Brigitte</a></li>
          <li><a href="kontakt.html#adressen">Hilfreiche Adressen</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Kontakt</h4>
        <ul>
          <li><a href="tel:+41522033737">+41 52 203 37 37</a></li>
          <li>Im Geissacker 6<br>8404 Winterthur</li>
          <li><a href="kontakt.html">Termin &amp; Anmeldung</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Brigitte Meissner, Winterthur. Fotos und Texte dürfen ohne schriftliche Genehmigung nicht verwendet werden.</span>
      <span class="legal">
        <a href="impressum.html">Impressum</a>
        <a href="impressum.html#datenschutz">Datenschutz</a>
        <a href="impressum.html#agb">AGB</a>
        <a href="impressum.html#widerruf">Widerruf</a>
      </span>
    </div>
  </div>
</footer>'''

# Datenschutzfreundliche, cookielose Besucherstatistik (GoatCounter).
# 1. Kostenlos auf https://www.goatcounter.com registrieren und einen Code wählen.
# 2. Diesen Code hier eintragen (z. B. "herzensfaden" -> herzensfaden.goatcounter.com).
# Leerer String ("") schaltet die Statistik komplett ab.
GOATCOUNTER_CODE = "herzensfaden"

ANALYTICS = (
    f'<script data-goatcounter="https://{GOATCOUNTER_CODE}.goatcounter.com/count" '
    'async src="//gc.zgo.at/count.js"></script>'
) if GOATCOUNTER_CODE else ""

# Structured Data (JSON-LD): hilft Google, die Praxis als lokales Unternehmen
# mit Adresse, Telefon und Inhaberin zu verstehen (Rich Results / Local SEO).
STRUCTURED_DATA = {
    "@context": "https://schema.org",
    "@type": "MedicalBusiness",
    "name": "Herzensfaden – Brigitte Meissner",
    "description": "Hebamme, Craniosacral-Therapeutin und Autorin in Winterthur. "
                   "Geburten verarbeiten, Mutter-Kind-Bindung fördern, Belastungen reduzieren.",
    "url": BASE_URL + "/",
    "telephone": "+41522033737",
    "image": OG_IMAGE,
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Im Geissacker 6",
        "postalCode": "8404",
        "addressLocality": "Winterthur",
        "addressRegion": "ZH",
        "addressCountry": "CH",
    },
    "founder": {
        "@type": "Person",
        "name": "Brigitte Renate Meissner",
        "jobTitle": "Hebamme, Craniosacral-Therapeutin, Autorin",
    },
    "areaServed": ["CH", "DE", "AT"],
    "knowsLanguage": ["de"],
}
JSONLD = ('<script type="application/ld+json">'
          + json.dumps(STRUCTURED_DATA, ensure_ascii=False)
          + '</script>')

TEMPLATE = '''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Brigitte Meissner">
<link rel="canonical" href="{canonical}">{robots}
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_CH">
<meta property="og:site_name" content="Herzensfaden">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<meta name="theme-color" content="#fbf5ef">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..600;1,9..144,400..500&family=Nunito+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cpath d='M23.6 4c-3.4 0-6.3 2.7-7.6 5.6C14.7 6.7 11.8 4 8.4 4 3.8 4 0 7.8 0 12.4 0 21.8 9.5 24.3 16 34.1 22.1 24.3 32 21.5 32 12.4 32 7.8 28.2 4 23.6 4z' fill='%23eb458d'/%3E%3C/svg%3E">
{jsonld}
</head>
<body>
{header}
<main id="main">
{body}
</main>
{footer}
<script src="assets/js/main.js" defer></script>
{analytics}
</body>
</html>
'''

def page_url(slug):
    return BASE_URL + "/" + ("" if slug == "index" else slug + ".html")

def render(slug, title, desc, active, robots=""):
    body_path = os.path.join(ROOT, "content", slug + ".html")
    with open(body_path, encoding="utf-8") as f:
        body = f.read().strip()
    return TEMPLATE.format(
        title=title, desc=desc,
        canonical=page_url(slug), og_image=OG_IMAGE,
        robots=("\n" + robots if robots else ""),
        jsonld=JSONLD,
        header=header(active), body=body, footer=FOOTER,
        analytics=ANALYTICS,
    )

def write(name, content):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(content)

def build():
    for slug, title, desc, active in PAGES:
        html = render(slug, title, desc, active)
        write(slug + ".html", html)
        print("built", slug + ".html", f"({len(html)//1024} kB)")

    # Eigene 404-Seite (von Suchmaschinen ausgenommen)
    write("404.html", render(
        "404", "Seite nicht gefunden | Herzensfaden",
        "Diese Seite wurde nicht gefunden. Zur Startseite von Herzensfaden zurückkehren.",
        "none", robots='<meta name="robots" content="noindex">'))
    print("built 404.html")

    # sitemap.xml
    today = datetime.date.today().isoformat()
    urls = "\n".join(
        f"  <url><loc>{page_url(slug)}</loc><lastmod>{today}</lastmod></url>"
        for slug, *_ in PAGES
    )
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               f"{urls}\n</urlset>\n")
    write("sitemap.xml", sitemap)
    print("built sitemap.xml")

    # robots.txt
    robots_txt = ("User-agent: *\nAllow: /\n\n"
                  f"Sitemap: {BASE_URL}/sitemap.xml\n")
    write("robots.txt", robots_txt)
    print("built robots.txt")

if __name__ == "__main__":
    build()
