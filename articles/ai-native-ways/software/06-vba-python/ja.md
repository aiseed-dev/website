---
slug: vba-python
number: "06"
part: "1"
title: VBA を Python に移す ── Excel マクロを AI と書き直す
subtitle: セキュリティに脆弱な業務マクロを、現行を正解器に Python へ ── Excel はそのまま、AI が超得意な言語で書き直す
description: 第5章の最初の実例。たいていの会社の足元にある Excel の VBA マクロ ── セキュリティに脆弱で、作者も去り誰も直せない ── を、AI と Python に移す。Python は AI 自身が書かれている言語で、AI が超得意。Polars と openpyxl で Excel(.xlsx)はそのまま読み書き・編集できる(ODF を使う LibreOffice より、OOXML を保つ OnlyOffice が噛み合う)。現行マクロを正解器に、入出力を見比べて一本ずつ。
date: 2026.06.30
label: Introduction 6
title_html: 脆弱な VBA を、<br>AI 得意の <span class="accent">Python</span> へ。
prev_slug: customer-codev
prev_title: "顧客がAIと協働して開発する時代"
next_slug: website
next_title: "Webサイトを作る ── AI と対話して"
---

# VBA を Python に移す ── Excel マクロを AI と書き直す

第5章で見たとおり、個人は OSS と AI で、自分の道具を作れる。最初の実例は、
たいていの会社の足元にある ── **Excel の VBA マクロ**だ。長年の業務がそこ
に書かれ、作った人はもういない、直せる人もいない。これを AI と **Python**
に移す。

## なぜ、早急に Python へ移すのか

- **VBA はセキュリティに脆弱だ**。マクロは古くからマルウェアの主要な侵入口
  で、メール添付の Excel マクロは攻撃の定番だった。業務の VBA を抱え続ける
  こと自体がリスクで、**早急に移すべき**だ。
- **作者が去ると、ブラックボックスになる**。VBA は Excel に縛られ、中身が
  分からないまま動き続け、誰も直せない。
- **Python は、AI が超得意だ**。AI 自身が Python で書かれ、いまや **AI が
  AI を Python で書いている**。だから Python を書かせれば、最も精度が高い。
  しかも、読めて、テストでき、どこでも動く。

## Excel はやめなくていい ── Polars と openpyxl

「Python に移す」と聞くと、Excel を捨てるのかと身構える。だが違う。Python
には **Polars** と **openpyxl** があり、**Excel ファイル(.xlsx)をそのまま
読み書き・編集できる**。人は今までどおり Excel で入力し、結果を読む ──
処理(機械の仕事)だけを、VBA から Python に移す。

```python
# 例: VBA の集計マクロを Python(Polars)に
import polars as pl
df = pl.read_excel("売上.xlsx")
df.group_by("部門").agg(pl.col("売上").sum()).write_excel("部門集計.xlsx")
```

Polars も openpyxl も、**人間にとっても扱いやすい**。API は素直で、コード
は読みやすい ── VBA のブラックボックスと違い、後から人が読んで直せる。

一点、注意がある。**LibreOffice や OpenOffice は ODF 形式(.ods)**で保存
するため、Polars や openpyxl では **扱いづらい**。だから、表計算ソフトその
ものを置き換えるなら、Microsoft と同じ **OOXML(.xlsx)** を保つ
**OnlyOffice** を選ぶ ── Python の道具とそのまま噛み合う(自立編 第4章の
文書基盤で扱う)。

## 進め方 ── 現行を正解器にする

一度に全部ではない。マクロ一本ずつ、**現行を「答え合わせの相手(正解器)」**
にして移す。

1. 既存マクロを AI に渡し、**何をしているかを説明させる**(仕様の言語化)
2. 同じ入出力の **Python を AI に書かせる**
3. 同じ Excel に対して、旧マクロと新 Python を流し、**結果を見比べる**
4. 合うまで直し、合ったら切り替える

現行と新版の出力が一致したら、古いマクロを外す ── 止めずに、一本ずつ。
分からない所は、その場で AI に聞く。これは第5章の作り方そのものだ。

## まとめ

- **脆弱な VBA は、早急に Python へ** ── セキュリティの観点でも待ったなし
- **Excel はそのまま** ── Polars・openpyxl が .xlsx を扱う。置き換えるなら、
  ODF ではなく OOXML を保つ OnlyOffice
- **現行を正解器に**、入出力を見比べて一本ずつ移す
- **Python は AI が超得意** ── AI 自身が Python で書かれている

次章では、もう一つの実例 ── **Web サイト**を AI と対話して作る。

---

## 関連記事

- [第5章: 顧客がAIと協働して開発する時代](/ai-native-ways/software/customer-codev/)
- [自立編 第4章: 文書を取り戻す ── OnlyOffice Docs](/ai-native-ways/software/documents/)
- [親シリーズ第2章: 処理を書く ── AIにPythonで書いてもらう](/ai-native-ways/python/)
- [親シリーズ第7章: 業務システムと付き合う ── 並行稼働で書き換える](/ai-native-ways/business-systems/)
