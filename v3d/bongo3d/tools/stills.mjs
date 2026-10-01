// Standbilder zu beliebigen Zeitpunkten rendern (schneller Check ohne Voll-Render).
//   node tools/stills.mjs out_dir 0.5 1.2 3.0 [--page index.html]
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const PUP = process.env.PUPPETEER_CORE || path.join(process.env.LOCALAPPDATA, 'npm-cache/_npx/f293411582888030/node_modules/puppeteer-core');
const puppeteer = require(PUP);

const args = process.argv.slice(2);
const outDir = args.shift();
let page = 'index.html';
const pi = args.indexOf('--page');
if (pi >= 0) { page = args[pi + 1]; args.splice(pi, 2); }
const times = args.map(Number);
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/, '$1')), '..');

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.wav': 'audio/wav', '.mp3': 'audio/mpeg', '.json': 'application/json', '.css': 'text/css' };
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  fs.readFile(p, (err, data) => {
    if (err) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(p)] || 'application/octet-stream' });
    res.end(data);
  });
});
await new Promise((r) => server.listen(0, r));
const port = server.address().port;

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  headless: 'new',
  userDataDir: path.join(process.env.TEMP, 'bongo-stills-profile'),
  args: ['--no-first-run', '--no-default-browser-check', '--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader'],
});
const tab = await browser.newPage();
await tab.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
const errs = [];
tab.on('pageerror', (e) => errs.push(String(e)));
tab.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()); });
await tab.goto(`http://localhost:${port}/${page}`, { waitUntil: 'networkidle0', timeout: 120000 });
await tab.waitForFunction('window.__bongoReady === true', { timeout: 60000 }).catch(() => {});
fs.mkdirSync(outDir, { recursive: true });
const t0 = Date.now();
for (const t of times) {
  await tab.evaluate((tt) => window.renderAt(tt), t);
  const el = await tab.$('#gl');
  await el.screenshot({ path: path.join(outDir, `t${t.toFixed(2)}.png`) });
}
console.log(`${times.length} stills in ${((Date.now() - t0) / 1000).toFixed(1)}s`);
const info = await tab.evaluate(() => { const c = document.getElementById('gl'); const g = c.getContext('webgl2'); const d = g && g.getExtension('WEBGL_debug_renderer_info'); return d ? g.getParameter(d.UNMASKED_RENDERER_WEBGL) : 'n/a'; });
console.log('GPU:', info);
if (errs.length) console.log('ERRORS:\n' + errs.slice(0, 10).join('\n'));
await browser.close();
server.close();
