// Renders stills and the screw-on/off animation from render.html.
// Usage (from bottle-cap-prototype/):  python3 -m http.server 8765 &  node render/render.js
// Needs: playwright with Chromium, ffmpeg.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const OUT = path.join(__dirname, 'out');
const BASE = 'http://localhost:8765/render/render.html';

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-gl=swiftshader', '--ignore-certificate-errors'],
    proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY, bypass: 'localhost,127.0.0.1' } : undefined });

  async function open(mode, w, h, scale) {
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
    page.on('pageerror', e => console.error('page error:', e.message));
    await page.goto(`${BASE}#${mode}`, { waitUntil: 'networkidle' });
    await page.waitForFunction(() => window.renderReady === true, null, { timeout: 120000 });
    return page;
  }

  for (const [mode, file] of [['bottle', 'cap-on-bottle.png'], ['cap', 'cap-alone.png']]) {
    const page = await open(mode, 1200, 1500, 2);
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(OUT, file) });
    await page.close();
    console.log('wrote', file);
  }

  const FPS = 30, SECONDS = 8;
  const frames = path.join(OUT, 'frames');
  fs.rmSync(frames, { recursive: true, force: true }); fs.mkdirSync(frames);
  const page = await open('screw', 1280, 800, 1);
  for (let i = 0; i < FPS * SECONDS; i++) {
    await page.evaluate(t => window.setFrame(t), i / FPS);
    await page.screenshot({ path: path.join(frames, `f${String(i).padStart(4, '0')}.png`) });
  }
  await browser.close();
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(frames, 'f%04d.png'),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', path.join(OUT, 'cap-screw-on-off.mp4')]);
  fs.rmSync(frames, { recursive: true, force: true });
  console.log('wrote cap-screw-on-off.mp4');
})();
