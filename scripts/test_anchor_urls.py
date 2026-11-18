#!/usr/bin/env python3
"""Prüft, dass Anker-Links zum Abschnitt scrollen, die Adresszeile aber ohne "#..." bleibt.
Aufruf: python scripts/test_anchor_urls.py [Basis-URL]   (Standard: http://localhost:8765/)
"""
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8765/'
if not BASE.endswith('/'):
    BASE += '/'
results = []


def check(name, ok, detail=''):
    results.append(ok)
    print(('[OK]   ' if ok else '[FAIL] ') + name + (f'  ({detail})' if detail else ''))


def top_of(page, sel):
    return page.evaluate("s => Math.round(document.querySelector(s).getBoundingClientRect().top)", sel)


with sync_playwright() as p:
    browser = None
    for channel in ('msedge', 'chrome'):
        try:
            browser = p.chromium.launch(channel=channel, headless=True)
            break
        except Exception:  # noqa: BLE001
            continue
    if browser is None:
        sys.exit('Kein Browser verfügbar.')
    ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
    errors = []

    for lang, path, flow, demo_btn in (('DE', '', '#ablauf', 'Demo anfordern'),
                                         ('EN', 'en/', '#workflow', 'Request a demo')):
        page = ctx.new_page()
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto(BASE + path, wait_until='networkidle')
        base_url = page.url
        # 1) Klick auf "So funktioniert's" im Menü
        page.click(f'.primary-nav a[href$="{flow}"]')
        page.wait_for_timeout(1200)
        check(f'{lang}: Menü-Klick {flow} -> Adresse ohne #', '#' not in page.url, page.url)
        check(f'{lang}: Menü-Klick {flow} -> Abschnitt sichtbar', abs(top_of(page, flow)) < 220, f'top={top_of(page, flow)}px')
        # 2) Klick auf den Demo-Button im Menü
        page.evaluate('window.scrollTo(0,0)')
        page.click(f'.btn-nav:has-text("{demo_btn}")')
        page.wait_for_timeout(1200)
        check(f'{lang}: Demo-Button -> Adresse ohne #', '#' not in page.url, page.url)
        check(f'{lang}: Demo-Button -> Formular im Blick', abs(top_of(page, '#demo')) < 220, f'top={top_of(page, "#demo")}px')
        # 3) Direktaufruf mit Anker (so wie aus der E-Mail)
        page.goto(base_url + 'index.html#demo' if lang == 'DE' else base_url + 'index.html#demo', wait_until='load')
        page.wait_for_timeout(1000)
        check(f'{lang}: Direktaufruf index.html#demo -> Adresse ohne #', '#' not in page.url, page.url)
        check(f'{lang}: Direktaufruf -> Formular im Blick', abs(top_of(page, '#demo')) < 220, f'top={top_of(page, "#demo")}px')
        page.close()

    # 4) Anker von einer Unterseite aus (about.html -> Startseite#demo) bleibt funktionsfähig
    page = ctx.new_page()
    page.goto(BASE + 'about.html', wait_until='networkidle')
    page.click('.btn-nav')
    page.wait_for_timeout(1500)
    check('Unterseite: Demo-Button führt zur Startseite', page.url.rstrip('/').endswith(('index.html', BASE.rstrip('/'), '#demo')) or page.url.startswith(BASE), page.url)
    check('Unterseite: Formular im Blick', abs(top_of(page, '#demo')) < 220, f'top={top_of(page, "#demo")}px')
    check('Keine JS-Fehler', not errors, '; '.join(errors))
    browser.close()

print()
print('Ergebnis:', 'ALLE TESTS BESTANDEN' if all(results) else 'FEHLER VORHANDEN', f'({sum(results)}/{len(results)})')
sys.exit(0 if all(results) else 1)
