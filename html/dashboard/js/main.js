// エントリポイント: 読み込み時に静的 JSON を 1 回 fetch → 描画。
// フレームワーク・バンドラ・状態管理なし（仕様 §4 フロントエンド）。
import { renderChokepointSection, renderLegend } from './render.js';

const DATA_URL = 'data/dashboard.json';

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
  if (node && iso) node.textContent = `最終生成: ${iso.replace('T', ' ').replace('+00:00', ' UTC')}`;
}

async function load() {
  const main = document.getElementById('dashboard');
  try {
    const res = await fetch(DATA_URL, { cache: 'no-cache' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    main.textContent = '';
    for (const cp of data.chokepoints) {
      main.appendChild(renderChokepointSection(cp));
    }
    renderGeneratedAt(data.generated_at);
  } catch (err) {
    main.innerHTML =
      `<p class="dash-error">データを読み込めませんでした（${String(err.message || err)}）。` +
      `<br><code>data/dashboard.json</code> が生成されているか確認してください。</p>`;
  }
}

document.getElementById('legend').appendChild(renderLegend());
setupThemeToggle();
load();
