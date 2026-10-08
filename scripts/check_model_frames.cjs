// Run after publishing. Dependencies and the isolated browser come from the
// caller; this checker never writes profiles/screenshots into the repository.
const { pathToFileURL } = require('url');
const path = require('path');
const assert = require('assert');
const { chromium } = require(process.argv[2] || 'playwright');

(async () => {
  const browser = await chromium.launch({
    executablePath: process.argv[3] || undefined,
    headless: true,
    args: ['--allow-file-access-from-files'],
  });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    const root = path.resolve(process.argv[4] || 'site/preview/model-guides');
    await page.goto(pathToFileURL(path.join(root, 'llm-models.html')).href);
    const frame = page.locator('iframe').contentFrame();
    await frame.locator('#filter-tool-button').waitFor();
    await page.waitForTimeout(500); // Original chart/height observation finishes.
    for (const id of ['tool', 'provider', 'access', 'tier', 'status']) {
      await frame.locator(`#filter-${id}-button`).click();
      const height = await page.locator('iframe').evaluate(element => element.style.height);
      await frame.locator(`#filter-${id}-all`).uncheck();
      await page.waitForTimeout(300);
      assert.equal(await page.locator('iframe').evaluate(element => element.style.height), height,
        'Changing filtered rows must not move an open popup');
      assert.equal(await frame.locator('#tbl tbody tr:visible').count(), 0);
      await frame.locator(`#filter-${id}-option-0`).check();
      assert.ok(await frame.locator('#tbl tbody tr:visible').count());
      await frame.locator(`#filter-${id}-option-0`).press('Escape');
      await frame.locator('#reset').click();
      await page.waitForTimeout(150); // Source chart redraws after reset (40ms).
    }
    assert.deepEqual(errors, []);
    console.log('Source table: five filters, empty/result states, stable popup viewport, Escape/reset pass.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
