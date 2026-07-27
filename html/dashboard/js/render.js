// 指標カード / 隘路セクションの描画（仕様 §4 フロント部品）。
// 各部品は入力データだけで完結する。テキストは実 DOM（検索に拾われ・選択でき・
// 記事から id でリンクできる）。
import { kindBadge, acquisitionTag } from './badges.js';
import { renderSparkline } from './sparkline.js';
import { renderClockGauge } from './gauge.js';
import { KIND_META } from './kinds.js';

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;
  return node;
}

function formatValue(value) {
  if (typeof value === 'number') {
    const abs = Math.abs(value);
    const digits = abs !== 0 && abs < 10 ? 2 : abs < 100 ? 1 : 0;
    return value.toLocaleString('ja-JP', { maximumFractionDigits: digits });
  }
  return String(value); // 状態文字列（開/制限 など）
}

// renderIndicatorCard(indicator) → 要素: 値・単位・観測日・出所・kind バッジ
export function renderIndicatorCard(ind) {
  const card = el('article', `card kind-${ind.kind}`);
  card.id = `indicator-${ind.id}`; // 記事から #indicator-<id> でリンク可能

  const head = el('div', 'card__head');
  head.appendChild(el('h3', 'card__name', ind.name_ja));
  const badges = el('div', 'card__badges');
  badges.appendChild(kindBadge(ind.kind));
  badges.appendChild(acquisitionTag(ind.acquisition));
  head.appendChild(badges);
  card.appendChild(head);

  const latest = ind.series.length ? ind.series[ind.series.length - 1] : null;

  // 値 + 単位（観測が無ければ「観測待ち」）
  const valueRow = el('div', 'card__value');
  if (latest != null && latest.value !== null && latest.value !== '') {
    valueRow.appendChild(el('span', 'card__num', formatValue(latest.value)));
    if (ind.unit) valueRow.appendChild(el('span', 'card__unit', ind.unit));
  } else {
    valueRow.appendChild(el('span', 'card__pending', '観測待ち'));
    if (ind.unit) valueRow.appendChild(el('span', 'card__unit', ind.unit));
  }
  card.appendChild(valueRow);

  // 時計はゲージ、その他は数値系列があればスパークライン
  const gauge = ind.kind === 'clock' ? renderClockGauge(ind) : null;
  if (gauge) {
    const g = el('div', 'card__gauge');
    g.innerHTML = gauge;
    card.appendChild(g);
  } else {
    const spark = renderSparkline(ind.series);
    if (spark) {
      const s = el('div', 'card__spark');
      s.innerHTML = spark;
      card.appendChild(s);
    }
  }

  // 観測日 ・ 出所
  const meta = el('div', 'card__meta');
  if (latest) {
    meta.appendChild(el('span', 'card__date', `観測 ${latest.date}`));
    meta.appendChild(el('span', 'card__source', `出所 ${latest.source}`));
  } else {
    meta.appendChild(el('span', 'card__source', `出所 ${ind.source}`));
  }
  card.appendChild(meta);

  if (ind.note) card.appendChild(el('p', 'card__note', ind.note));
  return card;
}

// renderChokepointSection(chokepoint) → 隘路の見出し + カードグリッド
export function renderChokepointSection(cp) {
  const section = el('section', 'chokepoint');
  section.id = `chokepoint-${cp.id}`;

  const header = el('div', 'chokepoint__head');
  header.appendChild(el('h2', 'chokepoint__title', cp.name_ja));
  header.appendChild(el('span', 'chokepoint__en', cp.name_en));
  section.appendChild(header);

  const grid = el('div', 'card-grid');
  for (const ind of cp.indicators) grid.appendChild(renderIndicatorCard(ind));
  section.appendChild(grid);
  return section;
}

// 凡例（kind の色分け）
export function renderLegend() {
  const frag = document.createDocumentFragment();
  for (const [kind, meta] of Object.entries(KIND_META)) {
    const item = el('span', `legend-item kind-${kind}`);
    item.appendChild(el('span', 'legend-swatch'));
    item.appendChild(el('span', 'legend-label', `${meta.label}`));
    item.title = meta.desc;
    frag.appendChild(item);
  }
  return frag;
}
