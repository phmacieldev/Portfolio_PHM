const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const BASE = 'https://finance-api-web.vercel.app';
const OUT  = path.join(__dirname, '..', 'public', 'images', 'finance');

const wait = ms => new Promise(r => setTimeout(r, ms));
async function shot(page, name) {
  await page.screenshot({ path: path.join(OUT, `${name}.png`) });
  console.log(`[finance] ${name}.png`);
}

(async () => {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'], defaultViewport: { width: 1440, height: 860 } });
  const page = await browser.newPage();

  // Login regular user
  await page.goto(BASE + '/login', { waitUntil: 'networkidle2', timeout: 15000 });
  const ef = await page.$('input[type="email"]') || await page.$('input[name="email"]');
  const pf = await page.$('input[type="password"]');
  await ef.type('pedrohenrique_maciel@hotmail.com');
  await pf.type('12345678');
  const btns = await page.$$('button');
  for (const b of btns) {
    const t = await page.evaluate(e => e.textContent.trim().toLowerCase(), b);
    if (t.includes('entrar')||t.includes('login')||t.includes('sign')) { await b.click(); break; }
  }
  await wait(4000);

  const routes = [
    ['/extratos',    '08_extratos'],
    ['/categorias',  '09_categorias'],
    ['/contas',      '10_contas'],
    ['/previsoes',   '11_previsoes'],
    ['/conciliacao', '12_conciliacao'],
    ['/dre',         '13_dre'],
    ['/relatorio',   '14_relatorio'],
  ];

  for (const [route, name] of routes) {
    await page.goto(BASE + route, { waitUntil: 'networkidle2', timeout: 12000 }).catch(() => {});
    await wait(1800);
    if (!page.url().includes('login')) await shot(page, name);
  }

  await browser.close();
  console.log('[finance] Done!');
})();
