#!/usr/bin/env python3
"""Local visual smoke tests; test helper, not required for static hosting."""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent
PAGES=['index.html','about.html','impressum.html','datenschutz.html','en/index.html','en/about.html','en/legal.html','en/privacy.html']
VIEWS={'desktop':(1440,900),'tablet':(820,1180),'mobile':(390,844)}

async def main():
  results=[]
  async with async_playwright() as pw:
    browser=await pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox','--disable-dev-shm-usage'])
    for viewport,(width,height) in VIEWS.items():
      for page_path in PAGES:
        page=await browser.new_page(viewport={'width':width,'height':height}, device_scale_factor=1)
        problems=[]
        page.on('pageerror', lambda e: problems.append(str(e)))
        markup=(ROOT/page_path).read_text(encoding='utf-8')
        markup=markup.replace('<link rel="stylesheet" href="assets/css/style.css">','<style>'+ (ROOT/'assets/css/style.css').read_text(encoding='utf-8')+'</style>')
        markup=markup.replace('<link rel="stylesheet" href="../assets/css/style.css">','<style>'+ (ROOT/'assets/css/style.css').read_text(encoding='utf-8')+'</style>')
        markup=markup.replace('<link rel="stylesheet" href="assets/css/dark-theme.css">','<style>'+ (ROOT/'assets/css/dark-theme.css').read_text(encoding='utf-8')+'</style>')
        markup=markup.replace('<link rel="stylesheet" href="../assets/css/dark-theme.css">','<style>'+ (ROOT/'assets/css/dark-theme.css').read_text(encoding='utf-8')+'</style>')
        markup=markup.replace('<script src="assets/js/site.js" defer></script>','').replace('<script src="../assets/js/site.js" defer></script>','')
        markup=markup.replace('</body>', '<script>'+(ROOT/'assets/js/site.js').read_text(encoding='utf-8')+'</script></body>')
        await page.set_content(markup, wait_until='load')
        await page.wait_for_timeout(160)
        state=await page.evaluate('''() => ({
          title:document.title,
          pageWidth:document.documentElement.scrollWidth,
          viewportWidth:innerWidth,
          lang:document.documentElement.lang,
          hasDarkStyle:Array.from(document.styleSheets).length>=2,
          bodyBackground:getComputedStyle(document.body).backgroundColor,
          cards:document.querySelectorAll('.feature-card,.pain-card').length,
          form:Boolean(document.querySelector('[data-demo-form]')),
          nav:Boolean(document.querySelector('#primary-nav')),
        })''')
        if state['pageWidth']>width+2: problems.append(f'horizontal overflow: {state["pageWidth"]}>{width}')
        if not state['hasDarkStyle']: problems.append('dark css missing')
        if page_path.startswith('en/') != (state['lang']=='en'): problems.append('incorrect lang attr')
        if viewport=='mobile' and page_path in ('index.html','en/index.html','about.html'):
          await page.locator('.menu-toggle').click()
          if await page.locator('#primary-nav').evaluate('(n)=>!n.classList.contains("is-open")'):
            problems.append('mobile menu not opened')
          await page.locator('.menu-toggle').click()
        if page_path in ('index.html','en/index.html') and viewport=='desktop':
          await page.locator('.hero').screenshot(path=str(OUT/f'ispm15-dark-hero-{page_path.replace("/","-")}.png'))
        if viewport=='desktop' and page_path=='index.html':
          await page.screenshot(path=str(OUT/'ispm15-dark-desktop.png'), full_page=True)
        if viewport=='tablet' and page_path=='index.html':
          await page.screenshot(path=str(OUT/'ispm15-dark-tablet.png'), full_page=True)
        if viewport=='mobile' and page_path=='index.html':
          await page.screenshot(path=str(OUT/'ispm15-dark-mobile.png'), full_page=True)
        if viewport=='mobile' and page_path=='about.html':
          await page.screenshot(path=str(OUT/'ispm15-dark-about-mobile.png'),full_page=True)
        if page_path=='index.html' and viewport=='desktop':
          await page.locator('#demo-company').fill('Test Firma')
          await page.locator('#demo-name').fill('Jane Example')
          await page.locator('#demo-email').fill('example@example.com')
          await page.locator('[data-submit-button]').click()
          status=await page.locator('[data-form-status]').inner_text()
          if 'noch nicht freigeschaltet' not in status: problems.append('unconfigured form not handled')
        results.append({'viewport':viewport,'page':page_path,'ok':not problems,'problems':problems,'details':state})
        await page.close()
    await browser.close()
  (OUT/'ispm15-dark-test-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
  for r in results:
    print(f"{'PASS' if r['ok'] else 'FAIL'} {r['viewport']:8} {r['page']:24} W:{r['details']['pageWidth']} Problems: {', '.join(r['problems'])}")
  if not all(r['ok'] for r in results): raise SystemExit(1)

if __name__=='__main__': asyncio.run(main())
