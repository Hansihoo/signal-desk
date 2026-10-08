// Run after publish; the caller provides Playwright and owns browser scratch.
// Optional arguments: preview directory/URL, screenshot output directory.
const assert = require('assert');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require(process.argv[2] || 'playwright');
const root = process.argv[4] || 'site/preview';
const base = /^https?:/.test(root) ? root.replace(/\/?$/, '/') : pathToFileURL(path.resolve(root) + path.sep).href;
const pages = ['ai-model-guides.html', 'index.html', 'ai-models.html',
  'mcp-apps-workflows.html', 'model-guides/gpt-6-1-sol-model-guide.html'];

(async () => {
  const browser = await chromium.launch({ executablePath: process.argv[3] || undefined,
    headless: true, args: ['--allow-file-access-from-files'] });
  const errors = [];
  let checked = 0;
  try {
    const page = await browser.newPage();
    page.on('pageerror', error => errors.push(error.message));
    for (const width of [320, 390, 736, 768, 980, 1280, 1440]) {
      await page.setViewportSize({ width, height: 900 });
      for (const filename of pages) {
        await page.goto(new URL(filename, base).href);
        await page.evaluate(() => document.fonts.ready);
        const geometry = await page.evaluate(() => {
          const button = document.querySelector('#header .menu-toggle');
          const logo = document.querySelector('#header .logo');
          const b = button.getBoundingClientRect(), l = logo.getBoundingClientRect();
          const hit = document.elementFromPoint(l.x + l.width / 2, l.y + l.height / 2);
          return { separated: b.right + 8 <= l.left,
            aligned: Math.abs(b.y + b.height / 2 - l.y - l.height / 2) < 1,
            target: b.width >= 44 && b.height >= 44,
            brandClickable: hit === logo || logo.contains(hit),
            fits: document.documentElement.scrollWidth <= innerWidth };
        });
        assert.deepEqual(geometry, { separated: true, aligned: true, target: true,
          brandClickable: true, fits: true }, `${filename} at ${width}px`);
        checked++;
        if (filename !== pages[0]) continue;
        const total = await page.locator('#model-page-rows tr:visible').count();
        assert.ok(total > 0);
        const metadata = await page.locator('#model-page-rows tr:visible').first().locator('td:not(:first-child)').evaluateAll(cells =>
          cells.every(cell => {
            const range = document.createRange(); range.selectNodeContents(cell);
            const lines = [...range.getClientRects()];
            return lines.length === 1 && lines[0].width <= cell.clientWidth;
          }));
        assert.equal(metadata, true, `Library category/dates must remain readable at ${width}px`);
        await page.locator('#model-page-query').fill('GPT-6.1');
        assert.equal(await page.locator('#model-page-rows tr:visible').count(), 1);
        await page.locator('#model-page-query').fill('no-model-matches-this-query');
        assert.equal(await page.locator('#model-page-rows tr:visible').count(), 0);
        assert.equal(await page.locator('#model-page-empty').isVisible(), true);
        await page.locator('#model-page-query').fill('');
        assert.equal(await page.locator('#model-page-rows tr:visible').count(), total);
        const toggle = page.locator('#header .menu-toggle');
        const close = page.locator('#sidebar .sidebar-close');
        if (await toggle.getAttribute('aria-expanded') === 'true') {
          await toggle.click();
          await page.waitForTimeout(550);
        }
        await toggle.focus();
        await toggle.press('Enter');
        await page.waitForTimeout(550);
        assert.equal(await toggle.getAttribute('aria-expanded'), 'true');
        assert.equal(await page.locator('#sidebar-inner').evaluate(el => el.inert), false);
        await close.click();
        await page.waitForTimeout(550);
        assert.equal(await toggle.getAttribute('aria-expanded'), 'false');
        assert.equal(await toggle.evaluate(el => el === document.activeElement), true);
        await toggle.press('Space');
        await page.waitForTimeout(550);
        await page.keyboard.press('Escape');
        await page.waitForTimeout(550);
        assert.equal(await toggle.getAttribute('aria-expanded'), 'false');
        assert.equal(await page.locator('#sidebar-inner').evaluate(el => el.inert), true);
        if (width <= 1280) {
          await toggle.click();
          await page.waitForTimeout(550);
          await page.mouse.click(width - 4, 250);
          await page.waitForTimeout(550);
          assert.equal(await toggle.getAttribute('aria-expanded'), 'false');
        }
        if (process.argv[5] && [390, 768, 1440].includes(width)) {
          await page.screenshot({ path: path.join(process.argv[5], `header-fixed-${width}.png`) });
        }
        await page.locator('#header .logo').click();
        await page.waitForURL(new URL('index.html', base).href);
      }
    }
    assert.deepEqual(errors, []);
    console.log(`Header: ${checked} page/width checks; 44px targets, brand hit test, Enter/Space, close/Escape/outside click pass.`);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
