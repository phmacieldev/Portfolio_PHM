import re, sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ── ASD (featured) carousel ──────────────────────────────────────────────────
asd_carousel = '''
      <!-- SCREENSHOTS GALLERY -->
      <div style="margin-top:2rem;" class="reveal">
        <div style="font-size:0.65rem;letter-spacing:0.15em;color:var(--muted2);text-transform:uppercase;margin-bottom:1.2rem;" data-i18n="feat_gallery_label">// Sistema em Produção</div>

        <div id="asd-carousel" style="position:relative;border-radius:8px;overflow:hidden;border:1px solid var(--border2);background:var(--bg3);">
          <div style="position:relative;aspect-ratio:16/9;overflow:hidden;cursor:zoom-in;" onclick="asdOpenLightbox(asdIdx)">
            <img id="asd-main-img" src="public/images/airops/02_dashboard.png" alt="ASD" style="width:100%;height:100%;object-fit:cover;object-position:top;transition:opacity 0.25s;" />
            <div style="position:absolute;bottom:0;left:0;right:0;padding:0.75rem 1rem;background:linear-gradient(transparent,rgba(8,10,15,0.85));display:flex;align-items:center;justify-content:space-between;">
              <span id="asd-main-label" style="font-size:0.65rem;letter-spacing:0.12em;color:var(--text);text-transform:uppercase;">Dashboard</span>
              <span style="font-size:0.6rem;color:var(--muted2);">clique para ampliar</span>
            </div>
            <button onclick="event.stopPropagation();asdNav(-1)" style="position:absolute;left:0.8rem;top:50%;transform:translateY(-50%);background:rgba(8,10,15,0.7);border:1px solid var(--border2);color:var(--text);width:2rem;height:2rem;border-radius:50%;cursor:pointer;font-size:0.9rem;display:flex;align-items:center;justify-content:center;" onmouseover="this.style.background=\'rgba(79,142,247,0.3)\'" onmouseout="this.style.background=\'rgba(8,10,15,0.7)\'">&#8249;</button>
            <button onclick="event.stopPropagation();asdNav(1)"  style="position:absolute;right:0.8rem;top:50%;transform:translateY(-50%);background:rgba(8,10,15,0.7);border:1px solid var(--border2);color:var(--text);width:2rem;height:2rem;border-radius:50%;cursor:pointer;font-size:0.9rem;display:flex;align-items:center;justify-content:center;" onmouseover="this.style.background=\'rgba(79,142,247,0.3)\'" onmouseout="this.style.background=\'rgba(8,10,15,0.7)\'">&#8250;</button>
          </div>
          <div style="display:flex;gap:0.5rem;padding:0.75rem;overflow-x:auto;scrollbar-width:thin;scrollbar-color:var(--border2) transparent;" id="asd-thumbs"></div>
        </div>
      </div>

      <div id="asd-lightbox" onclick="asdCloseLightbox()" style="display:none;position:fixed;inset:0;z-index:999;background:rgba(0,0,0,0.92);align-items:center;justify-content:center;cursor:zoom-out;">
        <button onclick="event.stopPropagation();asdNav(-1)" style="position:fixed;left:1.5rem;top:50%;transform:translateY(-50%);background:rgba(30,37,53,0.9);border:1px solid var(--border2);color:var(--text);width:3rem;height:3rem;border-radius:50%;cursor:pointer;font-size:1.4rem;display:flex;align-items:center;justify-content:center;">&#8249;</button>
        <img id="asd-lb-img" src="" alt="" style="max-width:92vw;max-height:90vh;border-radius:6px;object-fit:contain;box-shadow:0 0 60px rgba(0,0,0,0.8);" onclick="event.stopPropagation()" />
        <button onclick="event.stopPropagation();asdNav(1)"  style="position:fixed;right:1.5rem;top:50%;transform:translateY(-50%);background:rgba(30,37,53,0.9);border:1px solid var(--border2);color:var(--text);width:3rem;height:3rem;border-radius:50%;cursor:pointer;font-size:1.4rem;display:flex;align-items:center;justify-content:center;">&#8250;</button>
        <button onclick="asdCloseLightbox()" style="position:fixed;top:1rem;right:1rem;background:transparent;border:none;color:var(--muted);font-size:1.5rem;cursor:pointer;">&#x2715;</button>
        <div id="asd-lb-label" style="position:fixed;bottom:1.5rem;left:50%;transform:translateX(-50%);font-size:0.7rem;letter-spacing:0.12em;color:var(--muted);text-transform:uppercase;"></div>
      </div>

      <script>
      (function(){
        const slides = [
          { src:\'public/images/airops/02_dashboard.png\', label:\'Dashboard\' },
          { src:\'public/images/airops/03_roster.png\',    label:\'Roster — Efetivo\' },
          { src:\'public/images/airops/04_briefings.png\', label:\'Briefings\' },
          { src:\'public/images/airops/05_badges.png\',    label:\'Badges\' },
          { src:\'public/images/airops/06_documents.png\', label:\'Documentos\' },
          { src:\'public/images/airops/07_rolecall.png\',  label:\'Role Call\' },
          { src:\'public/images/airops/08_settings.png\',  label:\'Configurações\' },
          { src:\'public/images/airops/09_register.png\',  label:\'Cadastrar Oficial\' },
          { src:\'public/images/airops/01_login.png\',     label:\'Login\' },
        ];
        window.asdIdx = 0;
        const mainImg  = document.getElementById(\'asd-main-img\');
        const mainLbl  = document.getElementById(\'asd-main-label\');
        const lbImg    = document.getElementById(\'asd-lb-img\');
        const lbLbl    = document.getElementById(\'asd-lb-label\');
        const lightbox = document.getElementById(\'asd-lightbox\');
        const thumbsEl = document.getElementById(\'asd-thumbs\');
        slides.forEach((s,i) => {
          const th = document.createElement(\'img\');
          th.src=s.src; th.alt=s.label; th.title=s.label; th.dataset.i=i;
          th.style.cssText=\'height:56px;aspect-ratio:16/9;object-fit:cover;object-position:top;border-radius:4px;cursor:pointer;border:2px solid transparent;flex-shrink:0;transition:border-color 0.2s,opacity 0.2s;opacity:0.55;\';
          th.onclick=()=>asdSet(i); thumbsEl.appendChild(th);
        });
        function asdSet(i) {
          window.asdIdx=(i+slides.length)%slides.length;
          const s=slides[window.asdIdx];
          mainImg.style.opacity=\'0\';
          setTimeout(()=>{ mainImg.src=s.src; mainImg.style.opacity=\'1\'; },150);
          mainLbl.textContent=s.label;
          if(lightbox.style.display===\'flex\'){ lbImg.src=s.src; lbLbl.textContent=s.label; }
          thumbsEl.querySelectorAll(\'img\').forEach((th,j)=>{ th.style.borderColor=j===window.asdIdx?\'var(--accent)':\'transparent\'; th.style.opacity=j===window.asdIdx?\'1\':\'0.55\'; });
          const act=thumbsEl.querySelectorAll(\'img\')[window.asdIdx]; if(act) act.scrollIntoView({behavior:\'smooth\',inline:\'center\',block:\'nearest\'});
        }
        window.asdNav=function(d){ asdSet(window.asdIdx+d); };
        window.asdOpenLightbox=function(i){ asdSet(i); lbImg.src=slides[window.asdIdx].src; lbLbl.textContent=slides[window.asdIdx].label; lightbox.style.display=\'flex\'; document.body.style.overflow=\'hidden\'; };
        window.asdCloseLightbox=function(){ lightbox.style.display=\'none\'; document.body.style.overflow=\'\'; };
        document.addEventListener(\'keydown\',e=>{ if(lightbox.style.display!==\'flex\') return; if(e.key===\'ArrowLeft\') asdNav(-1); if(e.key===\'ArrowRight\') asdNav(1); if(e.key===\'Escape\') asdCloseLightbox(); });
        asdSet(0);
      })();
      </script>

    <!-- stack pills -->'''

# ── Finance carousel ──────────────────────────────────────────────────────────
fin_carousel = '''    <!-- GALLERY (outside hero card, like ASD) -->
    <div style="margin-top:2rem;" class="reveal">
      <div style="font-size:0.65rem;letter-spacing:0.15em;color:var(--muted2);text-transform:uppercase;margin-bottom:1.2rem;" data-i18n="fin_gallery_label">// Sistema em Produção</div>

      <div id="fin-carousel" style="position:relative;border-radius:8px;overflow:hidden;border:1px solid var(--border2);background:var(--bg3);">
        <div style="position:relative;aspect-ratio:16/9;overflow:hidden;cursor:zoom-in;" onclick="finOpenLightbox(finIdx)">
          <img id="fin-main-img" src="public/images/finance/06_user_home.png" alt="Finance" style="width:100%;height:100%;object-fit:cover;object-position:top;transition:opacity 0.25s;" />
          <div style="position:absolute;bottom:0;left:0;right:0;padding:0.75rem 1rem;background:linear-gradient(transparent,rgba(8,10,15,0.85));display:flex;align-items:center;justify-content:space-between;">
            <span id="fin-main-label" style="font-size:0.65rem;letter-spacing:0.12em;color:var(--text);text-transform:uppercase;">Dashboard Financeiro</span>
            <span style="font-size:0.6rem;color:var(--muted2);">clique para ampliar</span>
          </div>
          <button onclick="event.stopPropagation();finNav(-1)" style="position:absolute;left:0.8rem;top:50%;transform:translateY(-50%);background:rgba(8,10,15,0.7);border:1px solid var(--border2);color:var(--text);width:2rem;height:2rem;border-radius:50%;cursor:pointer;font-size:0.9rem;display:flex;align-items:center;justify-content:center;" onmouseover="this.style.background=\'rgba(79,142,247,0.3)\'" onmouseout="this.style.background=\'rgba(8,10,15,0.7)\'">&#8249;</button>
          <button onclick="event.stopPropagation();finNav(1)"  style="position:absolute;right:0.8rem;top:50%;transform:translateY(-50%);background:rgba(8,10,15,0.7);border:1px solid var(--border2);color:var(--text);width:2rem;height:2rem;border-radius:50%;cursor:pointer;font-size:0.9rem;display:flex;align-items:center;justify-content:center;" onmouseover="this.style.background=\'rgba(79,142,247,0.3)\'" onmouseout="this.style.background=\'rgba(8,10,15,0.7)\'">&#8250;</button>
        </div>
        <div style="display:flex;gap:0.5rem;padding:0.75rem;overflow-x:auto;scrollbar-width:thin;scrollbar-color:var(--border2) transparent;" id="fin-thumbs"></div>
      </div>
    </div>

    <div id="fin-lightbox" onclick="finCloseLightbox()" style="display:none;position:fixed;inset:0;z-index:999;background:rgba(0,0,0,0.92);align-items:center;justify-content:center;cursor:zoom-out;">
      <button onclick="event.stopPropagation();finNav(-1)" style="position:fixed;left:1.5rem;top:50%;transform:translateY(-50%);background:rgba(30,37,53,0.9);border:1px solid var(--border2);color:var(--text);width:3rem;height:3rem;border-radius:50%;cursor:pointer;font-size:1.4rem;display:flex;align-items:center;justify-content:center;">&#8249;</button>
      <img id="fin-lb-img" src="" alt="" style="max-width:92vw;max-height:90vh;border-radius:6px;object-fit:contain;box-shadow:0 0 60px rgba(0,0,0,0.8);" onclick="event.stopPropagation()" />
      <button onclick="event.stopPropagation();finNav(1)"  style="position:fixed;right:1.5rem;top:50%;transform:translateY(-50%);background:rgba(30,37,53,0.9);border:1px solid var(--border2);color:var(--text);width:3rem;height:3rem;border-radius:50%;cursor:pointer;font-size:1.4rem;display:flex;align-items:center;justify-content:center;">&#8250;</button>
      <button onclick="finCloseLightbox()" style="position:fixed;top:1rem;right:1rem;background:transparent;border:none;color:var(--muted);font-size:1.5rem;cursor:pointer;">&#x2715;</button>
      <div id="fin-lb-label" style="position:fixed;bottom:1.5rem;left:50%;transform:translateX(-50%);font-size:0.7rem;letter-spacing:0.12em;color:var(--muted);text-transform:uppercase;"></div>
    </div>

    <script>
    (function(){
      const slides = [
        { src:\'public/images/finance/06_user_home.png\',   label:\'Dashboard Financeiro\' },
        { src:\'public/images/finance/08_extratos.png\',     label:\'Extratos\' },
        { src:\'public/images/finance/09_categorias.png\',   label:\'Categorias\' },
        { src:\'public/images/finance/10_contas.png\',       label:\'Contas\' },
        { src:\'public/images/finance/11_previsoes.png\',    label:\'Previsões\' },
        { src:\'public/images/finance/12_conciliacao.png\',  label:\'Conciliação\' },
        { src:\'public/images/finance/13_dre.png\',          label:\'DRE\' },
        { src:\'public/images/finance/14_relatorio.png\',    label:\'Relatório\' },
        { src:\'public/images/finance/02_admin_painel.png\', label:\'Painel Admin\' },
        { src:\'public/images/finance/03_admin_usuarios.png\', label:\'Admin — Usuários\' },
        { src:\'public/images/finance/04_configuracoes.png\', label:\'Configurações\' },
        { src:\'public/images/finance/05_audit_log.png\',    label:\'Audit Log\' },
        { src:\'public/images/finance/01_login.png\',        label:\'Login\' },
      ];
      window.finIdx = 0;
      const mainImg  = document.getElementById(\'fin-main-img\');
      const mainLbl  = document.getElementById(\'fin-main-label\');
      const lbImg    = document.getElementById(\'fin-lb-img\');
      const lbLbl    = document.getElementById(\'fin-lb-label\');
      const lightbox = document.getElementById(\'fin-lightbox\');
      const thumbsEl = document.getElementById(\'fin-thumbs\');
      slides.forEach((s,i) => {
        const th = document.createElement(\'img\');
        th.src=s.src; th.alt=s.label; th.title=s.label; th.dataset.i=i;
        th.style.cssText=\'height:56px;aspect-ratio:16/9;object-fit:cover;object-position:top;border-radius:4px;cursor:pointer;border:2px solid transparent;flex-shrink:0;transition:border-color 0.2s,opacity 0.2s;opacity:0.55;\';
        th.onclick=()=>finSet(i); thumbsEl.appendChild(th);
      });
      function finSet(i) {
        window.finIdx=(i+slides.length)%slides.length;
        const s=slides[window.finIdx];
        mainImg.style.opacity=\'0\';
        setTimeout(()=>{ mainImg.src=s.src; mainImg.style.opacity=\'1\'; },150);
        mainLbl.textContent=s.label;
        if(lightbox.style.display===\'flex\'){ lbImg.src=s.src; lbLbl.textContent=s.label; }
        thumbsEl.querySelectorAll(\'img\').forEach((th,j)=>{ th.style.borderColor=j===window.finIdx?\'var(--accent)\':\'transparent\'; th.style.opacity=j===window.finIdx?\'1\':\'0.55\'; });
        const act=thumbsEl.querySelectorAll(\'img\')[window.finIdx]; if(act) act.scrollIntoView({behavior:\'smooth\',inline:\'center\',block:\'nearest\'});
      }
      window.finNav=function(d){ finSet(window.finIdx+d); };
      window.finOpenLightbox=function(i){ finSet(i); lbImg.src=slides[window.finIdx].src; lbLbl.textContent=slides[window.finIdx].label; lightbox.style.display=\'flex\'; document.body.style.overflow=\'hidden\'; };
      window.finCloseLightbox=function(){ lightbox.style.display=\'none\'; document.body.style.overflow=\'\'; };
      document.addEventListener(\'keydown\',e=>{ if(lightbox.style.display!==\'flex\') return; if(e.key===\'ArrowLeft\') finNav(-1); if(e.key===\'ArrowRight\') finNav(1); if(e.key===\'Escape\') finCloseLightbox(); });
      finSet(0);
    })();
    </script>'''

# ── Replacements ──────────────────────────────────────────────────────────────

# 1. ASD: replace from <!-- SCREENSHOTS GALLERY --> up to (but not including) <!-- stack pills -->
asd_pattern = r'<!-- SCREENSHOTS GALLERY -->.*?(?=\s*<!-- stack pills -->)'
html, n = re.subn(asd_pattern, asd_carousel, html, flags=re.DOTALL)
print(f'ASD gallery replacements: {n}')

# 2. Finance: replace from <!-- GALLERY (outside hero card --> up to (not including) <!-- stack pills
fin_pattern = r'<!-- GALLERY \(outside hero card, like ASD\) -->.*?(?=\s*<!-- stack pills -->)'
html, n = re.subn(fin_pattern, fin_carousel, html, flags=re.DOTALL)
print(f'Finance gallery replacements: {n}')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Done!')
