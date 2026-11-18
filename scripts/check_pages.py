#!/usr/bin/env python3
"""Prüft alle Seiten im Browser: lädt fehlerfrei, keine JS-Fehler, keine toten internen Links/Anker.
Aufruf: python scripts/check_pages.py [Basis-URL]   (Standard: http://localhost:8765/)
Benötigt: pip install playwright (nutzt installierten Microsoft Edge bzw. Chrome)
"""
import sys
from urllib.parse import urljoin, urldefrag
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8765/'
PAGES = ['', 'about.html', 'impressum.html', 'datenschutz.html',
         'en/', 'en/about.html', 'en/legal.html', 'en/privacy.html']
bad = 0

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
    for path in PAGES:
        url = urljoin(BASE, path)
        page = ctx.new_page()
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        resp = page.goto(url, wait_until='networkidle')
        problems = []
        if resp is None or resp.status != 200:
            problems.append(f'HTTP {resp.status if resp else "?"}')
        problems += [f'JS-Fehler: {e}' for e in errors]
        hrefs = page.eval_on_selector_all('a[href]', 'els => els.map(e => e.getAttribute("href"))')
        for href in sorted(set(hrefs)):
            if href.startswith(('mailto:', 'tel:', 'http://', 'https://')):
                continue
            target, frag = urldefrag(urljoin(url, href))
            if frag and target == url and page.locator(f'[id="{frag}"]').count() == 0:
                problems.append(f'toter Anker #{frag}')
            elif target != url:
                r = ctx.request.get(target)
                if r.status != 200:
                    problems.append(f'toter Link {href} -> {r.status}')
                elif frag:
                    html = r.text()
                    if f'id="{frag}"' not in html:
                        problems.append(f'toter Anker {href}')
        mark = 'OK  ' if not problems else 'FAIL'
        bad += bool(problems)
        print(f'[{mark}] {path or "(Startseite)"}' + ('' if not problems else '  ' + '; '.join(problems)))
        page.close()
    browser.close()

print('Ergebnis:', 'ALLE SEITEN OK' if not bad else f'{bad} Seite(n) mit Problemen')
sys.exit(1 if bad else 0)
