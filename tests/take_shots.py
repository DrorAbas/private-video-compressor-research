import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})

        # EN top (full hero + tool)
        await page.goto('http://127.0.0.1:8878/', wait_until='networkidle')
        await page.wait_for_timeout(600)
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/shot_en_hero.png')

        # HE top
        await page.goto('http://127.0.0.1:8878/he/', wait_until='networkidle')
        await page.wait_for_timeout(600)
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/shot_he_hero.png')

        # HE with file loaded + presets
        await page.set_input_files('#fileInput', '/opt/data/projects/private-video-compressor-research/tests/test_small.mp4')
        await page.wait_for_timeout(1200)
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/shot_he_loaded.png')

        await browser.close()
        print('done')

asyncio.run(main())
