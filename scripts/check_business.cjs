// Run after publish; the caller owns Playwright browser scratch.
const assert = require('assert');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require(process.argv[2] || 'playwright');
const root = process.argv[4] || 'site/preview';
const base = /^https?:/.test(root) ? root.replace(/\/?$/, '/') : pathToFileURL(path.resolve(root) + path.sep).href;
const reportIds = ['polaris-government-opportunities', 'polaris-sales-opportunities', 'office-business-directions'];

(async () => {
  const browser = await chromium.launch({ executablePath: process.argv[3] || undefined, headless: true,
    args: ['--allow-file-access-from-files'] });
  const errors = [];
  let checked = 0;
  try {
    const page = await browser.newPage();
    page.on('pageerror', error => errors.push(error.message));
    for (const width of [320, 390, 768, 1280, 1440]) {
      await page.setViewportSize({ width, height: 900 });
      for (const file of ['business.html', ...reportIds.map(id => id + '.html')]) {
        const response = await page.goto(new URL(file, base).href);
        if (response) assert(response.ok(), `${file} response`);
        await page.evaluate(() => document.fonts.ready);
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${file} overflow at ${width}`);
        const brand = await page.locator('#header .logo').boundingBox();
        const menu = await page.locator('#header .menu-toggle').boundingBox();
        assert(menu.x + menu.width + 8 <= brand.x, `${file} header at ${width}`);
        checked++;
      }
    }
    await page.goto(new URL('business.html', base).href);
    const count = () => page.locator('#board .research-post:visible').count();
    assert.equal(await count(), 3);
    for (const category of ['국책사업', '영업 기회', '경쟁사·시장']) {
      await page.locator('#report-topic').selectOption('사업 / ' + category);
      assert.equal(await count(), 1, category);
    }
    await page.locator('#report-topic').selectOption('');
    await page.locator('#report-query').fill('does-not-exist');
    assert.equal(await count(), 0);
    assert(await page.locator('.board-empty').isVisible());
    await page.locator('#report-query').fill('구조화');
    assert((await count()) > 0);
    await page.locator('#report-query').fill('');
    assert.equal(await count(), 3);
    await page.locator('#board a[href="polaris-government-opportunities.html"]').first().click();
    assert(page.url().includes('polaris-government-opportunities.html'));
    assert(await page.locator('body').innerText().then(text => text.includes('3월 30일')));
    await page.goBack();
    if (process.argv[5]) {
      await page.setViewportSize({ width: 390, height: 1100 });
      await page.goto(new URL('business.html', base).href);
      await page.evaluate(() => document.fonts.ready);
      await page.waitForFunction(() => document.querySelector('#sidebar').classList.contains('inactive'));
      await page.screenshot({ path: process.argv[5], fullPage: true, animations: 'disabled' });
    }
    await page.goto(new URL('../research/business/index.html', base).href);
    assert.equal(await count(), 3);
    await page.locator('#board .research-post a').first().click();
    assert(reportIds.some(id => page.url().includes('/preview/' + id + '.html')));
    if (process.argv[6]) {
      await page.goto(pathToFileURL(path.resolve(process.argv[6])).href);
      for (const width of [320, 390, 1280]) {
        await page.setViewportSize({ width, height: 900 });
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `private overflow ${width}`);
      }
      assert.equal(await page.locator('article:visible').count(), 3);
      await page.locator('#category').selectOption('국책사업');
      assert.equal(await page.locator('article:visible').count(), 1);
      await page.locator('#category').selectOption('');
      await page.locator('#status').selectOption('검토 중');
      assert.equal(await page.locator('article:visible').count(), 1);
      await page.locator('#status').selectOption('');
      await page.locator('#query').fill('does-not-exist');
      assert.equal(await page.locator('article:visible').count(), 0);
    }
    assert.deepEqual(errors, []);
    console.log(`PASS: ${checked} business page/width checks; public filters, empty/reset, detail/formal links; private checks when supplied`);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
