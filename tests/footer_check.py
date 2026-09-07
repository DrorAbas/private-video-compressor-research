import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})
        await page.goto('http://127.0.0.1:8878/he/', wait_until='networkidle')
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(800)
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/he_footer.png')
        n = await page.locator('details').count()
        print('HE details (FAQ) count:', n)
        await page.goto('http://127.0.0.1:8878/', wait_until='networkidle')
        n2 = await page.locator('details').count()
        print('EN details count:', n2)
        await browser.close()

asyncio.run(main())
