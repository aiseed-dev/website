---
slug: vba-python
number: "06"
part: "1"
title: VBA を Python に移す ── Excel マクロを AI と書き直す
subtitle: 作者が去って直せなくなった業務マクロを、現行を正解器に Python へ移す
description: 第5章の最初の実例。たいていの会社の足元にある Excel の VBA マクロ ── 作った人はもういない、直せる人もいない「ブラックボックス」を、AI と Python に移す。現行マクロを正解器にして、同じ入出力を見比べながら一本ずつ。表計算(人の入出力)は Excel のまま、処理(機械)は Python へ。読めて、テストでき、どこでも動くコードに変える。
date: 2026.06.30
label: Introduction 6
title_html: VBA の<span class="accent">ブラックボックス</span>を、<br>読める Python に。
prev_slug: customer-codev
prev_title: "顧客がAIと協働して開発する時代"
next_slug: website
next_title: "Webサイトを作る ── AI と対話して"
---

# VBA を Python に移す ── Excel マクロを AI と書き直す

第5章で見たとおり、顧客は AI と組んで自分で作れる。最初の実例は、たいてい
の会社の足元にある ── **Excel の VBA マクロ**だ。長年の業務がそこに書かれ、
作った人はもういない、直せる人もいない。これを AI と **Python** に移す。

## なぜ Python に移すのか

- **VBA は Excel に縛られる**。作者が去ると、誰も中身が分からない「ブラック
  ボックス」になりがちだ
- **Python は読めて、テストでき、どこでも動く**。AI が最も得意な言語の一つ
- **表計算(人の入出力)は Excel のまま、処理(機械)は Python へ** ── 役割で
  分ける(自立編のデータ基盤で詳しく扱う)

## 進め方 ── 現行を正解器にする

一度に全部ではない。マクロ一本ずつ、**現行を「答え合わせの相手(正解器)」**
にして移す。

1. 既存マクロを AI に渡し、**何をしているかを説明させる**(仕様の言語化)
2. 同じ入出力の **Python を AI に書かせる**
3. 同じ Excel に対して、旧マクロと新 Python を流し、**結果を見比べる**
4. 合うまで直し、合ったら切り替える

```python
# 例: VBA の集計マクロを Python(Polars)に
import polars as pl
df = pl.read_excel("売上.xlsx")
df.group_by("部門").agg(pl.col("売上").sum()).write_excel("部門集計.xlsx")
```

人は Excel で入れて読み、機械は Python で捌く。現行と新版の出力が一致したら、
古いマクロを外す ── 止めずに、一本ずつ。

## 対話で、少しずつ

仕様を最初から書き切る必要はない。**AI と対話しながら**、現行と見比べて直す。
分からない所は、その場で AI に聞く。これは第5章の作り方そのものだ。

## まとめ

- **VBA のブラックボックスを、読める Python に**
- **現行を正解器に**、入出力を見比べて一本ずつ移す
- **表計算は人の道具のまま、処理は機械(Python)へ**

次章では、もう一つの実例 ── **Web サイト**を AI と対話して作る。

---

## 関連記事

- [第5章: 顧客がAIと協働して開発する時代](/ai-native-ways/software/customer-codev/)
- [親シリーズ第2章: 処理を書く ── AIにPythonで書いてもらう](/ai-native-ways/python/)
- [親シリーズ第7章: 業務システムと付き合う ── 並行稼働で書き換える](/ai-native-ways/business-systems/)
