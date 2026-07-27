// 構造指標ダッシュボード (Insights) のエントリポイント。
// フロント部品は物理量ダッシュボード (/dashboard/js/) を再利用し、複製しない
// (仕様 docs/plan/insights-dashboard-spec.md §1)。
// このファイル固有の仕事は2つだけ: themes 構造の JSON を読むことと、
// 各カードに関連記事リンクを足すこと。
import { renderChokepointSection, renderLegend } from '../../js/render.js';

const DATA_URL = 'data/structural.json';

function setupThemeToggle() {
  const btn = document.getElementById('theme-toggle');
  if (!btn) return;
  btn.addEventListener('click', () => {
    const root = document.documentElement;
    const current = root.getAttribute('data-theme')
      || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    const next = current === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('aiseed-theme', next); } catch (e) {}
  });
}

function renderGeneratedAt(iso) {
  const node = document.getElementById('generated-at');
  if (node && iso) node.textContent = `最終更新: ${iso.replace('T', ' ').replace('+00:00', ' UTC')}`;
}

// 関連記事リンクをカード末尾に追加 (renderIndicatorCard は article を知らない)
function appendArticleLinks(theme) {
  for (const ind of theme.indicators) {
    if (!ind.article) continue;
    const card = document.getElementById(`indicator-${ind.id}`);
    if (!card) continue;
    const p = document.createElement('p');
    p.className = 'card__article';
    const a = document.createElement('a');
    a.href = ind.article.href;
    a.textContent = `→ 記事: ${ind.article.label}`;
    p.appendChild(a);
    card.appendChild(p);
  }
}

async function load() {
  const main = document.getElementById('dashboard');
  try {
    const res = await fetch(DATA_URL, { cache: 'no-cache' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    main.textContent = '';
    for (const theme of data.themes) {
      main.appendChild(renderChokepointSection(theme));
      appendArticleLinks(theme);
    }
    renderGeneratedAt(data.generated_at);
  } catch (err) {
    main.innerHTML =
      `<p class="dash-error">データを読み込めませんでした（${String(err.message || err)}）。` +
      `<br><code>data/structural.json</code> を確認してください。</p>`;
  }
}

document.getElementById('legend').appendChild(renderLegend());
setupThemeToggle();
load();
