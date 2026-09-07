import asyncio
from playwright.async_api import async_playwright

# Test real size-reduction on the medium video (crf20 gradient, 280KB source may already be compact;
# use the LARGE test video from user's own recordings? No - use a bigger synthetic: compress test_small UP is invalid.
# Better test: compress the SIMULATED 20MB output (7.5MB real ffmpeg output) down to 2MB via custom preset.

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))

        await page.goto('http://127.0.0.1:8878/', wait_until='networkidle')
        await page.set_input_files('#fileInput', '/opt/data/projects/private-video-compressor-research/tests/out_20mb_sim.mp4')
        await page.wait_for_timeout(1500)
        # custom target: 2MB
        await page.click('.chip[data-preset="custom"]')
        await page.locator('#customRange').evaluate("el => { el.value = 2; el.dispatchEvent(new Event('input', {bubbles:true})); }")
        val = await page.text_content('#customVal')
        print('custom target:', val, 'MB')
        await page.click('#compressBtn')
        try:
            await page.wait_for_selector('#result:not([hidden])', timeout=300000)
            summary = await page.text_content('#resultSummary')
            print('SUMMARY:', summary)
            # get the download href size
            href = await page.get_attribute('#downloadBtn', 'href')
            print('download blob available:', bool(href and href.startswith('blob:')))
            await page.screenshot(path='/opt/data/projects/private-video-compressor-research/tests/en_custom_result.png')
        except Exception as e:
            print('TIMEOUT:', e)
            print('phase:', await page.text_content('#phase'))
        print('JS errors:', errors if errors else 'none')
        await browser.close()

asyncio.run(main())
