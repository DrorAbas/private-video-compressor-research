import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})

        # Final screenshots: EN light, EN dark, HE light, HE dark (full page for HE)
        await page.goto('http://127.0.0.1:8878/', wait_until='networkidle')
        await page.evaluate("localStorage.setItem('pvc-theme','light')")
        await page.reload(wait_until='networkidle')
        await page.wait_for_timeout(400)
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/final_en_light.png')

        await page.evaluate("localStorage.setItem('pvc-theme','dark')")
        await page.reload(wait_until='networkidle')
        await page.wait_for_timeout(400)
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/final_en_dark.png', full_page=True)

        await page.goto('http://127.0.0.1:8878/he/', wait_until='networkidle')
        await page.evaluate("localStorage.setItem('pvc-theme','light')")
        await page.reload(wait_until='networkidle')
        await page.wait_for_timeout(400)
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/final_he_light.png')

        await page.evaluate("localStorage.setItem('pvc-theme','dark')")
        await page.reload(wait_until='networkidle')
        await page.wait_for_timeout(400)
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/final_he_dark.png')

        print('shots done')
        await browser.close()

asyncio.run(main())
