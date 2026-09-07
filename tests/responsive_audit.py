import asyncio
from playwright.async_api import async_playwright

# Mobile-first responsive audit: multiple viewports, EN+HE, light+dark
VIEWPORTS = [
    ("phone-sm", 360, 740),
    ("phone-lg", 414, 896),
    ("tablet", 768, 1024),
    ("desktop", 1280, 900),
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        issues = []
        for name, w, h in VIEWPORTS:
            page = await browser.new_page(viewport={'width': w, 'height': h})
            for lang in ['', 'he/']:
                url = f'http://127.0.0.1:8879/site/{lang}'
                await page.goto(url, wait_until='networkidle')
                await page.wait_for_timeout(400)
                audit = await page.evaluate("""() => {
                  const out = {overflow: 0, problems: []};
                  out.overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
                  // header nav audit
                  const nav = document.querySelector('.site-header nav ul');
                  const header = document.querySelector('.site-header');
                  if (nav) {
                    const nb = nav.getBoundingClientRect();
                    out.navH = Math.round(nb.height);
                    out.navItems = nav.querySelectorAll('li').length;
                    // is nav wrapping into many rows (tall nav = bad on phone)?
                    out.headerH = Math.round(header.getBoundingClientRect().height);
                  }
                  // elements overflowing horizontally
                  const vw = document.documentElement.clientWidth;
                  document.querySelectorAll('body *').forEach(e => {
                    const b = e.getBoundingClientRect();
                    if (b.width > 0 && (b.right > vw + 8)) {
                      const cls = (e.className||'').toString().slice(0,30);
                      out.problems.push(e.tagName + '.' + cls + ' right=' + Math.round(b.right));
                    }
                  });
                  out.problems = out.problems.slice(0, 4);
                  return out;
                }""")
                label = name + ('/HE' if lang else '/EN')
                if audit['overflow'] > 2 or audit['problems']:
                    issues.append(f"{label}: overflow={audit['overflow']}px headerH={audit['headerH']} problems={audit['problems']}")
                else:
                    print(f"OK  {label}: headerH={audit['headerH']} navH={audit['navH']} overflow=0")
            await page.close()
        print()
        if issues:
            print("ISSUES:")
            for i in issues: print(" -", i)
        else:
            print("ALL CLEAN")
        await browser.close()

asyncio.run(main())
