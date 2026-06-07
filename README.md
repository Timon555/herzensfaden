# Herzensfaden – Website

Moderne Website für **Brigitte Meissner** – Hebamme, Craniosacral-Therapeutin und Autorin in Winterthur.
Themen: Geburten verarbeiten, Mutter-Kind-Bindung fördern, Fortbildungen für Fachpersonen, Bücher und Karten.

Statische Website ohne Build-Abhängigkeiten – reines HTML, CSS und etwas JavaScript.

## Seiten
- `index.html` – Start
- `ueber-mich.html` – Über Brigitte Meissner
- `praxis.html` – Praxis & Therapie (mit Karte)
- `kurse-fachpersonen.html` – Fortbildungen (Module & Kursdaten)
- `kurse-eltern.html` – Kurse für Eltern
- `babyheilbad.html` – Babyheilbad (Merkblatt-PDF)
- `buecher.html` – Bücher (Bestellung CH / DE)
- `poster-postkarten.html` – Poster & Postkarten
- `kontakt.html` – Kontakt & hilfreiche Adressen
- `impressum.html` – Impressum & Datenschutz

## Lokale Vorschau
```bash
python3 -m http.server 8080
# dann http://127.0.0.1:8080 öffnen
```

## Seiten bearbeiten / neu bauen
Die Seiten teilen sich Kopf- und Fusszeile. Inhalte liegen in `content/`,
das gemeinsame Layout in `build.py`:
```bash
python3 build.py   # erzeugt die fertigen *.html im Hauptordner
```

## Verzeichnis
```
assets/css/styles.css   Design-System "Warm & geborgen"
assets/js/main.js       Navigation, Animationen, CH/DE-Umschalter
assets/img/             Bilder
assets/files/           PDF & Bestellformulare
content/                Seiteninhalte (Quelle für build.py)
build.py                Generator
```

© Brigitte Meissner, Winterthur. Fotos und Texte dürfen ohne schriftliche Genehmigung nicht verwendet werden.
