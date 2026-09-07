import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))

        # --- EN light ---
        await page.goto('http://127.0.0.1:8878/', wait_until='networkidle')
        await page.evaluate("localStorage.removeItem('pvc-theme')")
        await page.reload(wait_until='networkidle')
        await page.wait_for_timeout(500)
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/brand_en_light.png')
        print('EN theme:', await page.get_attribute('html', 'data-theme'))

        # --- EN dark (click toggle) ---
        await page.click('.theme-toggle')
        await page.wait_for_timeout(400)
        print('EN theme after toggle:', await page.get_attribute('html', 'data-theme'))
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/brand_en_dark.png')

        # persistence check
        await page.reload(wait_until='networkidle')
        print('EN theme after reload (persisted):', await page.get_attribute('html', 'data-theme'))

        # --- HE dark ---
        await page.goto('http://127.0.0.1:8878/he/', wait_until='networkidle')
        await page.evaluate("localStorage.setItem('pvc-theme','dark')")
        await page.reload(wait_until='networkidle')
        await page.wait_for_timeout(400)
        print('HE theme:', await page.get_attribute('html', 'data-theme'))
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/brand_he_dark.png')

        # --- HE light ---
        await page.click('.theme-toggle')
        await page.wait_for_timeout(400)
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/brand_he_light.png')

        # compression still works in dark mode
        await page.set_input_files('#fileInput', '/opt/data/projects/private-video-compressor-research/tests/out_20mb_sim.mp4')
        await page.wait_for_timeout(1200)
        await page.click('.chip[data-preset="custom"]')
        await page.locator('#customRange').evaluate("el => { el.value = 2; el.dispatchEvent(new Event('input', {bubbles:true})); }")
        await page.click('#compressBtn')
        await page.wait_for_selector('#result:not([hidden])', timeout=300000)
        print('HE dark compression:', await page.text_content('#resultSummary'))
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/brand_he_dark_result.png')

        print('JS errors:', errors if errors else 'none')
        await browser.close()

asyncio.run(main())
