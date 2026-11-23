const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const FPS = 30, DUR = 10;
const outDir = process.argv[2];
const only = process.argv[3] ? process.argv[3].split(',').map(Number) : null; // seconds for preview
(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(__dirname, 'skit.html'));
  await page.evaluate(async () => {
    await Promise.all(['500', '700'].map(w => document.fonts.load(`${w} 40px Cairo`, 'بكام؟ abc')));
    await document.fonts.load('40px "Noto Color Emoji"', '😭👌👍🙂');
    await document.fonts.ready;
  });
  const ok = await page.evaluate(() => [document.fonts.check('700 40px Cairo', 'بكام'), document.fonts.check('500 40px Cairo', 'بكام')]);
  console.log('fonts loaded:', ok);
  // snapshot frame 0 so the scene can crossfade back to it at the loop seam
  await page.evaluate(() => window.render(0));
  const first = await page.screenshot();
  await page.evaluate(src => window.setLoopImage(src), 'data:image/png;base64,' + first.toString('base64'));
  const frames = only ? only.map(s => Math.round(s * FPS)) : [...Array(FPS * DUR).keys()];
  for (const f of frames) {
    await page.evaluate(t => window.render(t), f / FPS);
    await page.screenshot({ path: path.join(outDir, only ? `t${f / FPS}.png` : `f${String(f).padStart(4, '0')}.png`) });
  }
  await browser.close();
})();
