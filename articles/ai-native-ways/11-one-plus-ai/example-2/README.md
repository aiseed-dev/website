# 実例 2 — 個人事業主の月次クロージングを 1 コマンドで

第 11 章「1 人 + AI で作る、新しい仕事の単位」の **2 番目の角度**:
**個人事業主の月次フロー**(章本文の 3 つの具体例の 1 つ目)。

## 章のどの主張に対応するか

> A さんは、コンサルティング業務をやっている。月末に何が起きるか。
>
> **請求書作成**: Claude が顧客マスタ(CSV)を読んで、各顧客への請求書 PDF を生成する。
> **経費精算**: 領収書の写真を Claude に渡せば、テキスト化して仕分けし、CSV に整理する。
> **月次報告**: 売上データと経費データから、Claude が Markdown で月次レポートを作る。
>
> これが、A さん一人で完結する。10 年前なら、経理担当・マーケティング担当・
> Web 制作会社・印刷会社、合わせて数人〜十数人が関わっていた仕事だ。

(章本文「具体例: 個人事業主の月次」より)

example-1 が「Mochi.ai SaaS の全成果物」、これは **コンサル業の月次クローズ**
を実演する。

## やること

入力(月初〜月末を CSV に貯めるだけ):

- `data/clients.csv` ── 顧客マスタ(4 社)
- `data/work_log.csv` ── 業務ログ(時間 × 単価、12 件)
- `data/expenses.csv` ── 経費(10 件)

`make all` 1 コマンドで:

1. **顧客ごとの請求書 PDF**(4 件、A4 1 枚)
2. **顧客ごとの請求書 Markdown**(後で編集できるように)
3. **月次サマリ Markdown + PDF**(売上・経費・利益)
4. **確定申告用の経費 CSV**(国税庁仕訳に近い形)
5. **`index.md`**(成果物一覧、自分用ナビ)

すべて **約 43 秒**(PDF レンダリング 4 件分が支配的)。

## 構成

```
example-2/
├── README.md
├── build_month.py        ── 月次クロージング(約 200 行)
├── Makefile
├── results.md
├── data/
│   ├── clients.csv
│   ├── work_log.csv
│   └── expenses.csv
└── out/2026-04/
    ├── index.md          ── 月次成果物のナビ
    ├── summary.md / summary.pdf  ── 自分用月次レポート
    ├── tax-expenses.csv  ── 確定申告用
    └── invoices/
        ├── INV-2026-04-A001.md / .pdf
        ├── INV-2026-04-A002.md / .pdf
        ├── INV-2026-04-A003.md / .pdf
        └── INV-2026-04-A004.md / .pdf
```

## 実行

```bash
pip install pandas jinja2 markdown-it-py weasyprint
sudo apt install fonts-noto-cjk
make clean && make all
```

## なぜこれが「実例」になるのか

10 年前の月次クロージングは:

1. 経理担当が会計ソフトに入力(2 時間)
2. 自分が請求書を Word で作る(顧客ごと、1 件 30 分 × 4 件 = 2 時間)
3. PDF にして印刷会社経由で送付(1 日かかる)
4. 月次レポートを Excel で作って Word に貼り直す(2 時間)
5. 確定申告用の整理(月末 2 時間 + 期末 半日)

**月 8〜10 時間**。経理代行を雇えば月 3〜5 万円。

これが **`make all` で 43 秒**。

- 入力は CSV 3 つ(月の途中で書き溜めれば済む)
- 出力は **顧客提示用 / 自分用 / 税理士用** の 3 種類
- すべて Git でバージョン管理
- 来月も再来月も、CSV を更新して `make all` のみ

これが章で言う「**創業者 1 人 + Claude + 必要に応じて時間契約の専門家**」の
**会計サイド** の最小実演。

## 数字(このフォルダの結果)

```
=== 月次クロージング完了 (2026-04) ===
  実行時間: 42.76 秒

  顧客 : 4 社
  業務 : 12 件
  経費 : 10 件

  売上(税込): 414,700 円
  経費       : 79,700 円
  利益       : 297,299 円  (利益率 78.9%)

  生成ファイル: 12 個 / 1,428.8 KB
```

## 来月の運用

```bash
# 1. 業務ログを書き溜める(週 1 で更新)
$EDITOR data/work_log.csv

# 2. 領収書を CSV に(Claude に画像から起こさせる)
$EDITOR data/expenses.csv

# 3. 月末に走らせる
make clean && make all

# 4. PDF を顧客にメール、CSV を税理士に共有
```

これで月次クロージング完了。

## 関連する例

- [第 02 章 example-2](/ai-native-ways/data-formats/example-2/) で扱った
  CSV ⇄ JSON ⇄ YAML はそのまま流用できる
- [第 05 章 example-2](/ai-native-ways/office-replacement/example-2/)
  の差し込み印刷は、このフォルダの請求書生成と同じ仕組み
- [第 11 章 example-1](/ai-native-ways/one-plus-ai/example-1/)
  の Mochi.ai SaaS 例と組み合わせれば、**B2B + B2C 両方の月次が動く**
