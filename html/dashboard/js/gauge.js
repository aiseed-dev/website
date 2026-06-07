// renderClockGauge(indicator) — threshold 付きの残り日数 / ゲージ（仕様 §4）。
// 結論は書かない。物理的に閾値（→0・期日）を示すだけ。

// カウントダウン（target_date あり）か、ゼロに向かう残高 clock を描く。
// 返り値は HTML 文字列。該当しなければ null。
export function renderClockGauge(indicator) {
  const latest = indicator.series.length ? indicator.series[indicator.series.length - 1] : null;

  // 1) 期日カウントダウン（残り日数）
  if (indicator.target_date && latest && typeof latest.value === 'number') {
    const days = latest.value;
    const label = indicator.threshold ? indicator.threshold.label : indicator.target_date;
    const overdue = days < 0;
    return (
      `<div class="gauge gauge-countdown ${overdue ? 'is-overdue' : ''}">` +
      `<span class="gauge-num">${overdue ? '経過' : days}</span>` +
      `<span class="gauge-unit">${overdue ? `${Math.abs(days)}日` : '日'}</span>` +
      `<span class="gauge-target">→ ${label}</span>` +
      `</div>`
    );
  }

  // 2) ゼロに向かう残高（threshold.direction === 'down'）
  if (indicator.threshold && indicator.threshold.direction === 'down' && latest &&
      typeof latest.value === 'number') {
    const start = indicator.series.find((p) => typeof p.value === 'number');
    const baseline = start ? start.value : latest.value;
    const span = baseline - indicator.threshold.value || 1;
    const remain = Math.max(0, Math.min(1, (latest.value - indicator.threshold.value) / span));
    return (
      `<div class="gauge gauge-depletion">` +
      `<div class="gauge-bar"><div class="gauge-bar__fill" style="width:${(remain * 100).toFixed(0)}%"></div></div>` +
      `<span class="gauge-target">→ ${indicator.threshold.label}（${indicator.threshold.value}${indicator.unit}）</span>` +
      `</div>`
    );
  }

  return null;
}
