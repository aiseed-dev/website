// renderSparkline(series) — 手書きインライン SVG（チャートライブラリなし）。
// 数値系列のみ対象。点が 2 つ未満なら null（呼び出し側で非表示）。

const W = 120;
const H = 32;
const PAD = 2;

function numericPoints(series) {
  return series.filter((p) => typeof p.value === 'number' && isFinite(p.value));
}

// 系列を入力に SVG 文字列を返す（実 DOM ではなく軽量に文字列で組む）。
export function renderSparkline(series) {
  const pts = numericPoints(series);
  if (pts.length < 2) return null;

  const values = pts.map((p) => p.value);
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max - min || 1;

  const x = (i) => PAD + (i * (W - 2 * PAD)) / (pts.length - 1);
  const y = (v) => PAD + (H - 2 * PAD) * (1 - (v - min) / span);

  const d = pts.map((p, i) => `${i ? 'L' : 'M'}${x(i).toFixed(1)},${y(p.value).toFixed(1)}`).join(' ');
  const last = pts[pts.length - 1];
  const cx = x(pts.length - 1).toFixed(1);
  const cy = y(last.value).toFixed(1);
  const trendUp = last.value >= pts[0].value;

  return (
    `<svg class="sparkline ${trendUp ? 'spark-up' : 'spark-down'}" ` +
    `viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" ` +
    `role="img" aria-label="推移 ${pts.length} 点">` +
    `<path d="${d}" fill="none" stroke="currentColor" stroke-width="1.5" ` +
    `stroke-linecap="round" stroke-linejoin="round"/>` +
    `<circle cx="${cx}" cy="${cy}" r="2.2" fill="currentColor"/>` +
    `</svg>`
  );
}
