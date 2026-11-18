# ISPM15 Desk – zweisprachige Landingpage für GitHub Pages

**Deutsch · English | Dark-Violet-Design mit Glow-Effekten | Statisches HTML, CSS und JavaScript | Kein Webserver für das Hosting**

Diese Website wurde auf Grundlage der vom Auftraggeber bereitgestellten ISPM-15-Markt-, Zielgruppen- und Entwicklungsunterlagen erstellt. Sie stellt **ein in Entwicklung befindliches Pilotprodukt** für Holzverpackungs- und Palettenbetriebe vor; sie behauptet bewusst weder fertige Kundenprojekte noch gemessene Einsparungen oder bestehende Zertifizierungen.

## Projekt-Links

| Zweck | Link |
|---|---|
| GitHub-Repository | <https://github.com/JohannKern/ISPM15_Landingpage> |
| Pages-Einstellungen (Aktivierung) | <https://github.com/JohannKern/ISPM15_Landingpage/settings/pages> |
| Live-Seite Deutsch | <https://johannkern.github.io/ISPM15_Landingpage/> |
| Live-Seite English | <https://johannkern.github.io/ISPM15_Landingpage/en/> |
| Impressum / Datenschutz (DE) | <https://johannkern.github.io/ISPM15_Landingpage/impressum.html> · <https://johannkern.github.io/ISPM15_Landingpage/datenschutz.html> |
| Legal notice / Privacy (EN) | <https://johannkern.github.io/ISPM15_Landingpage/en/legal.html> · <https://johannkern.github.io/ISPM15_Landingpage/en/privacy.html> |

> **Status (18.11.2026):** GitHub Pages ist aktiv (Branch `main`, Ordner `/`) und die Seite ist online – **aber nur als Testseite**: `site.config.json` ist noch nicht ausgefüllt, Impressum, „Über mich" und Datenschutz enthalten Platzhalter, das Formular hat noch keinen Formspree-Endpunkt, und alle Seiten tragen `noindex,nofollow`. Vor einer echten Veröffentlichung bzw. vor Nutzung der Seite in der E-Mail-Kampagne Abschnitt 1 abarbeiten. Die URL `https://johannkern.github.io/ISPM15_Landingpage/` ist die `site_url` für den separaten E-Mail-Flyer.

## 1. Vor der Liveschaltung (wichtig)

Die Dateien sind technisch fertig für GitHub Pages. **Vor einem öffentlichen, rechtssicheren Betrieb sind echte Betreiberangaben und ein externer Formularservice nötig.** Niemand hat Name, berufliche Qualifikationen, Kontaktadresse oder Formspree-Konto des Auftraggebers mitgeliefert. Diese Informationen sind daher nicht erfunden worden.

1. Öffne `site.config.json` und trage die echten Angaben ein. **Pflicht für Freigabe des Suchmaschinen-Indexings:** `owner_name`, `street_address`, `postal_code`, `city`, `phone`, `contact_email`, `formspree_endpoint`, die deutschen und englischen `about_role_*`, `about_background_*`, `about_expertise_*` und `privacy_retention_*`-Felder. `business_name`, `legal_form`, `representative`, Register und USt-ID sind bei zutreffender Rechtsform ebenfalls sachlich korrekt anzugeben.
2. Prüfe jede Angabe des Impressums. Bei geschäftsmäßigen Websites in Deutschland gilt grundsätzlich **§ 5 DDG**. Welche zusätzlichen Angaben erforderlich sind, hängt von der Rechtsform und Tätigkeit ab.
3. Erstelle bei **Formspree** ein Formular und setze den Endpoint als `formspree_endpoint`, z. B. `https://formspree.io/f/abcdefgh` (nur ein Beispiel, kein funktionierender Account). Aktiviere die Benachrichtigung an deine eigene E-Mail-Adresse im Formspree-Konto.
4. **Datenschutz prüfen**: Formspree-Vertrag / Auftragsverarbeitung, ggf. Drittlandübermittlungen, Art und Dauer der Speicherung, Hosting, Datenschutzrechte. Lasse Impressum und Datenschutzhinweise anhand deines tatsächlichen Betriebs juristisch prüfen. Passe die Texte an, falls du weitere Dienste hinzufügst. Die Website verwendet selbst keine Marketing-Tracker, fremden Schriftdateien oder Tracking-Cookies. Externe Formularanbieter können eigene Verarbeitungsvorgänge haben.
5. Generiere die acht HTML-Seiten nach der Konfiguration erneut und teste **eine echte Demoanfrage** inklusive Empfang und Bestätigungs-/Fehlerfall.
6. Prüfe, ob der Produktname **ISPM15 Desk** für deine Nutzung markenrechtlich verfügbar ist. Dies ist ein vorgeschlagener Projektname, keine geprüfte Marke.

> **Veröffentlichungsschutz:** Solange wesentliche Angaben fehlen, generiert das Skript für alle Seiten `<meta name="robots" content="noindex,nofollow">`. Die Seiten sind dann **trotzdem öffentlich aufrufbar**; `noindex` ersetzt **keinen** Zugangsschutz und macht unvollständige Pflichtangaben nicht rechtmäßig.

## 2. Formular über Formspree aktivieren

1. Registriere ein eigenes Konto auf <https://formspree.io/>.
2. Lege ein Formular für Demoanfragen an und bestätige deine Empfangsadresse.
3. Kopiere den **öffentlichen Formular-Endpunkt** in `site.config.json` unter `formspree_endpoint`.
4. Führe das Build-Skript aus (siehe unten).
5. Sende von der veröffentlichten Website aus eine Testanfrage. Prüfe den Eingang im Formspree-Dashboard **und** im verbundenen Postfach. Bestätige in den Formspree-Einstellungen gegebenenfalls die Domain und Spam-Schutzoptionen.

Der Formularcode verwendet HTML5-Pflichtfelder, ein unsichtbares Honeypot-Feld und `fetch()` mit `Accept: application/json`. **Nur eine erfolgreiche HTTP-Antwort führt zur Erfolgsmeldung.** Fehler werden angezeigt; die bereits eingegebenen Angaben bleiben bei fehlgeschlagenem Versand erhalten. Ohne JavaScript kann das Formular bei konfiguriertem Formspree-Endpunkt auch per normalem HTML-POST übermittelt werden. Bei nicht konfiguriertem Endpunkt verhindert das JavaScript einen irreführenden „Erfolg“.

**Datenschutz:** Ein Formularservice kann personenbezogene Daten verarbeiten. Die technische Integration ist keine Garantie für DSGVO-Konformität. Nutze einen passenden AV-Vertrag / andere geeignete Garantien und überprüfe die konkreten Vertrags- und Datenflussbedingungen. Es werden keine geheimen API-Schlüssel im Frontend benötigt; die Formspree-Form-ID ist öffentlich.

Offizielle Anleitung: <https://formspree.io/html/> · <https://help.formspree.io/articles/building-your-form/submit-forms-with-javascript-ajax>

## 3. Inhalte bearbeiten

Alle wiederkehrenden persönlichen Angaben liegen in **`site.config.json`** und werden durch `scripts/build.py` in die Seiten übernommen.

### Konfiguration und neu erzeugen

```bash
python3 scripts/build.py
```

Kein Python-Paket muss installiert werden. Die HTML-Dateien sind nach dem Bauen **sofort statisch nutzbar**. Du kannst auch direkt HTML/CSS ändern; wenn du `build.py` später noch einmal startest, werden direkte Änderungen an den acht generierten HTML-Dateien jedoch überschrieben. Für dauerhafte Änderungen passe `scripts/build.py` bzw. `assets/css/style.css` und `assets/js/site.js` an.

### Lokale Vorschau

```bash
python3 -m http.server 8000
```

Im Browser öffnen: <http://localhost:8000/> (Deutsch) und <http://localhost:8000/en/> (Englisch). Alternativ lassen sich die HTML-Dateien direkt öffnen. Die Demo-Übermittlung benötigt den konfigurierten externen Service und eine Internetverbindung.

## 4. Auf GitHub Pages veröffentlichen

1. ✅ Repository angelegt: <https://github.com/JohannKern/ISPM15_Landingpage> (öffentlich, Branch `main`).
2. ✅ Inhalte dieses Projektordners liegen im Repository-Stamm (`/`). `ChatGPT.md` ist über `.gitignore` ausgeschlossen. Änderungen später per `git add -A`, `git commit` und `git push` hochladen.
3. ✅ Pages aktiviert (Testseite): <https://github.com/JohannKern/ISPM15_Landingpage/settings/pages> → **Build and deployment → Source → Deploy from a branch → `main` → `/(root)`**.
4. Warten, bis GitHub Pages die Veröffentlichung abgeschlossen hat (Fortschritt unter <https://github.com/JohannKern/ISPM15_Landingpage/actions>); anschließend <https://johannkern.github.io/ISPM15_Landingpage/> öffnen.
5. Links der deutschen und englischen Website, das mobile Menü, Impressum, Datenschutz und echte Demoübermittlung erneut prüfen. Falls gewünscht, eine eigene Domain in GitHub Pages einrichten und HTTPS aktivieren.

**Wichtig:** GitHub Pages stellt nur statische Dateien bereit und kann selbst keine Formular-E-Mails versenden oder Django/PostgreSQL hosten. Die spätere SaaS-Anwendung aus deinen Unterlagen ist ein **separates Backend-Projekt**; die hier gelieferte Marketingwebsite benötigt dieses Backend nicht.

Offizielle GitHub-Anleitung: <https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>

## 5. Projektstruktur

```text
index.html                  Deutsche Landingpage (Startpunkt)
about.html                  Über mich (DE)
impressum.html              Impressum (DE)
datenschutz.html            Datenschutzerklärung (DE)
en/
  index.html                English landing page
  about.html                About me
  legal.html                Legal notice
  privacy.html              Privacy policy
assets/
  css/style.css             Basislayout und Responsive-Styles
  css/dark-theme.css        Dark-Theme: Violett/Schwarz, Lichtbögen, Karten, Formulare
  js/site.js                Mobile Navigation + Formspree-Formular
  images/favicon.svg       Eigenes violettes SVG-Favicon
site.config.json            Stammdaten, persönliches Profil und Formspree-Endpunkt
scripts/build.py            Generiert alle acht HTML-Seiten, keine Abhängigkeiten
.nojekyll                   Deaktiviert Jekyll-Verarbeitung für GitHub Pages
README.md                   Diese Anleitung
```

## 6. Design, Sprache und inhaltliche Grenzen

- Responsiv für Desktop, Tablet und Smartphone, inklusive mobiler Menüführung, Fokuszuständen und `prefers-reduced-motion`.
- Durchgängiges **Dark-Violet-Theme**: tiefe Aubergine-/Schwarztöne, weiche violette Lichtverläufe, Halo im Hero, halbtransparente dunkle Karten und kontrastreiche helle Typografie. Visuell an der vom Auftraggeber bereitgestellten Referenz orientiert, ohne fremde Logos oder Designs zu übernehmen.
- Für Farbanpassungen **`assets/css/dark-theme.css`** bearbeiten: Die Datei wird nach `style.css` geladen und überschreibt den Basisstil. Nach Änderungen an `scripts/build.py` kannst du die acht Seiten mit `python3 scripts/build.py` regenerieren; die Theme-Datei wird dabei nicht überschrieben.
- Deutsch und Englisch als **eigene HTML-Seiten**, per Sprachumschalter erreichbar; SEO-Sprachtags und `<html lang>` sind gesetzt.
- CSS/JS lokal; alle Glow-Effekte sind CSS-only, kein CDN, kein Remote-Font, keine unnötigen Frameworks, keine Tracking-/Marketing-Pixel.
- Produktdashboard ist ausdrücklich als **Konzeptansicht mit Beispieldaten** bezeichnet. Es zeigt **keine** reale oder angeblich produktiv laufende SaaS-Instanz.
- Funktionen sind als **geplant** formuliert, da die Dokumente die Validierung und phasenweise Entwicklung des Produkts beschreiben, nicht eine ausgelieferte Software.
- Zielgruppe und Workflow folgen den Unterlagen: **Lieferanten → Holzlieferungen → Behandlungs-/Lieferdokumente → Vollständigkeitsprüfung → kontrollgeeigneter Export**.
- Kundenliste und Kontaktdaten aus der Excel-Datei werden **nicht** öffentlich mit der Website ausgeliefert. Recherchezahlen wurden nicht als Testimonials, Kundenlogos oder Produktnachweise missbraucht.
- Der Bereich „Über mich“ enthält bewusst Platzhalter für persönliche Biografie und Erfahrung, die aus den Dokumenten nicht hervorgehen.

### Vor Veröffentlichung besonders prüfen

```text
[ ] Name, Rechtsform, Anschrift, Kontakt (und Register-/Steuerangaben, soweit erforderlich)
[ ] Persönlicher Werdegang, Rolle und fachliche Expertise (DE + EN)
[ ] Formspree eingerichtet und echte erfolgreiche Testanfrage geprüft
[ ] Datenschutzerklärung an Dienstleister, Verträge und Speicherfristen angepasst
[ ] Domain/HTTPS, alle Seitenlinks, mobile Darstellung und Sprache geprüft
[ ] Produktname und Aussagen fachlich/rechtlich geprüft
[ ] Erneut python3 scripts/build.py ausgeführt und noindex-Status geprüft
```

Rechtlicher Ausgangspunkt: <https://www.gesetze-im-internet.de/ddg/__5.html> · Hinweise zu Kontaktformularen: <https://www.ihk-muenchen.de/ratgeber/recht/datenschutz/eu-datenschutz-grundverordnung/datenschutz-bei-webseiten/>
