import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})
        await page.goto('http://127.0.0.1:8878/he/', wait_until='networkidle')
        bad = await page.evaluate("""() => {
          const out = [];
          const sw = document.documentElement.scrollWidth;
          document.querySelectorAll('*').forEach(e => {
            const b = e.getBoundingClientRect();
            if (b.left < -5 || b.right > 1285) {
              out.push({tag: e.tagName, cls: (e.className||'').toString().slice(0,50), left: Math.round(b.left), right: Math.round(b.right)});
            }
          });
          return {els: out.slice(0,10), scrollW: sw, clientW: document.documentElement.clientWidth};
        }""")
        print(bad)
        await browser.close()

asyncio.run(main())
