import asyncio
import sys
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)

        # ---- EN page ----
        await page.goto('http://127.0.0.1:8878/', wait_until='networkidle')
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/en_top.png')
        title = await page.title()
        print('EN title:', title)

        # check dropzone & preset chips
        assert await page.is_visible('#dropzone'), 'dropzone missing'
        chips = await page.locator('.chip').count()
        print('EN preset chips:', chips)
        assert chips == 8, 'expected 8 chips'

        # crosslink/related tools removed: crosslink div may exist but should not show cards; we removed it entirely
        cl = await page.locator('#crosslink').count()
        print('crosslink elements (should be 0):', cl)

        # upload test video via file input
        await page.set_input_files('#fileInput', '/opt/data/projects/private-video-compressor-research/tests/test_small.mp4')
        await page.wait_for_timeout(1500)
        controls_visible = await page.is_visible('#controls')
        print('Controls visible after upload:', controls_visible)
        assert controls_visible

        # trim fieldset visible?
        trim_visible = await page.is_visible('#trimWrap')
        print('Trim visible:', trim_visible)

        # custom slider appears on Custom click (controls now visible)
        await page.click('.chip[data-preset="custom"]')
        assert await page.is_visible('#customWrap'), 'customWrap not shown'
        print('Custom slider OK')

        # screenshot with file loaded
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/en_loaded.png')

        # click Discord preset then Compress, wait for result (ffmpeg.wasm loads from CDN)
        await page.click('.chip[data-preset="discord8"]')
        await page.click('#compressBtn')
        print('Compression started, waiting...')
        try:
            await page.wait_for_selector('#result:not([hidden])', timeout=180000)
            summary = await page.text_content('#resultSummary')
            print('RESULT SUMMARY:', summary)
            await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/en_result.png')
        except Exception as e:
            print('Compression did not complete in time:', e)
            phase = await page.text_content('#phase')
            print('phase:', phase)
            await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/en_compressing.png')

        # ---- HE page ----
        await page.goto('http://127.0.0.1:8878/he/', wait_until='networkidle')
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/he_top.png')
        title = await page.title()
        print('HE title:', title)
        direction = await page.get_attribute('html', 'dir')
        print('HE dir:', direction)
        assert direction == 'rtl'
        chips = await page.locator('.chip').count()
        print('HE preset chips:', chips)

        await page.set_input_files('#fileInput', '/opt/data/projects/private-video-compressor-research/tests/test_small.mp4')
        await page.wait_for_timeout(1500)
        print('HE controls visible:', await page.is_visible('#controls'))
        await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/he_loaded.png')

        await page.click('.chip[data-preset="whatsapp"]')
        await page.click('#compressBtn')
        try:
            await page.wait_for_selector('#result:not([hidden])', timeout=180000)
            summary = await page.text_content('#resultSummary')
            print('HE RESULT SUMMARY:', summary)
            await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/he_result.png')
        except Exception as e:
            print('HE compression timeout:', e)
            print('phase:', await page.text_content('#phase'))

        print('JS errors:', errors if errors else 'none')
        await browser.close()

asyncio.run(main())
