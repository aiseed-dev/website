# 実例 1 — 1 人 + AI で SaaS 一式を 8 秒で組み立てる

第 11 章「1人+AIで作る、新しい仕事の単位」の主張を裏付ける。

## 章のどの主張に対応するか

第 11 章は、**それまでの 10 章で身につけた道具をひとりが使えると何ができるか**
の総まとめだった。具体例として「個人事業主の月次」「農家の AI」
「1 人スタートアップ」の 3 つを挙げた。

このフォルダは **3 つ目「1 人スタートアップ」を実演する** ─
架空の SaaS「Mochi.ai(古民家のための AI 管理人)」の事業立ち上げに必要な
成果物を **1 つの Python コマンドで丸ごと生成** する。

## やること

`build_all.py` 1 ファイルが、以下を **約 8 秒で全部生成**:

1. **ランディングサイト 4 ページ**(章 07 の道具)
   - `index.html` ─ サービス紹介
   - `pricing.html` ─ 料金表
   - `privacy.html` ─ プライバシーポリシー
   - `about.html` ─ 会社情報
2. **月次売上レポート**(章 02 + 04 + 05 の道具)
   - `sales.csv` を読んで集計
   - Markdown レポート + A4 PDF レポートを生成
3. **投資家ピッチ**(章 03 の道具)
   - Marp 互換 Markdown(`pitch-deck.md`)
   - HTML スライド(`pitch-deck.html`)
4. **システム構成図**(章 03 の道具)
   - Mermaid 入りの Markdown(GitHub / Notion でレンダリング)

入力ソースの合計はわずか **5 KB(Markdown 4 枚 + CSV 1 枚)**。
出力は **278 KB / 9 ファイル** ── **顧客に提示できる成果物の集合体**。

## 構成

```
example-1/
├── README.md
├── build_all.py        ── 全成果物を生成する 1 ファイル(約 230 行)
├── Makefile
├── results.md
├── sales.csv           ── 月次売上の入力データ
├── site/               ── サイトのソース Markdown
│   ├── index.md
│   ├── pricing.md
│   ├── privacy.md
│   └── about.md
└── out/                ── 生成物(全 9 ファイル)
    ├── site/{index,pricing,privacy,about}.html
    ├── monthly-report.md
    ├── monthly-report.pdf      ── A4 PDF、印刷可
    ├── pitch-deck.md           ── Marp 互換
    ├── pitch-deck.html
    └── architecture.md         ── Mermaid 入り
```

## 実行

```bash
pip install pandas markdown-it-py weasyprint
sudo apt install fonts-noto-cjk
make clean && make all
```

## なぜこれが「実例」になるのか

普通、「SaaS をローンチする」と言えば:

- フロントエンド開発: React + Next.js で **3 ヶ月**
- バックエンド開発: Node + Postgres で **2 ヶ月**
- デザイナー: Figma + ブランディング **1 ヶ月**
- マーケ: ランディングコピー + ピッチ作成 **1 ヶ月**
- 経理ツール導入: freee セットアップ + テンプレ **1 週間**
- 法務: 利用規約・プライバシー作成 **2 週間**

合計 **半年 + 数千万円**。

このフォルダはそれを **8 秒** で再現する(架空の規模で、ごく最小限の
中身ではあるが):

- フロント: Markdown 4 枚 → HTML(章 07)
- 月次売上: CSV → Markdown + PDF(章 02・04・05)
- ピッチ: Markdown + Marp(章 03)
- 構成図: Mermaid テキスト(章 03)

**1 人が、Markdown と Python と Claude だけで、ここまでのアセットを持てる**。
ここに API 実装(FastAPI 1 ファイル)を足し、cron で月次レポートを毎月
自動配信し、Claude に LINE 返信を下書きさせる ── これで **1 人 SaaS の
最小フル装備**になる。

これが、シリーズ全体の結論「**仕事の最小単位は、1 人 + AI**」の最小実演。

## サンプル出力(`out/monthly-report.md` 抜粋)

```markdown
# Mochi.ai 月次レポート — 2026-04

## サマリ

| 項目 | 値 |
|------|-----|
| 新規契約数 | 13 件 |
| MRR(月次経常収益) | **23,740 円** |
| 平均単価 | 1,826 円 |

## プラン別

| プラン | 契約数 | 売上 |
|--------|-------|------|
| ライト | 8 | 7,840 円 |
| スタンダード | 3 | 5,940 円 |
| プロ | 2 | 9,960 円 |

## コスト

| 項目 | 月額 |
|------|------|
| Cloudflare Pages | 0 円(無料枠内) |
| Cloudflare R2(センサデータ) | 約 200 円 |
| Claude Pro | 約 3,000 円 |
| Claude API | 約 2,000 円 |
| LINE Messaging API | 0 円(無料枠内) |
| ドメイン | 月割 100 円 |
| **合計** | **約 5,300 円** |
```

これを **来月もそのまま `make all` で再生成**できる。
人間が触るのは `sales.csv` だけ。

## 生成にかかった時間

| 工程 | 時間 |
|------|------|
| サイト 4 ページ HTML 化 | 1 ms |
| 月次レポート Markdown 生成 | 5 ms |
| 月次レポート PDF レンダリング (WeasyPrint) | 約 7,800 ms |
| ピッチ Markdown + HTML | 1 ms |
| 構成図 Markdown | < 1 ms |
| **合計** | **約 8,000 ms(8 秒)** |

PDF 生成だけが支配的。残りは数 ms。

## 関連する章の例

- [第 07 章 example-1](/ai-native-ways/web/example-1/): Markdown → HTML サイト
- [第 02 章 example-1](/ai-native-ways/data-formats/example-1/): pandas で集計
- [第 03 章 example-1](/ai-native-ways/design/example-1/): Mermaid 図
- [第 05 章 example-1](/ai-native-ways/office-replacement/example-1/): 月次レポート

このフォルダは、それらを **1 つに束ねた**形になっている。
