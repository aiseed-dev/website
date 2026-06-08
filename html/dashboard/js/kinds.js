// kind（指標の種別）と acquisition（取得方法）のメタ情報を 1 か所に集約。
// UI 上の色分けと日本語ラベルはここだけ見ればよい（仕様 §2 の表に対応）。

export const KIND_META = {
  price:    { label: '価格', en: 'price',    desc: '世界需給が決める下流の読み取り値' },
  flow:     { label: '流れ', en: 'flow',     desc: '量・経路・割引。制御が行使される層' },
  clock:    { label: '時計', en: 'clock',    desc: 'ゼロや期限に向かうカウントダウン' },
  stock:    { label: '在庫', en: 'stock',    desc: '在庫日数など' },
  constant: { label: '定数', en: 'constant', desc: '依存率などほぼ動かない構造の事実' },
};

export const ACQUISITION_META = {
  auto:    { label: '自動', desc: 'Python fetcher が API/スクレイプで取得' },
  derived: { label: '計算', desc: '他指標から計算（スプレッド・比率・残り日数）' },
  manual:  { label: '手入力', desc: 'プログラム的な出所が無い残余（出所が現れ次第 auto へ昇格）' },
};

export function kindLabel(kind) {
  return (KIND_META[kind] || { label: kind }).label;
}
