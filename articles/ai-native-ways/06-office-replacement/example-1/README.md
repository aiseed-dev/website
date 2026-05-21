# 実例 1 — 月次報告書を CSV から Markdown + Marp で 30 秒で作る

第 05 章「事務処理を変える ── Officeから離れる現実的な道筋」の主張を裏付ける。

## 章のどの主張に対応するか

> 事務職の月次報告書作成: Word + Excel + PowerPoint で **3 時間** →
> Markdown + CSV + Marp で **30 分**。**6 分の 1**。

(章本文「実例: 数字で見る」より)

実測 ── スクリプトのビルド時間は **約 8 秒**(Markdown 生成 7 ms + HTML 6 秒
+ PDF 2 秒)。来月以降、データ CSV を差し替えて `make all` だけで完了する。

## やること

1. **入力**: `data/sales.csv`(売上 30 件)+ `data/expenses.csv`(経費 13 件)
2. **生成**: `build_report.py` が pandas で集計して、表とコメントを埋め込んだ
   **Marp フォーマット** の Markdown 報告書 (`out/report.md`) を作る
3. **配布**: pandoc が同じ Markdown から:
   - **HTML** 版(社内 Wiki / メール添付用)
   - **PDF** 版(印刷 / 取引先送付用、A4 2 ページ)
4. **スライド**: `report.md` に Marp フロントマターが付いているので、
   `marp report.md -o slides.pdf` で **スライド版**にもなる(別途 marp-cli)

`make all` 一発。

## 構成

```
example-1/
├── README.md
├── build_report.py        ── CSV → Markdown 報告書(pandas + str.format)
├── Makefile               ── 全工程
├── results.md
├── data/
│   ├── sales.csv          ── 入力(売上)
│   └── expenses.csv       ── 入力(経費)
└── out/
    ├── report.md          ── 生成された Markdown 報告書(Marp 互換)
    ├── report.html        ── HTML 配布版(TOC 付き)
    └── report.pdf         ── PDF 配布版(A4 2 ページ)
```

## 実行

```bash
pip install pandas weasyprint
sudo apt install pandoc fonts-noto-cjk
make clean && make all
```

## なぜこれが「実例」になるのか

**月次報告は事務職の月初定型業務**。Word + Excel + PowerPoint だと:

1. Excel で売上・経費を集計(30 分)
2. 表と数字を Word にコピペ(20 分、書式調整で逆に時間が増える)
3. グラフを Excel で作って Word に画像で貼る(20 分)
4. 同じ内容を PowerPoint に書き直す(60 分)
5. 数字が間違っていて 4 つのファイルを直す(30 分)

合計 **3 時間**。これが毎月 12 回。**1 年で 36 時間**。

Markdown + Python だと:

1. CSV を差し替えて `make all`
2. 完了

**1 分かからない**。スクリプトは初回だけ Claude に書いてもらえばいい。
表の書式を直したいときも、`build_report.py` の Markdown テンプレを 1 行
直せば 12 ヶ月分にも遡及する。

しかも同じソースが **HTML / PDF / Marp スライド** に展開される。「Word の
表を PowerPoint に貼り直す」という事務作業そのものが消える。

これが章で言う「**事務処理は AI でもやれる簡単な仕事になる**」の最小実演。
