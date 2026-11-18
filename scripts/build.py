#!/usr/bin/env python3
"""Regenerate standalone GitHub Pages HTML. No third-party Python dependencies."""
from __future__ import annotations
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / 'site.config.json').read_text(encoding='utf-8'))

def esc(value):
    return html.escape(str(value or ''), quote=True)

def field(key, de='[Angabe ergänzen]', en='[Add information]'):
    return esc(CFG.get(key)) if str(CFG.get(key, '')).strip() else f'<span class="not-set">{de if LANG == "de" else en}</span>'

def legal_owner():
    return esc(CFG.get('business_name') or CFG.get('owner_name')) if (CFG.get('business_name') or CFG.get('owner_name')) else field('owner_name', '[Name / Firma]', '[Name / business]')

def icon(name, size=22, cls=''):
    paths = {
        'arrow': '<path d="M5 12h14m-6-6 6 6-6 6"/>',
        'check': '<path d="m5 12 4 4L19 6"/>',
        'folder': '<path d="M3 8a2 2 0 0 1 2-2h5l2 2h7a2 2 0 0 1 2 2v9H3z"/>',
        'shield': '<path d="m12 2 8 4v6c0 5.5-3.7 8.7-8 10-4.3-1.3-8-4.5-8-10V6z"/><path d="m9 12 2 2 4-4"/>',
        'box': '<path d="m12 2 9 5-9 5-9-5zM3 7v10l9 5 9-5V7M12 12v10"/>',
        'search': '<circle cx="10.7" cy="10.7" r="7.2"/><path d="m16 16 5 5"/>',
        'file': '<path d="M6 2h8l4 4v16H6zM14 2v5h5M9 12h6M9 16h6"/>',
        'download': '<path d="M12 3v12m-4-4 4 4 4-4M4 17v4h16v-4"/>',
        'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
        'layers': '<path d="m12 3 9 5-9 5-9-5zM3 12l9 5 9-5M3 16l9 5 9-5"/>',
        'spark': '<path d="m12 2 1.8 6.2L20 10l-6.2 1.8L12 18l-1.8-6.2L4 10l6.2-1.8zM19 18l.7 1.3L21 20l-1.3.7L19 22l-.7-1.3L17 20l1.3-.7z"/>',
        'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
        'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 7 9-7"/>',
        'lock': '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    }
    return f'<svg class="{cls}" width="{size}" height="{size}" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round">{paths[name]}</svg>'

COPY = {
'de': {
 'meta_title': 'ISPM15 Desk – ISPM-15-Nachweise einfach verwalten',
 'meta_desc': 'Die geplante digitale Nachweisverwaltung für Holzverpackungs- und Palettenbetriebe. Lieferungen, Behandlungsbelege und Kontrollakten an einem Ort. Jetzt Pilot-Demo anfragen.',
 'about_meta': 'Über das Projekt und die Person hinter ISPM15 Desk: eine schlanke ISPM-15-Nachweisverwaltung mit Fokus auf echte betriebliche Abläufe.',
 'nav_how': 'So funktioniert’s', 'nav_features': 'Funktionen', 'nav_about': 'Über mich', 'nav_demo': 'Demo anfordern',
 'nav_aria': 'Hauptnavigation', 'menu': 'Menü öffnen', 'lang_aria': 'Sprache wählen',
 'footer_tagline': 'Weniger suchen. Mehr Überblick.', 'footer_desc': 'Eine fokussierte Softwareidee für ISPM-15-Nachweise in Holzverpackungs- und Palettenbetrieben.',
 'footer_product': 'Produkt', 'footer_company': 'Informationen', 'footer_home': 'Startseite', 'footer_privacy': 'Datenschutz', 'footer_imprint': 'Impressum',
 'footer_disclaimer': 'Unabhängiges Softwareprojekt. Keine offizielle Zertifizierungs- oder Behördenplattform.',
 'demo_short': 'Unverbindlich anfragen',
},
'en': {
 'meta_title': 'ISPM15 Desk – Simplify ISPM 15 documentation',
 'meta_desc': 'A focused documentation workspace for wood packaging and pallet manufacturers. Manage shipments, treatment records and audit-ready exports. Request a pilot demo.',
 'about_meta': 'Meet the idea and person behind ISPM15 Desk: focused software for real-life ISPM 15 documentation workflows.',
 'nav_how': 'How it works', 'nav_features': 'Features', 'nav_about': 'About me', 'nav_demo': 'Request a demo',
 'nav_aria': 'Main navigation', 'menu': 'Open menu', 'lang_aria': 'Select language',
 'footer_tagline': 'Less searching. More clarity.', 'footer_desc': 'A focused software concept for ISPM 15 documentation in wood packaging and pallet businesses.',
 'footer_product': 'Product', 'footer_company': 'Information', 'footer_home': 'Home', 'footer_privacy': 'Privacy policy', 'footer_imprint': 'Legal notice',
 'footer_disclaimer': 'Independent software project. Not an official certification or government platform.',
 'demo_short': 'Get in touch',
}}

LANG = 'de'

def paths(page):
    prefix = '' if LANG == 'de' else '../'
    local_home = 'index.html' if LANG == 'de' else 'index.html'
    if LANG == 'de':
        return dict(home='index.html', about='about.html', legal='impressum.html', privacy='datenschutz.html', assets='assets/', other={'home':'en/index.html','about':'en/about.html','legal':'en/legal.html','privacy':'en/privacy.html'})
    return dict(home='index.html', about='about.html', legal='legal.html', privacy='privacy.html', assets='../assets/', other={'home':'../index.html','about':'../about.html','legal':'../impressum.html','privacy':'../datenschutz.html'})

def head(page):
    c = COPY[LANG]; p = paths(page)
    title = {'home':c['meta_title'], 'about':c['nav_about'] + ' | ' + CFG['site_name'], 'legal':c['footer_imprint']+' | '+CFG['site_name'], 'privacy':c['footer_privacy']+' | '+CFG['site_name']}[page]
    desc = c['about_meta'] if page == 'about' else c['meta_desc'] if page == 'home' else title
    altlang = 'en' if LANG == 'de' else 'de'
    endpoint_ok = bool(re.fullmatch(r'https://formspree\.io/f/[a-zA-Z0-9]+', CFG.get('formspree_endpoint','')))
    must = ['owner_name', 'street_address', 'postal_code', 'city', 'contact_email', 'phone']
    ready = endpoint_ok and all(str(CFG.get(k,'')).strip() for k in must) and all(str(CFG.get(k,'')).strip() for k in ['about_role_de','about_role_en','about_background_de','about_background_en','about_expertise_de','about_expertise_en','privacy_retention_de','privacy_retention_en'])
    robots = 'index,follow' if ready else 'noindex,nofollow'
    return f'''<!doctype html>
<html lang="{LANG}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#100919">
  <meta name="robots" content="{robots}">
  <meta name="description" content="{esc(desc)}">
  <meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
  <title>{esc(title)}</title>
  <link rel="alternate" hreflang="{LANG}" href="{esc(p['home'] if page == 'home' else p[page])}">
  <link rel="alternate" hreflang="{altlang}" href="{esc(p['other'][page])}">
  <link rel="icon" type="image/svg+xml" href="{p['assets']}images/favicon.svg">
  <link rel="stylesheet" href="{p['assets']}css/style.css">
  <link rel="stylesheet" href="{p['assets']}css/dark-theme.css">
  <script src="{p['assets']}js/site.js" defer></script>
</head>
<body data-lang="{LANG}" data-page="{page}">
<a href="#main" class="skip-link">{'Zum Inhalt springen' if LANG=='de' else 'Skip to content'}</a>'''

def header(page):
    c = COPY[LANG]; p = paths(page)
    ishome = page == 'home'
    brand = f'<a class="brand" href="{p["home"]}" aria-label="{esc(CFG["site_name"])} – {c["footer_home"]}"><span class="brand-symbol" aria-hidden="true"><span></span><span></span><span></span></span><span class="brand-words">ISPM<span class="brand-number">15</span><span class="brand-desk">Desk</span></span></a>'
    features = '#features' if LANG == 'en' else '#funktionen'
    how = '#workflow' if LANG == 'en' else '#ablauf'
    demo = '#demo'
    return f'''<header class="site-header"><div class="shell header-inner">
  {brand}
  <button class="menu-toggle" aria-controls="primary-nav" aria-expanded="false" aria-label="{c['menu']}">{icon('menu',24)}</button>
  <nav id="primary-nav" class="primary-nav" aria-label="{c['nav_aria']}">
    <a class="nav-link" href="{p['home']}{how}">{c['nav_how']}</a>
    <a class="nav-link" href="{p['home']}{features}">{c['nav_features']}</a>
    <a class="nav-link {'active' if page=='about' else ''}" {'aria-current="page"' if page=='about' else ''} href="{p['about']}">{c['nav_about']}</a>
    <div class="header-extras"><div class="lang-switch" aria-label="{c['lang_aria']}">
      <a href="{p['other'][page]}" lang="{'en' if LANG=='de' else 'de'}" hreflang="{'en' if LANG=='de' else 'de'}" class="lang-option">{'EN' if LANG=='de' else 'DE'}</a><span class="lang-separator" aria-hidden="true">/</span><span class="lang-current" aria-current="true">{'DE' if LANG=='de' else 'EN'}</span>
    </div><a class="btn btn-nav" href="{p['home']}{demo}">{c['nav_demo']}{icon('arrow',17)}</a></div>
  </nav>
</div></header>'''

def footer(page):
    c=COPY[LANG]; p=paths(page)
    return f'''<footer class="site-footer"><div class="shell">
  <div class="footer-top"><div class="footer-intro"><a class="brand brand-footer" href="{p['home']}"><span class="brand-symbol" aria-hidden="true"><span></span><span></span><span></span></span><span class="brand-words">ISPM<span class="brand-number">15</span><span class="brand-desk">Desk</span></span></a><h2>{c['footer_tagline']}</h2><p>{c['footer_desc']}</p></div>
  <div class="footer-columns"><div><h3>{c['footer_product']}</h3><a href="{p['home']}">{c['footer_home']}</a><a href="{p['home']}#{'funktionen' if LANG=='de' else 'features'}">{c['nav_features']}</a><a href="{p['home']}#demo">{c['nav_demo']}</a></div><div><h3>{c['footer_company']}</h3><a href="{p['about']}">{c['nav_about']}</a><a href="{p['legal']}">{c['footer_imprint']}</a><a href="{p['privacy']}">{c['footer_privacy']}</a></div></div></div>
  <div class="footer-bottom"><span>© 2026 ISPM15 Desk. {c['footer_disclaimer']}</span><span>{'Mit Fokus auf reale Arbeitsabläufe.' if LANG=='de' else 'Built around real-world workflows.'}</span></div>
</div></footer>'''

def wrap(page, content):
    return head(page)+'\n'+header(page)+'\n<main id="main">\n'+content+'\n</main>\n'+footer(page)+'\n</body>\n</html>\n'

DASHBOARD = {
'de':dict(overview='Übersicht',demo='Konzeptansicht · Beispieldaten',date='November 2026',welcome='Guten Morgen',sub='Ihre Nachweise auf einen Blick.',all='Lieferungen',complete='Vollständig',open='Zur Prüfung',recent='Aktuelle Lieferungen',col1='Lieferung',col2='Lieferant',col3='Status',row1='Holzlieferung #084',row2='Holzlieferung #083',row3='Holzlieferung #082',supplier1='Musterholz GmbH',supplier2='Beispiel Sägewerk',supplier3='Nordwald Holz',status1='Vollständig',status2='Prüfen',status3='Vollständig',floating='Noch 1 Nachweis offen',floatdesc='Im Blick statt übersehen',compliance='Dokumentenstatus',percent='14 von 18 vollständig'),
'en':dict(overview='Overview',demo='Concept preview · Sample data',date='November 2026',welcome='Good morning',sub='Your records at a glance.',all='Shipments',complete='Complete',open='To review',recent='Recent shipments',col1='Shipment',col2='Supplier',col3='Status',row1='Shipment #084',row2='Shipment #083',row3='Shipment #082',supplier1='Sample Timber Ltd',supplier2='Example Sawmill',supplier3='Northern Wood',status1='Complete',status2='Review',status3='Complete',floating='1 record needs attention',floatdesc='Visible. Not forgotten.',compliance='Record status',percent='14 of 18 complete')}

def dashboard():
    d=DASHBOARD[LANG]
    return f'''<div class="dashboard-stage"><div class="dash-float dash-float-top">{icon('shield',16)}<span>{d['demo']}</span></div>
<div class="dashboard" role="img" aria-label="{'Schematische Vorschau der geplanten Software mit fiktiven Daten' if LANG=='de' else 'Conceptual product interface with fictional sample data'}">
  <div class="dash-side"><div class="dash-side-logo">D<span>.</span></div><span class="side-dot side-dot-active">{icon('layers',17)}</span><span class="side-dot">{icon('box',17)}</span><span class="side-dot">{icon('file',17)}</span><span class="side-dot">{icon('search',17)}</span><span class="side-gear">•••</span></div>
  <div class="dash-main"><div class="dash-top"><span>{d['overview']} <span class="muted">/ {d['date']}</span></span><span class="dash-avatar">IS</span></div>
  <div class="dash-hello"><h3>{d['welcome']} <span class="dash-wave">✳</span></h3><p>{d['sub']}</p></div>
  <div class="dash-metrics"><div class="dash-stat"><small>{d['all']}</small><strong>18</strong><span class="dash-graph">▁▃▄▂▅▇</span></div><div class="dash-stat"><small>{d['complete']}</small><strong>14</strong><span class="dash-stat-pill pill-green">{icon('check',12)} 78%</span></div><div class="dash-stat"><small>{d['open']}</small><strong>04</strong><span class="dash-stat-pill pill-amber">{icon('clock',12)} 4</span></div></div>
  <div class="dash-table-wrap"><div class="dash-table-title"><b>{d['recent']}</b><span>•••</span></div><div class="dash-table"><div class="dash-table-row dash-table-head"><span>{d['col1']}</span><span>{d['col2']}</span><span>{d['col3']}</span></div>
  <div class="dash-table-row"><span><i class="doc-glyph">{icon('file',13)}</i>{d['row1']}</span><span>{d['supplier1']}</span><span><em class="status-pill done">● {d['status1']}</em></span></div>
  <div class="dash-table-row"><span><i class="doc-glyph">{icon('file',13)}</i>{d['row2']}</span><span>{d['supplier2']}</span><span><em class="status-pill review">● {d['status2']}</em></span></div>
  <div class="dash-table-row"><span><i class="doc-glyph">{icon('file',13)}</i>{d['row3']}</span><span>{d['supplier3']}</span><span><em class="status-pill done">● {d['status3']}</em></span></div>
  </div></div></div>
</div><div class="dash-floating-card"> <span class="float-alert">{icon('file',18)}</span><span><strong>{d['floating']}</strong><small>{d['floatdesc']}</small></span><span class="float-arrow">↗</span></div></div>'''

DE = {
  'hero_eyebrow':'Für Holzverpackungs- & Palettenbetriebe',
  'hero_title':'Alle ISPM-15-Nachweise.<br><em>Endlich an einem Ort.</em>',
  'hero_desc':'Lieferungen erfassen, Behandlungsnachweise organisieren und fehlende Angaben rechtzeitig erkennen. Damit aus verstreuten Dokumenten eine klare, auffindbare Nachweisakte wird.',
  'hero_primary':'Pilot-Demo anfragen', 'hero_secondary':'So funktioniert’s',
  'hero_note':'In Entwicklung · Wir suchen Pilotbetriebe',
  'trust_intro':'Entwickelt für einen klaren Anwendungsfall',
  'trust1':'Holzverpackungen & Paletten', 'trust2':'ISPM-15-Dokumentation', 'trust3':'Ohne ERP-Wechsel geplant',
  'pain_eyebrow':'KENNEN SIE DAS?', 'pain_title':'Dokumentation sollte kein zweiter Vollzeitjob sein.',
  'pain_desc':'Die richtigen Unterlagen sind oft vorhanden – aber nicht dort, wo man sie gerade braucht. Genau hier setzt ISPM15 Desk an.',
  'paincards':[
    ('01','Verstreute Unterlagen','Lieferscheine, Rechnungen und Behandlungsbelege liegen in E-Mails, Ordnern oder unterschiedlichen Ablagen.'),
    ('02','Offene Nachweisfragen','Ob Angaben oder Lieferantennachweise fehlen, fällt häufig erst bei einer Rückfrage oder Kontrolle auf.'),
    ('03','Zeitverlust bei Kontrollen','Wer Nachweise manuell zusammensucht, verliert Zeit, die im laufenden Betrieb besser eingesetzt wäre.')
  ],
  'workflow_eyebrow':'EINFACHER ABLAUF', 'workflow_title':'Vom Wareneingang zur Kontrollakte.','workflow_desc':'Ein klarer Prozess, der den Betrieb unterstützt, statt neue Komplexität zu schaffen.',
  'steps':[
    ('01','Lieferanten anlegen','Lieferantenstammdaten und vorhandene Berechtigungsunterlagen geordnet hinterlegen.'),
    ('02','Lieferungen erfassen','Holzlieferungen mit Datum, Menge, Behandlung und Referenz dokumentieren.'),
    ('03','Nachweise zuordnen','Belege ablegen und fehlende Angaben in der Übersicht erkennen.'),
    ('04','Akte bereitstellen','Gesuchte Vorgänge filtern und die zugehörigen Dokumente strukturiert exportieren.')
  ],
  'features_eyebrow':'DIE GEPLANTE PILOTVERSION', 'features_title':'Alles Wichtige. Ohne unnötigen Ballast.',
  'features_desc':'Die erste Version konzentriert sich bewusst auf den täglichen Nachweisprozess. Zusätzliche Automatisierung folgt nur, wenn sie echten Mehrwert schafft.',
  'features':[
    ('layers','Ein zentraler Überblick','Lieferungen, offene Vorgänge und Nachweisstatus auf einer klaren Oberfläche.'),
    ('box','Lieferungen & Lieferanten','Lieferungen samt Mengen, Referenzen, Behandlungsangaben und Lieferanten verwalten.'),
    ('folder','Dokumente am richtigen Ort','Lieferscheine, Rechnungen und Behandlungspapiere nachvollziehbar zuordnen.'),
    ('shield','Vollständigkeit im Blick','Hinweise auf fehlende Felder und nicht zugeordnete Unterlagen erhalten.'),
    ('search','Wiederfinden statt Suchen','Nach Lieferanten, Zeiträumen, Referenzen und Bearbeitungsstatus filtern.'),
    ('download','Kontrollakten exportieren','Zugehörige Nachweise für die betriebliche Prüfung gesammelt bereitstellen.')
  ],
  'feature_notice':'Konzept und geplanter MVP-Funktionsumfang – keine Behauptung einer bereits verfügbaren Produktivsoftware.',
  'fit_eyebrow':'FÜR WEN IST DAS GEDACHT?',
  'fit_title':'Gemacht für Betriebe, die Holz verarbeiten – nicht für IT-Abteilungen.',
  'fit_desc':'Besonders sinnvoll kann der Ansatz für Unternehmen sein, die regelmäßig bereits behandeltes Holz von mehreren Lieferanten beziehen und Nachweise bislang manuell verwalten.',
  'fit_bullets':['Holzverpackungs- und Exportpalettenhersteller','Kleine und mittelständische Betriebe','Regelmäßiger Dokumenteneingang','Wunsch nach einfacher Lösung statt umfassendem ERP-Projekt'],
  'fit_card_title':'Erst den Arbeitsablauf verstehen. Dann digitalisieren.',
  'fit_card_desc':'In der Pilotphase geht es um Ihren tatsächlichen Nachweisprozess – nicht um eine lange Liste theoretischer Funktionen.',
  'fit_card_kicker':'UNSER ANSATZ','fit_card1':'Schlanker Einstieg', 'fit_card1_desc':'Den Kernprozess zuerst nutzbar machen.', 'fit_card2':'Praxisnah weiterentwickeln', 'fit_card2_desc':'Erweiterungen an echten Rückmeldungen ausrichten.',
  'next_eyebrow':'BEWUSST SCHRITTWEISE', 'next_title':'Erst die Basis. Dann die Automatisierung.',
  'next_desc':'Geplant ist ein klarer Ausbaupfad – mit Raum für tatsächliche Kundenwünsche und ohne leere Funktionsversprechen.',
  'next1':'Pilotversion', 'next1_desc':'Lieferungen, Dokumente, Vollständigkeit und Export.',
  'next2':'Bei nachgewiesenem Bedarf', 'next2_desc':'Aufgaben, Fristen und Erinnerungen.',
  'next3':'Spätere Optionen', 'next3_desc':'Assistierte PDF-Erkennung und Lieferanten-Upload.',
  'demo_eyebrow':'JETZT INS GESPRÄCH KOMMEN', 'demo_title':'Weniger Papierarbeit beginnt mit einem Gespräch.',
  'demo_desc':'Erfahren Sie, wie ISPM15 Desk für Ihren Betrieb gedacht ist. Beschreiben Sie kurz Ihren Nachweisprozess und fragen Sie eine unverbindliche Pilot-Demo an.',
  'demo_expect_title':'Was Sie erwartet','demo_expect':['Ein Austausch über Ihren heutigen Nachweisprozess','Ein Einblick in das Produktkonzept und den Pilotumfang','Eine ehrliche Einschätzung, ob der Ansatz zu Ihnen passt'],
  'demo_form_heading':'Pilot-Demo anfragen','demo_form_sub':'Wir melden uns persönlich zur Abstimmung des nächsten Schritts.',
  'company':'Unternehmen', 'name':'Ihr Name','email':'Geschäftliche E-Mail','volume':'Nachweisvorgänge pro Monat','message':'Was kostet Sie heute am meisten Zeit? (optional)',
  'company_ph':'z. B. Muster Palettenbau GmbH', 'name_ph':'Vor- und Nachname','email_ph':'name@unternehmen.de','message_ph':'Ein paar Worte zu Ihrem aktuellen Ablauf ...',
  'select_default':'Bitte auswählen (optional)', 'volumes':[('under20','Unter 20'),('20to60','20–60'),('over60','Über 60'),('unknown','Kann ich noch nicht einschätzen')],
  'required':'Pflichtfeld', 'submit':'Demo anfordern', 'sending':'Wird gesendet ...',
  'form_privacy':'Mit dem Absenden verarbeiten wir Ihre Angaben zur Bearbeitung Ihrer Anfrage. Weitere Informationen in unserer <a href="datenschutz.html">Datenschutzerklärung</a>.',
  'form_success':'Vielen Dank! Ihre Anfrage wurde übermittelt. Wir melden uns so bald wie möglich.',
  'form_error':'Die Anfrage konnte nicht gesendet werden. Bitte versuchen Sie es später erneut.',
  'form_unconfigured':'Das Demoformular ist noch nicht freigeschaltet. Vor der Veröffentlichung muss der Formularservice eingerichtet werden.',
  'form_honeypot':'Dieses Feld leer lassen',
  'final_title':'Ihre Nachweise verdienen eine einfachere Lösung.', 'final_desc':'Lernen Sie das Konzept kennen und gestalten Sie die Pilotversion mit.', 'final_cta':'Demo anfordern',
}
EN = {
  'hero_eyebrow':'For wood packaging & pallet businesses',
  'hero_title':'Every ISPM 15 record.<br><em>Finally in one place.</em>',
  'hero_desc':'Track timber deliveries, organize treatment documents and spot missing details earlier. Turn scattered paperwork into a clear, searchable documentation file.',
  'hero_primary':'Request a pilot demo', 'hero_secondary':'See how it works',
  'hero_note':'In development · Seeking pilot partners',
  'trust_intro':'Purpose-built for one specific job',
  'trust1':'Wood packaging & pallets', 'trust2':'ISPM 15 documentation', 'trust3':'No ERP replacement planned',
  'pain_eyebrow':'SOUND FAMILIAR?', 'pain_title':'Documentation should not be a second full-time job.',
  'pain_desc':'The right records often exist — just not where you need them. That is the problem ISPM15 Desk is designed to address.',
  'paincards':[
    ('01','Scattered documents','Delivery notes, invoices and treatment records are spread across emails, folders and various systems.'),
    ('02','Missing information','Incomplete records or supplier documents often only become apparent when someone asks for proof.'),
    ('03','Time lost preparing for checks','Piecing together the right evidence manually takes time better spent running your business.')
  ],
  'workflow_eyebrow':'A CLEAR PROCESS', 'workflow_title':'From incoming delivery to audit file.',
  'workflow_desc':'A straightforward workflow designed to support your team, not add another layer of complexity.',
  'steps':[
    ('01','Add your suppliers','Keep supplier details and available authorisation documents together.'),
    ('02','Record deliveries','Log dates, quantities, treatment details and shipment references.'),
    ('03','Attach documentation','Connect documents to deliveries and make gaps easier to spot.'),
    ('04','Prepare your files','Filter records and export supporting documents in an organized package.')
  ],
  'features_eyebrow':'PLANNED PILOT FEATURES', 'features_title':'The essentials. Without the extra noise.',
  'features_desc':'The first version focuses on the daily documentation workflow. Further automation comes only when there is real value to unlock.',
  'features':[
    ('layers','One clear overview','See deliveries, outstanding items and document status in one place.'),
    ('box','Deliveries & suppliers','Manage quantities, references, treatment information and supplier details.'),
    ('folder','Documents where they belong','Link delivery notes, invoices and treatment records to the right entries.'),
    ('shield','Spot missing details','Flag incomplete fields and documents that still need attention.'),
    ('search','Find what you need','Filter by supplier, date, reference and processing status.'),
    ('download','Export organized records','Bring relevant evidence together for operational checks and inspections.')
  ],
  'feature_notice':'A concept preview and planned MVP scope, not a claim that production software is already available.',
  'fit_eyebrow':'WHO IS IT FOR?', 'fit_title':'For people working with wood. Not IT departments.',
  'fit_desc':'Especially relevant for businesses regularly sourcing pre-treated timber from multiple suppliers and handling documentation manually.',
  'fit_bullets':['Wood packaging and export pallet manufacturers','Small and midsize businesses','Regular inflow of documents','A need for a focused tool rather than a full ERP project'],
  'fit_card_title':'Understand the workflow first. Then digitize it.',
  'fit_card_desc':'The pilot is about your actual documentation process — not a long list of hypothetical features.',
  'fit_card_kicker':'OUR APPROACH','fit_card1':'Start focused', 'fit_card1_desc':'Make the core process useful first.', 'fit_card2':'Improve through feedback', 'fit_card2_desc':'Prioritize features based on real-world needs.',
  'next_eyebrow':'BUILT STEP BY STEP', 'next_title':'Start with clarity. Add automation later.',
  'next_desc':'A deliberate roadmap, shaped by real customer workflows rather than features promised too early.',
  'next1':'Pilot release', 'next1_desc':'Deliveries, documents, completeness and export.',
  'next2':'When there is proven demand', 'next2_desc':'Tasks, deadlines and reminders.',
  'next3':'Future possibilities', 'next3_desc':'Assisted PDF extraction and supplier uploads.',
  'demo_eyebrow':'LET’S TALK', 'demo_title':'Better documentation starts with a conversation.',
  'demo_desc':'See how ISPM15 Desk could fit your business. Tell us a little about your current process and request a no-obligation pilot demo.',
  'demo_expect_title':'What to expect','demo_expect':['A conversation about your current documentation workflow','A look at the product concept and planned pilot scope','A candid assessment of whether this solution makes sense for you'],
  'demo_form_heading':'Request a pilot demo','demo_form_sub':'We will get back to you personally to discuss the next step.',
  'company':'Company', 'name':'Your name', 'email':'Work email', 'volume':'Records processed per month', 'message':'What currently takes the most time? (optional)',
  'company_ph':'e.g. Example Pallets Ltd','name_ph':'First and last name','email_ph':'name@company.com','message_ph':'A few words about your current workflow ...',
  'select_default':'Select an option (optional)', 'volumes':[('under20','Under 20'),('20to60','20–60'),('over60','Over 60'),('unknown','Not sure yet')],
  'required':'Required', 'submit':'Request a demo', 'sending':'Sending ...',
  'form_privacy':'By submitting this form, you provide information used to respond to your enquiry. Read our <a href="privacy.html">privacy policy</a>.',
  'form_success':'Thank you! Your request has been sent. We will get back to you as soon as possible.',
  'form_error':'Your request could not be sent. Please try again later.',
  'form_unconfigured':'The demo form is not yet activated. A form service needs to be configured before launch.',
  'form_honeypot':'Leave this field blank',
  'final_title':'Your records deserve a simpler approach.', 'final_desc':'Explore the concept and help shape the pilot version.', 'final_cta':'Request a demo',
}

def demo_form(t):
    ep = CFG.get('formspree_endpoint','')
    ep_ok = bool(re.fullmatch(r'https://formspree\.io/f/[a-zA-Z0-9]+', ep))
    form_action = esc(ep) if ep_ok else '#demo'
    volume_options = ''.join(f'<option value="{v}">{txt}</option>' for v,txt in t['volumes'])
    return f'''<div class="demo-panel" id="demo"><div class="demo-copy"><p class="eyebrow eyebrow-light"><span class="eyebrow-line"></span>{t['demo_eyebrow']}</p><h2>{t['demo_title']}</h2><p class="demo-description">{t['demo_desc']}</p>
      <div class="demo-expect"><h3>{t['demo_expect_title']}</h3><ul>{''.join(f'<li>{icon("check",17)}<span>{v}</span></li>' for v in t['demo_expect'])}</ul></div>
      <div class="demo-decoration" aria-hidden="true"><span>15</span><span>DOCUMENTATION, SIMPLIFIED</span></div>
    </div>
    <div class="form-card"><div class="form-heading"><span class="form-mini-icon">{icon('mail',20)}</span><h3>{t['demo_form_heading']}</h3><p>{t['demo_form_sub']}</p></div>
    <form class="demo-form" data-demo-form data-endpoint="{form_action if ep_ok else ''}" data-msg-sending="{esc(t['sending'])}" data-msg-success="{esc(t['form_success'])}" data-msg-error="{esc(t['form_error'])}" data-msg-unconfigured="{esc(t['form_unconfigured'])}" action="{form_action}" method="POST" accept-charset="UTF-8">
      <input type="hidden" name="_subject" value="ISPM15 Desk – {'Demoanfrage' if LANG=='de' else 'Demo enquiry'}">
      <div class="trap" aria-hidden="true"><label for="website-check">{t['form_honeypot']}</label><input type="text" id="website-check" name="_gotcha" tabindex="-1" autocomplete="off"></div>
      <div class="form-grid"><div class="form-field"><label for="demo-company">{t['company']} <span aria-label="{t['required']}">*</span></label><input id="demo-company" name="company" type="text" placeholder="{esc(t['company_ph'])}" autocomplete="organization" maxlength="120" required></div>
      <div class="form-field"><label for="demo-name">{t['name']} <span aria-label="{t['required']}">*</span></label><input id="demo-name" name="name" type="text" placeholder="{esc(t['name_ph'])}" autocomplete="name" maxlength="100" required></div>
      <div class="form-field full"><label for="demo-email">{t['email']} <span aria-label="{t['required']}">*</span></label><input id="demo-email" name="email" type="email" placeholder="{esc(t['email_ph'])}" autocomplete="email" maxlength="160" required></div>
      <div class="form-field full"><label for="demo-volume">{t['volume']}</label><select id="demo-volume" name="monthly_volume"><option value="">{t['select_default']}</option>{volume_options}</select></div>
      <div class="form-field full"><label for="demo-message">{t['message']}</label><textarea id="demo-message" name="message" rows="3" maxlength="1500" placeholder="{esc(t['message_ph'])}"></textarea></div></div>
      <button class="btn btn-submit" type="submit" data-submit-button>{t['submit']}{icon('arrow',19)}</button>
      <p role="status" aria-live="polite" class="form-status" data-form-status></p>
      <p class="form-privacy">{icon('lock',14)}<span>{t['form_privacy']}</span></p>
    </form></div></div>'''

def landing():
    t=DE if LANG=='de' else EN
    wf_id='ablauf' if LANG=='de' else 'workflow'
    features_id='funktionen' if LANG=='de' else 'features'
    pains=''.join(f'<article class="pain-card"><span class="pain-index">{num}</span><h3>{title}</h3><p>{desc}</p><span class="pain-deco" aria-hidden="true">{icon("arrow",19)}</span></article>' for num,title,desc in t['paincards'])
    steps=''.join(f'<article class="step"><span class="step-number">{num}</span><div><h3>{title}</h3><p>{desc}</p></div></article>' for num,title,desc in t['steps'])
    features=''.join(f'<article class="feature-card"><span class="feature-icon">{icon(ic,25)}</span><h3>{title}</h3><p>{desc}</p></article>' for ic,title,desc in t['features'])
    bullets=''.join(f'<li>{icon("check",19)}<span>{i}</span></li>' for i in t['fit_bullets'])
    return f'''<section class="hero"><div class="hero-mesh" aria-hidden="true"></div><div class="shell hero-grid">
      <div class="hero-copy"><div class="hero-topline"><span class="tiny-ring" aria-hidden="true"></span>{t['hero_eyebrow']}</div><h1>{t['hero_title']}</h1><p class="hero-lead">{t['hero_desc']}</p>
        <div class="hero-actions"><a class="btn btn-primary btn-large" href="#demo">{t['hero_primary']}{icon('arrow',20)}</a><a class="btn btn-text-light" href="#{wf_id}">{t['hero_secondary']}{icon('arrow',18)}</a></div>
        <p class="hero-status"><span aria-hidden="true"></span>{t['hero_note']}</p>
      </div><div class="hero-art">{dashboard()}</div></div>
      <div class="shell hero-bottom"><span>{t['trust_intro']}</span><div class="trust-labels"><span>{icon('check',16)}{t['trust1']}</span><span>{icon('check',16)}{t['trust2']}</span><span>{icon('check',16)}{t['trust3']}</span></div></div>
    </section>
    <section class="section pain-section"><div class="shell"><div class="section-header section-header-split"><div><p class="eyebrow"><span class="eyebrow-line"></span>{t['pain_eyebrow']}</p><h2>{t['pain_title']}</h2></div><p>{t['pain_desc']}</p></div><div class="pain-grid">{pains}</div></div></section>
    <section class="section workflow-section" id="{wf_id}"><div class="shell workflow-layout"><div class="workflow-intro"><p class="eyebrow"><span class="eyebrow-line"></span>{t['workflow_eyebrow']}</p><h2>{t['workflow_title']}</h2><p>{t['workflow_desc']}</p><div class="workflow-art" aria-hidden="true"><div class="workflow-art-ring">{icon('file',58)}</div><span class="wa-line wa-one"></span><span class="wa-line wa-two"></span><span class="wa-node wa-node-a"></span><span class="wa-node wa-node-b"></span></div></div><div class="step-list">{steps}</div></div></section>
    <section class="section feature-section" id="{features_id}"><div class="shell"><div class="section-header centered"><p class="eyebrow"><span class="eyebrow-line"></span>{t['features_eyebrow']}</p><h2>{t['features_title']}</h2><p>{t['features_desc']}</p></div><div class="features-grid">{features}</div><p class="feature-notice">{icon('clock',16)}{t['feature_notice']}</p></div></section>
    <section class="section fit-section"><div class="shell fit-grid"><div class="fit-main"><p class="eyebrow"><span class="eyebrow-line"></span>{t['fit_eyebrow']}</p><h2>{t['fit_title']}</h2><p>{t['fit_desc']}</p><ul class="fit-bullets">{bullets}</ul></div><div class="fit-panel"><div class="fit-panel-pattern" aria-hidden="true"></div><span class="fit-mini">{t['fit_card_kicker']}</span><span class="fit-sign">✳</span><h3>{t['fit_card_title']}</h3><p>{t['fit_card_desc']}</p><div class="fit-divider"></div><div class="fit-benefits"><div>{icon('layers',20)}<span><strong>{t['fit_card1']}</strong><small>{t['fit_card1_desc']}</small></span></div><div>{icon('spark',20)}<span><strong>{t['fit_card2']}</strong><small>{t['fit_card2_desc']}</small></span></div></div></div></div></section>
    <section class="section roadmap-section"><div class="shell roadmap-layout"><div><p class="eyebrow"><span class="eyebrow-line"></span>{t['next_eyebrow']}</p><h2>{t['next_title']}</h2><p>{t['next_desc']}</p></div><div class="roadmap-list"><div><span class="roadmap-dot active"></span><b>{t['next1']}</b><p>{t['next1_desc']}</p></div><div><span class="roadmap-dot"></span><b>{t['next2']}</b><p>{t['next2_desc']}</p></div><div><span class="roadmap-dot"></span><b>{t['next3']}</b><p>{t['next3_desc']}</p></div></div></div></section>
    <section class="demo-section"><div class="shell">{demo_form(t)}</div></section>
    <section class="closing-section"><div class="shell closing-inner"><div><h2>{t['final_title']}</h2><p>{t['final_desc']}</p></div><a class="btn btn-secondary btn-large" href="#demo">{t['final_cta']}{icon('arrow',20)}</a></div></section>'''

ABOUT = {
'de':dict(kicker='DIE PERSON HINTER DEM PRODUKT',title='Nicht mehr Software.<br><em>Weniger Reibung.</em>',intro='ISPM15 Desk entsteht aus der Idee, dass digitale Werkzeuge vor allem eines tun sollten: einen konkreten Arbeitsablauf spürbar vereinfachen.',label='ÜBER MICH',bio_title='Hallo, ich bin',bio_placeholder='[Ihr Name]',bio_intro='Ich arbeite an einer fokussierten Lösung für die Verwaltung von ISPM-15-Nachweisen – mit dem Ziel, weniger Suchaufwand und mehr Übersicht in den Alltag von Holzverpackungsbetrieben zu bringen.',bio_role='Meine Rolle',bio_background='Mein beruflicher Hintergrund',bio_expertise='Meine fachliche Expertise',approach_label='WIE ICH ARBEITE',approach_title='Lieber ein Problem richtig lösen als zehn nur halb.',approach_desc='Die Projektkonzeption folgt drei einfachen Prinzipien:',principles=[('01','Erst zuhören','Vor neuen Funktionen steht die Frage, wie Betriebe heute tatsächlich arbeiten.'),('02','Einfach beginnen','Die erste Version konzentriert sich auf Lieferanten, Lieferungen, Dokumente und eine exportierbare Nachweisakte.'),('03','Sinnvoll ausbauen','Erinnerungen, PDF-Assistenz und weitere Funktionen folgen nur bei nachgewiesenem Bedarf.')],cta_title='Lassen Sie uns über Ihren Prozess sprechen.',cta_desc='Sie führen einen Holzverpackungs- oder Palettenbetrieb? Ich freue mich über einen Austausch zu Ihrem Dokumentationsalltag.',cta='Pilot-Demo anfragen',required_note='Persönliche Angaben sind in den Quellen nicht enthalten und müssen vor Veröffentlichung ergänzt werden.'),
'en':dict(kicker='THE PERSON BEHIND THE PROJECT',title='Not more software.<br><em>Less friction.</em>',intro='ISPM15 Desk is built around a simple belief: useful software should make one real-world workflow meaningfully easier.',label='ABOUT ME',bio_title='Hello, I’m',bio_placeholder='[Your name]',bio_intro='I’m developing a focused way to organize ISPM 15 documentation — helping wood packaging businesses spend less time looking for records and more time on their work.',bio_role='My role',bio_background='My professional background',bio_expertise='My expertise',approach_label='HOW I WORK',approach_title='Better to solve one problem well than ten halfway.',approach_desc='This project is guided by three practical principles:',principles=[('01','Listen first','Understand the workflows people actually use before deciding what to build.'),('02','Start simple','Focus the first release on suppliers, shipments, documents and exportable records.'),('03','Grow with proof','Add reminders, PDF assistance and new features only when real demand supports them.')],cta_title='Let’s talk about your workflow.',cta_desc='Run a wood packaging or pallet business? I’d love to learn about your documentation process.',cta='Request a pilot demo',required_note='Personal background details are not provided by the source documents and must be completed before publication.')}

def about_page():
    t=ABOUT[LANG]; p=paths('about')
    placeholder_name=esc(CFG['owner_name']) if CFG.get('owner_name') else f'<span class="not-set">{t["bio_placeholder"]}</span>'
    roles=field('about_role_'+LANG, '[Ihre Rolle im Projekt]', '[Your role in the project]')
    bg=field('about_background_'+LANG,'[Berufliche Stationen und Erfahrungen ergänzen]','[Add your professional background and experience]')
    expert=field('about_expertise_'+LANG,'[Kompetenzen, Qualifikationen und Schwerpunkte ergänzen]','[Add skills, qualifications and areas of expertise]')
    principles=''.join(f'<article><span>{num}</span><div><h3>{title}</h3><p>{desc}</p></div></article>' for num,title,desc in t['principles'])
    about_complete = all(str(CFG.get(k, '')).strip() for k in ['owner_name','about_role_de','about_role_en','about_background_de','about_background_en','about_expertise_de','about_expertise_en'])
    bio_note = '' if about_complete else f'<p class="bio-note">{icon("file",15)}{t["required_note"]}</p>'
    return f'''<section class="inner-hero"><div class="shell inner-hero-grid"><div><p class="eyebrow eyebrow-light"><span class="eyebrow-line"></span>{t['kicker']}</p><h1>{t['title']}</h1><p>{t['intro']}</p></div><div class="inner-hero-visual" aria-hidden="true"><div class="rings-logo"><div class="rings-small">15</div></div></div></div></section>
    <section class="section biography-section"><div class="shell biography-grid"><div class="bio-portrait" aria-hidden="true"><div class="portrait-mark">I<span>S</span></div><div class="portrait-grid"></div></div><div class="bio-content"><p class="eyebrow"><span class="eyebrow-line"></span>{t['label']}</p><h2>{t['bio_title']}<br>{placeholder_name}<span class="period">.</span></h2><p class="bio-intro">{t['bio_intro']}</p><dl class="bio-facts"><div><dt>{t['bio_role']}</dt><dd>{roles}</dd></div><div><dt>{t['bio_background']}</dt><dd>{bg}</dd></div><div><dt>{t['bio_expertise']}</dt><dd>{expert}</dd></div></dl>{bio_note}</div></div></section>
    <section class="section approach-section"><div class="shell"><div class="section-header centered"><p class="eyebrow"><span class="eyebrow-line"></span>{t['approach_label']}</p><h2>{t['approach_title']}</h2><p>{t['approach_desc']}</p></div><div class="approach-grid">{principles}</div></div></section>
    <section class="about-cta"><div class="shell about-cta-inner"><div><h2>{t['cta_title']}</h2><p>{t['cta_desc']}</p></div><a class="btn btn-primary btn-large" href="{p['home']}#demo">{t['cta']}{icon('arrow',18)}</a></div></section>'''

LEGAL = {
'de':dict(kicker='RECHTLICHES',title='Impressum',intro='Angaben gemäß § 5 Digitale-Dienste-Gesetz (DDG).',warning='Wichtig: Rechtliche Pflichtangaben fehlen noch. Bitte diese Seite vor Veröffentlichung vollständig mit Ihren eigenen Daten ergänzen und prüfen lassen.',operator='Anbieter',contact='Kontakt',email='E-Mail',phone='Telefon',represented='Vertretungsberechtigt',register='Registerangaben, soweit zutreffend',register_court='Registergericht',register_number='Registernummer',vat='Umsatzsteuer-Identifikationsnummer, soweit vorhanden',editorial='Hinweis',editorial_text='ISPM15 Desk ist ein unabhängiges Softwareprojekt und keine behördliche oder amtliche Zertifizierungsstelle.'),
'en':dict(kicker='LEGAL INFORMATION',title='Legal notice',intro='Provider information pursuant to Section 5 of the German Digital Services Act (DDG).',warning='Important: Required provider details are still missing. Complete and review this page with your own information before going live.',operator='Service provider',contact='Contact',email='Email',phone='Phone',represented='Legal representative',register='Commercial register details, if applicable',register_court='Register court',register_number='Registration number',vat='VAT ID, if applicable',editorial='Notice',editorial_text='ISPM15 Desk is an independent software project and not an official government or certification body.')}

def legal_page():
    t=LEGAL[LANG]
    required = ['owner_name','street_address','postal_code','city','contact_email','phone']
    complete = all(str(CFG.get(k,'')).strip() for k in required)
    alert = '' if complete else f'<div class="legal-alert">{icon("clock",22)}<p>{t["warning"]}</p></div>'
    legal_form = f'<br>{esc(CFG["legal_form"])}' if CFG.get('legal_form') else ''
    owner_section = f'<section><h2>{t["operator"]}</h2><p>{legal_owner()}{legal_form}<br>{field("street_address","[Straße und Hausnummer]","[Street and number]")}<br>{field("postal_code","[Postleitzahl]","[Postal code]")} {field("city","[Ort]","[City]")}<br>{esc(CFG.get("country") or "Deutschland")}</p></section>'
    contact_section = f'<section><h2>{t["contact"]}</h2><p>{t["email"]}: {field("contact_email","[Geschäftliche E-Mail-Adresse]","[Business email]")}<br>{t["phone"]}: {field("phone","[Telefonnummer]","[Phone number]")}</p></section>'
    representative = f'<section><h2>{t["represented"]}</h2><p>{esc(CFG["representative"])}</p></section>' if CFG.get('representative') else ''
    reg_fields = [('register_court','register_court'),('register_number','register_number'),('vat_id','vat')]
    entries=[f'{t[label]}: {esc(CFG[key])}' for key,label in reg_fields if CFG.get(key)]
    registered = f'<section><h2>{t["register"]}</h2><p>{"<br>".join(entries)}</p></section>' if entries else ''
    note = f'<section><h2>{t["editorial"]}</h2><p>{t["editorial_text"]}</p></section>'
    return f'''<section class="legal-hero"><div class="shell legal-hero-content"><p class="eyebrow eyebrow-light"><span class="eyebrow-line"></span>{t['kicker']}</p><h1>{t['title']}</h1><p>{t['intro']}</p></div></section>
    <div class="shell legal-body">{alert}{owner_section}{contact_section}{representative}{registered}{note}</div>'''

PRIVACY = {
'de':dict(kicker='DATENSCHUTZ',title='Datenschutzerklärung',intro='Transparente Informationen zur Verarbeitung personenbezogener Daten beim Besuch dieser Website und bei Demoanfragen.',alert='Vor Veröffentlichung mit den tatsächlichen Betreiberangaben, Dienstleisterverträgen und Löschfristen abgleichen. Dies ist ein anpassbarer Entwurf, keine anwaltliche Prüfung.',
sections=[
('1. Verantwortlicher','Für die Datenverarbeitung verantwortlich ist:'),
('2. Hosting über GitHub Pages','Diese Website wird als statische Website über GitHub Pages bereitgestellt (GitHub, Inc.). Beim Abruf der Website können technisch notwendige Verbindungsdaten, etwa IP-Adresse, Zeitpunkt, angeforderte Dateien und Browserinformationen, durch den Hostinganbieter verarbeitet werden. Zweck ist die sichere und zuverlässige Bereitstellung der Website. Soweit wir hierfür verantwortlich sind, stützen wir uns auf Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an einem sicheren Webauftritt). Weitere Informationen zur Verarbeitung durch GitHub ergeben sich aus den Datenschutzhinweisen von GitHub.'),
('3. Demoanfragen und Formspree','Wenn Sie eine Demo anfragen, verarbeiten wir die von Ihnen angegebenen Daten (Unternehmen, Name, geschäftliche E-Mail-Adresse und freiwillige Angaben), um die Anfrage zu bearbeiten, Rückfragen zu stellen und eine mögliche Zusammenarbeit vorzubereiten. Rechtsgrundlage ist grundsätzlich Art. 6 Abs. 1 lit. b DSGVO für vorvertragliche Maßnahmen. Für den Empfang wird nach Aktivierung des Formulars Formspree eingesetzt. Dabei werden die übermittelten Formulardaten an den Formularanbieter übertragen und dort verarbeitet. Beim Einsatz dieses Dienstes sind die erforderlichen Vereinbarungen zur Auftragsverarbeitung und gegebenenfalls Schutzmaßnahmen für internationale Datenübermittlungen relevant. Es findet keine werbliche Newsletter-Anmeldung durch dieses Formular statt.'),
('4. Speicherdauer','Wir speichern Anfragedaten nur so lange, wie dies für die Bearbeitung und gegebenenfalls die Anbahnung einer Geschäftsbeziehung erforderlich ist, oder soweit gesetzliche Aufbewahrungspflichten greifen. Die für diesen Betrieb festgelegte Speicherdauer ist nachfolgend angegeben.'),
('5. Cookies, Schriften und Analyse','Diese Website bindet keine externen Schriftbibliotheken, Marketing-Tracker oder Analyse-Tools ein und setzt selbst keine Tracking-Cookies. Bei Änderungen, etwa dem Einsatz weiterer Dienste, ist diese Erklärung entsprechend anzupassen.'),
('6. Ihre Rechte','Sie haben im gesetzlichen Rahmen Rechte auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung und Datenübertragbarkeit sowie gegebenenfalls das Recht auf Widerspruch. Sie haben zudem das Recht, sich bei einer zuständigen Datenschutzaufsichtsbehörde zu beschweren. Für Datenschutzanfragen kontaktieren Sie die oben genannte verantwortliche Stelle.'),
('7. Datensicherheit','Die Website wird bei Veröffentlichung auf GitHub Pages über HTTPS ausgeliefert. Formularübermittlungen erfolgen bei aktiviertem Dienst über eine HTTPS-Verbindung. Auch bei technisch sorgfältiger Umsetzung lässt sich ein Restrisiko bei Datenübertragungen nicht vollständig ausschließen.')]),
'en':dict(kicker='DATA PROTECTION',title='Privacy policy',intro='How personal data is handled when you visit this website or request a demo.',alert='Before publication, verify the actual provider details, processor contracts and retention periods. This is a customizable draft, not a legal review.',
sections=[
('1. Data controller','The controller responsible for personal data processing is:'),
('2. Hosting on GitHub Pages','This static website is hosted using GitHub Pages (GitHub, Inc.). When visitors access it, the hosting provider may process technical connection data such as IP addresses, request times, requested files and browser information. This supports reliable and secure website delivery. Where we are the responsible controller, processing is based on Article 6(1)(f) GDPR (legitimate interest in a secure online presence). See GitHub’s privacy information for more details.'),
('3. Demo requests and Formspree','When you request a demo, we use the information you provide (company, name, work email and any optional details) to handle your enquiry and potentially prepare a business relationship. Our main legal basis is Article 6(1)(b) GDPR (pre-contractual steps). Once configured, the form uses Formspree, which receives and processes the submitted information. Use of this provider is subject to relevant data-processing arrangements and, where applicable, safeguards for international data transfers. Submitting this form does not subscribe you to marketing emails.'),
('4. Retention period','We retain enquiry information only for as long as needed to respond and potentially establish a business relationship, or where legal retention obligations apply. The retention period for this website is stated below.'),
('5. Cookies, fonts and analytics','This website includes no externally hosted fonts, marketing trackers or analytics tools, and does not itself use tracking cookies. If services are added later, this policy must be updated.'),
('6. Your data protection rights','Subject to applicable law, you may request access, rectification, erasure, restriction of processing and data portability, and may have the right to object. You may also lodge a complaint with an appropriate supervisory authority. Please use the controller contact details above for privacy-related enquiries.'),
('7. Security','When published on GitHub Pages, this website is delivered over HTTPS. If activated, the form service receives submissions over HTTPS. No internet transmission can be guaranteed to be entirely risk-free.')])}

def privacy_page():
    t=PRIVACY[LANG]
    ctrl=f'<p>{legal_owner()}<br>{field("street_address", "[Straße und Hausnummer]", "[Street and number]")}<br>{field("postal_code", "[PLZ]", "[Postal code]")} {field("city", "[Ort]", "[City]")}<br>{field("contact_email", "[E-Mail-Adresse]", "[Email]")}</p>'
    github = '<p><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener noreferrer">GitHub Privacy Statement ↗</a></p>'
    formspree = '<p><a href="https://formspree.io/legal/privacy-policy" target="_blank" rel="noopener noreferrer">Formspree Privacy Policy ↗</a></p>'
    sections=[]
    for i,(title,desc) in enumerate(t['sections']):
        append=(ctrl if i==0 else github if i==1 else formspree if i==2 else f'<p>{field("privacy_retention_"+LANG,"[Konkrete Löschfrist ergänzen]","[Add your retention period]")}</p>' if i==3 else '')
        sections.append(f'<section><h2>{title}</h2><p>{desc}</p>{append}</section>')
    core_fields = ['owner_name','street_address','postal_code','city','contact_email','privacy_retention_de','privacy_retention_en']
    privacy_complete = all(str(CFG.get(k,'')).strip() for k in core_fields) and bool(CFG.get('formspree_endpoint'))
    alert = '' if privacy_complete else f'<div class="legal-alert">{icon("clock",22)}<p>{t["alert"]}</p></div>'
    return f'''<section class="legal-hero"><div class="shell legal-hero-content"><p class="eyebrow eyebrow-light"><span class="eyebrow-line"></span>{t['kicker']}</p><h1>{t['title']}</h1><p>{t['intro']}</p></div></section><div class="shell legal-body">{alert}{''.join(sections)}</div>'''

for LANG in ('de', 'en'):
    folder = ROOT if LANG == 'de' else ROOT / 'en'
    mapping = {'home': 'index.html', 'about': 'about.html', 'legal': 'impressum.html' if LANG == 'de' else 'legal.html', 'privacy':'datenschutz.html' if LANG=='de' else 'privacy.html'}
    generators={'home':landing,'about':about_page,'legal':legal_page,'privacy':privacy_page}
    for page, filename in mapping.items():
        (folder / filename).write_text(wrap(page,generators[page]()), encoding='utf-8')
        print(f'generated: {folder.name}/{filename}')
