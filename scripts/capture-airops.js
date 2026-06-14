const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const BASE = 'https://air-ops-system-web.vercel.app';
const OUT  = path.join(__dirname, '..', 'public', 'images', 'airops');
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

const wait = ms => new Promise(r => setTimeout(r, ms));
async function shot(page, name) {
  await page.screenshot({ path: path.join(OUT, `${name}.png`) });
  console.log(`[airops] ${name}.png`);
}
async function go(page, route, name) {
  await page.goto(BASE + route, { waitUntil: 'networkidle2', timeout: 15000 }).catch(() => {});
  await wait(1800);
  await shot(page, name);
}

(async () => {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'], defaultViewport: { width: 1440, height: 860 } });
  const page = await browser.newPage();

  // Login
  await page.goto(BASE + '/login', { waitUntil: 'networkidle2', timeout: 15000 });
  await shot(page, '01_login');
  await page.type('input[type="email"]', 'phmsfaria@gmail.com');
  await page.type('input[type="password"]', '8dciian0f');
  const btns = await page.$$('button');
  for (const b of btns) {
    const t = await page.evaluate(e => e.textContent.trim().toLowerCase(), b);
    if (t.includes('entrar') || t.includes('login') || t.includes('sign')) { await b.click(); break; }
  }
  await wait(4000);
  await shot(page, '02_dashboard');

  // Rotas reais do sistema
  await go(page, '/police/roster',    '03_roster');
  await go(page, '/police/briefings', '04_briefings');
  await go(page, '/police/badges',    '05_badges');
  await go(page, '/police/documents', '06_documents');
  await go(page, '/police/rolecall',  '07_rolecall');
  await go(page, '/settings',         '08_settings');
  await go(page, '/register',         '09_register');

  await browser.close();
  console.log('[airops] Done!');
})();
