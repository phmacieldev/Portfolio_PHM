const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const BASE_URL = 'http://localhost:8080';
const OUTPUT_DIR = path.join(__dirname, '..', 'public', 'images', 'sesmt');

if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

async function shot(page, name) {
  const file = path.join(OUTPUT_DIR, `${name}.png`);
  await page.screenshot({ path: file, fullPage: false });
  console.log(`Saved: ${name}.png`);
}

async function wait(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function goAndShot(page, route, name) {
  await page.goto(BASE_URL + route, { waitUntil: 'networkidle2', timeout: 12000 }).catch(() => {});
  await wait(1500);
  await shot(page, name);
}

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    defaultViewport: { width: 1440, height: 860 }
  });

  const page = await browser.newPage();

  // Login
  await page.goto(BASE_URL + '/login', { waitUntil: 'networkidle2', timeout: 15000 });
  await shot(page, '01_login');

  await page.type('input[name="username"]', 'admin');
  await page.type('input[type="password"]', 'admin@123');

  const buttons = await page.$$('button');
  for (const btn of buttons) {
    const text = await page.evaluate(el => el.textContent.trim(), btn);
    if (text.toLowerCase().includes('entrar')) { await btn.click(); break; }
  }
  await wait(3000);

  // Home / Dashboard principal
  await shot(page, '02_home');

  // Dashboard de exames
  await goAndShot(page, '/dashboard', '03_dashboard_exames');

  // Agendar exame
  await goAndShot(page, '/agendar', '04_agendar');

  // Agenda (calendário)
  await goAndShot(page, '/agenda', '05_agenda');

  // Dashboard sangue
  await goAndShot(page, '/dashboard_sangue', '06_dashboard_sangue');

  // Relatório ASO (dashboard_exames)
  await goAndShot(page, '/dashboard_exames', '07_relatorio_aso');

  // Atestados lista semanal
  await goAndShot(page, '/atestados', '08_atestados');

  // Atestados indicadores
  await goAndShot(page, '/atestados/indicadores', '09_atestados_indicadores');

  // Relatório de funcionários
  await goAndShot(page, '/funcionarios', '10_funcionarios');

  // Estatísticas de exames
  await goAndShot(page, '/dashboard_estatisticas', '11_estatisticas');

  // Indicadores SESMT
  await goAndShot(page, '/indicadores', '12_indicadores');

  // Admin - usuários
  await goAndShot(page, '/admin/usuarios', '13_admin_usuarios');

  // Admin - auditoria
  await goAndShot(page, '/admin/auditoria', '14_admin_auditoria');

  await browser.close();
  console.log('\nDone! All screenshots saved to:', OUTPUT_DIR);
})();
