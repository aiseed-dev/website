// kindBadge(kind) — 価格/流れ/時計… の色分けバッジ（仕様 §4 フロント部品）。
import { KIND_META, ACQUISITION_META } from './kinds.js';

// 種別バッジ（DOM 要素を返す。色は CSS の .kind-<kind> が担う）。
export function kindBadge(kind) {
  const meta = KIND_META[kind] || { label: kind, desc: '' };
  const el = document.createElement('span');
  el.className = `badge kind-badge kind-${kind}`;
  el.textContent = meta.label;
  el.title = meta.desc;
  return el;
}

// 取得方法の小さなタグ（auto/derived/manual）。
export function acquisitionTag(acquisition) {
  const meta = ACQUISITION_META[acquisition] || { label: acquisition, desc: '' };
  const el = document.createElement('span');
  el.className = `tag acq-${acquisition}`;
  el.textContent = meta.label;
  el.title = meta.desc;
  return el;
}
