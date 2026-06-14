const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const BASE = 'https://finance-api-web.vercel.app';
const OUT  = path.join(__dirname, '..', 'public', 'images', 'finance');
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

const wait = ms => new Promise(r => setTimeout(r, ms));
async function shot(page, name) {
  await page.screenshot({ path: path.join(OUT, `${name}.png`) });
  console.log(`[finance] ${name}.png | ${page.url()}`);
}
async function go(page, route, name) {
  await page.goto(BASE + route, { waitUntil: 'networkidle2', timeout: 15000 }).catch(() => {});
  await wait(1800);
  await shot(page, name);
}
async function login(page, email, pass) {
  // fresh cookies
  const client = await page.createCDPSession();
  await client.send('Network.clearBrowserCookies');
  await page.goto(BASE + '/login', { waitUntil: 'networkidle2', timeout: 15000 });
  await wait(1000);
  const emailSel = ['input[type="email"]','input[name="email"]','input[name="username"]'];
  let ef = null;
  for (const s of emailSel) { ef = await page.$(s); if (ef) break; }
  const pf = await page.$('input[type="password"]');
  if (ef && pf) {
    await ef.click({clickCount:3}); await ef.type(email);
    await pf.click({clickCount:3}); await pf.type(pass);
    const btns = await page.$$('button');
    for (const b of btns) {
      const t = await page.evaluate(e => e.textContent.trim().toLowerCase(), b);
      if (t.includes('entrar')||t.includes('login')||t.includes('sign')) { await b.click(); break; }
    }
    await wait(4000);
  }
}

(async () => {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'], defaultViewport: { width: 1440, height: 860 } });

  // === Admin user (phmsfaria) — acessa painel admin ===
  const adminPage = await browser.newPage();
  await adminPage.goto(BASE + '/login', { waitUntil: 'networkidle2', timeout: 15000 });
  await shot(adminPage, '01_login');
  await login(adminPage, 'phmsfaria@gmail.com', '53812277');
  await shot(adminPage, '02_admin_painel');
  await go(adminPage, '/admin-usuarios',         '03_admin_usuarios');
  await go(adminPage, '/configuracoes',           '04_configuracoes');
  await go(adminPage, '/painel-admin/audit-log',  '05_audit_log');

  // === Regular user (pedrohenrique) — vê dashboard financeiro ===
  const userPage = await browser.newPage();
  await login(userPage, 'pedrohenrique_maciel@hotmail.com', '12345678');
  await shot(userPage, '06_user_home');

  // print nav to know available routes
  const nav = await userPage.evaluate(() => { const n = document.querySelector('nav,aside,[class*="sidebar"],[class*="Sidebar"]'); return n ? n.innerText.slice(0,600) : document.body.innerText.slice(0,400); });
  const links = await userPage.evaluate(() => [...document.querySelectorAll('a[href]')].map(a=>a.pathname));
  console.log('[finance] user nav:', nav);
  console.log('[finance] user links:', [...new Set(links)].slice(0,20));

  // Rotas financeiras comuns
  const userRoutes = [
    ['/dashboard','07_dashboard'],
    ['/transacoes','08_transacoes'],
    ['/contas','09_contas'],
    ['/investimentos','10_investimentos'],
    ['/relatorios','11_relatorios'],
    ['/categorias','12_categorias'],
    ['/orcamento','13_orcamento'],
    ['/metas','14_metas'],
    ['/extrato','15_extrato'],
    ['/cartoes','16_cartoes'],
  ];
  for (const [route, name] of userRoutes) {
    await userPage.goto(BASE + route, { waitUntil: 'networkidle2', timeout: 12000 }).catch(() => {});
    await wait(1800);
    if (!userPage.url().includes('login')) await shot(userPage, name);
    else console.log('[finance] skipped', route);
  }

  await browser.close();
  console.log('[finance] Done!');
})();
