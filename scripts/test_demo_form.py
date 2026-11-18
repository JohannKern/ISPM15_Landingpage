#!/usr/bin/env python3
"""Browser-Test des Demo-Formulars (Live-Seite oder lokale Datei).

Die Formspree-Anfrage wird abgefangen und lokal beantwortet, es entsteht also keine echte Anfrage.
Benötigt: pip install playwright  (nutzt den installierten Microsoft Edge bzw. Chrome)
Aufruf:   python scripts/test_demo_form.py [URL]
"""
import sys
from playwright.sync_api import sync_playwright

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
REAL = '--real' in sys.argv  # echte Anfrage an Formspree senden (erzeugt einen echten Eintrag!)
URL = ARGS[0] if ARGS else 'https://johannkern.github.io/ISPM15_Landingpage/'
captured = []
responses = []
console_errors = []


def handle(route):
    captured.append({'method': route.request.method, 'url': route.request.url,
                     'accept': route.request.headers.get('accept', '')})
    route.fulfill(status=200, content_type='application/json',
                  headers={'Access-Control-Allow-Origin': '*'}, body='{"ok":true}')


with sync_playwright() as p:
    browser = None
    for channel in ('msedge', 'chrome'):
        try:
            browser = p.chromium.launch(channel=channel, headless=True)
            break
        except Exception as exc:  # noqa: BLE001
            print(f'Browser {channel} nicht startbar: {str(exc)[:80]}')
    if browser is None:
        sys.exit('Kein Browser verfügbar.')
    ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
    page = ctx.new_page()
    page.on('console', lambda m: console_errors.append(m.text) if m.type == 'error' else None)
    page.on('pageerror', lambda e: console_errors.append('PAGEERROR: ' + str(e)))
    if REAL:
        page.on('response', lambda r: responses.append((r.status, r.url, r.text()[:300]))
                if 'formspree.io' in r.url and r.request.method == 'POST' else None)
    else:
        ctx.route('**/formspree.io/**', handle)
    page.goto(URL, wait_until='networkidle')
    page.fill('#demo-company', 'TEST Cline - bitte ignorieren')
    page.fill('#demo-name', 'Technischer Test')
    page.fill('#demo-email', 'johann.kern1161@gmail.com')
    page.click('[data-submit-button]')
    page.wait_for_timeout(2500)
    status = page.inner_text('[data-form-status]').strip()
    state = page.get_attribute('[data-form-status]', 'data-state')
    print('Statusmeldung   :', repr(status))
    print('Status-Zustand  :', state)
    print('Abgefangene POSTs:', captured)
    print('Echte Antworten  :', responses)
    print('JS-Konsolenfehler:', console_errors or 'keine')
    browser.close()
