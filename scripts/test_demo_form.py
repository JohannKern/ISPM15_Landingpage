#!/usr/bin/env python3
"""Browser-Test des Demo-Formulars (Live-Seite oder lokale Datei).

Standard: Die Formspree-Anfrage wird abgefangen und lokal beantwortet, es entsteht KEINE echte Anfrage.
Geprüft werden:
  1. Mehrfachklick bei langsamer Antwort -> genau 1 Anfrage, Button + Felder währenddessen gesperrt
  2. Erfolgsfall -> eindeutige Bestätigung sichtbar, Formular ausgeblendet, kein erneuter Versand möglich
  3. Fehlerfall -> Fehlermeldung, Button/Felder wieder aktiv, eingegebene Daten bleiben erhalten
Mit --real wird zusätzlich EINE echte Testanfrage an Formspree gesendet (erzeugt einen echten Eintrag!).

Benötigt: pip install playwright  (nutzt den installierten Microsoft Edge bzw. Chrome)
Aufruf:   python scripts/test_demo_form.py [URL] [--real]
"""
import sys
import time
from playwright.sync_api import sync_playwright

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
REAL = '--real' in sys.argv
URL = ARGS[0] if ARGS else 'https://johannkern.github.io/ISPM15_Landingpage/'
CORS = {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*'}
results = []


def check(name, ok, detail=''):
    results.append(ok)
    print(('[OK]   ' if ok else '[FAIL] ') + name + (f'  ({detail})' if detail else ''))


def launch(p):
    for channel in ('msedge', 'chrome'):
        try:
            return p.chromium.launch(channel=channel, headless=True)
        except Exception as exc:  # noqa: BLE001
            print(f'Browser {channel} nicht startbar: {str(exc)[:80]}')
    sys.exit('Kein Browser verfügbar.')


def fill(page):
    page.fill('#demo-company', 'TEST Cline - bitte ignorieren')
    page.fill('#demo-name', 'Technischer Test')
    page.fill('#demo-email', 'johann.kern1161@gmail.com')


def new_page(browser, handler=None):
    ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    if handler:
        ctx.route('**/formspree.io/**', handler)
    page.goto(URL, wait_until='networkidle')
    return ctx, page, errors


def make_handler(posts, status, delay=0.0):
    def handler(route):
        if route.request.method == 'OPTIONS':
            route.fulfill(status=204, headers=CORS)
            return
        posts.append(1)
        time.sleep(delay)
        route.fulfill(status=status, content_type='application/json', headers=CORS,
                      body='{"ok":true}' if status == 200 else '{"ok":false}')
    return handler


with sync_playwright() as p:
    browser = launch(p)

    # --- 1 + 2: langsame Erfolgsantwort, mehrfache Auslösung ---------------------------------------
    posts = []
    ctx, page, errors = new_page(browser, make_handler(posts, 200, delay=1.5))
    fill(page)
    page.click('[data-submit-button]')
    page.wait_for_timeout(300)
    btn_text = page.inner_text('[data-submit-button]').strip()
    check('Button während des Versands gesperrt', page.is_disabled('[data-submit-button]'))
    check('Button zeigt Versandstatus', btn_text.lower().startswith(('wird gesendet', 'sending')), btn_text)
    check('Felder während des Versands gesperrt', page.is_disabled('#demo-email'))
    page.evaluate("document.querySelector('[data-submit-button]').click()")
    page.evaluate("document.querySelector('[data-demo-form]').requestSubmit()")
    page.wait_for_timeout(2500)
    success_text = page.inner_text('[data-form-success]').strip().replace('\n', ' | ')
    check('Bestätigung sichtbar', page.is_visible('[data-form-success]'), success_text)
    check('Formular nach Erfolg ausgeblendet', not page.is_visible('[data-demo-form]'))
    page.evaluate("document.querySelector('[data-demo-form]').requestSubmit()")
    page.wait_for_timeout(800)
    check('Genau 1 Anfrage trotz mehrfacher Auslösung', len(posts) == 1, f'{len(posts)} Anfrage(n)')
    check('Keine JS-Fehler (Erfolgsfall)', not errors, '; '.join(errors))
    page.screenshot(path='test_demo_form_success.png')
    ctx.close()

    # --- 3: Fehlerfall -------------------------------------------------------------------------------
    err_posts = []
    ctx, page, errors = new_page(browser, make_handler(err_posts, 500))
    fill(page)
    page.click('[data-submit-button]')
    page.wait_for_timeout(1200)
    err_msg = page.inner_text('[data-form-status]').strip()
    state = page.get_attribute('[data-form-status]', 'data-state')
    check('Fehlermeldung sichtbar', bool(err_msg) and state == 'error', err_msg)
    check('Button nach Fehler wieder aktiv', not page.is_disabled('[data-submit-button]'))
    check('Felder nach Fehler wieder aktiv', not page.is_disabled('#demo-email'))
    check('Eingaben nach Fehler erhalten', page.input_value('#demo-email') == 'johann.kern1161@gmail.com')
    check('Keine Erfolgsmeldung im Fehlerfall', not page.is_visible('[data-form-success]'))
    ctx.close()

    # --- optional: eine echte Anfrage ----------------------------------------------------------------
    if REAL:
        real = []
        ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = ctx.new_page()
        page.on('response', lambda r: real.append((r.status, r.text()[:120]))
                if 'formspree.io' in r.url and r.request.method == 'POST' else None)
        page.goto(URL, wait_until='networkidle')
        fill(page)
        page.click('[data-submit-button]')
        page.wait_for_timeout(4000)
        check('ECHTE Anfrage: Bestätigung sichtbar', page.is_visible('[data-form-success]'), str(real))
        ctx.close()

    browser.close()

print()
print('Ergebnis:', 'ALLE TESTS BESTANDEN' if all(results) else 'FEHLER VORHANDEN', f'({sum(results)}/{len(results)})')
sys.exit(0 if all(results) else 1)
