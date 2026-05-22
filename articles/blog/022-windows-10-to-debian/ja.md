---
slug: windows-10-to-debian
title: Windows 10 の PC がある人へ ── 今、Debian を試す
subtitle: Microsoft が「もう面倒を見ない」と言った今こそ、Debian + AI の時
date: 2026.05.22
description: 2025 年 10 月に Windows 10 のサポートが終了した。Windows 11 に対応していない PC が世界中で数億台ある。しかしハードウェアは何も壊れていない。同じハードウェアで Debian は普通に動く ── むしろ古い PC こそ Linux の方が向いている。「Linux は難しい」という常識は、AI 時代に二重に逆転した: ひとつは AI がコマンドと相性がいいこと、もうひとつは Flathub が普段使いアプリの GUI 導入を Microsoft Store より整った形で提供していること。AI が横にいる今、Linux のコマンドはもう難しくない。Debian を試すなら今が時。
lang: ja
label: Blog
category: 構造分析ノート
---

# Windows 10 の PC がある人へ ── 今、Debian を試す

2025 年 10 月、Microsoft は Windows 10 のサポートを終了した。ESU で 1 年延ばしている人、何もせずに使い続けている人 ── その先に、**買い替え以外の道**がある。

家にある古い PC に「Windows 11 に対応していません」と表示される人が、世界中で数億人いる。第 8 世代より前の CPU、TPM 2.0 非搭載 ── Microsoft の基準では「もう使えない」ことになっている。

しかし、ハードウェアは何も壊れていない。同じハードウェアで、**Debian は普通に動く**。むしろ軽快に動く。古い PC こそ、Linux の方が向いている。

## Debian という選択

Debian は、30 年以上続いている Linux ディストリビューションのひとつ。商業ベンダーの都合ではなく、世界中のボランティアによって維持されている。だから「サポートを切る商業判断」が起きにくい。

サポート切れの Windows 10 が動いていたハードウェアで、Debian 13 は普通に動く。Wi-Fi、画面、音、サスペンド ── 多くの場合、インストール後に追加設定はほとんど要らない。

## 「Linux は難しい」は、AI 時代に逆転した

Linux は難しい、という印象は根強い。コマンドを打つ黒い画面、聞いたことのない用語、Windows のような直感的な操作ができない ── これは、**人間が一人で覚える前提**の話だった。

しかし、2026 年の今、状況は二つの大きな変化で逆転している。

### ひとつ目 ── AI は「コマンド」と相性がいい

意外に思われるかもしれないが、Claude のような AI は **Windows の GUI 操作を教えるのが苦手で、Linux のコマンドを教えるのが得意** だ。

GUI を言葉で説明するのは難しい。「設定の左メニューの上から 3 番目」はバージョンで変わる。「歯車のアイコンをクリック」は画面のどこにあるかで違う。スクリーンショットを撮っても、AI が指せるのは大まかな場所だけ。

コマンドは違う。テキストで完結する。Claude が書いたコマンドを、あなたがコピーして貼り付ければ、そのまま動く。エラーが出ても、その文字列をそのまま Claude に渡せば、原因を特定できる。

**Linux の「コマンドが多い」という弱点は、AI が横にいる時代には強みに変わった**。

### ふたつ目 ── Flathub

普段使いのアプリのインストールは、コマンドさえ要らなくなった。[flathub.org](https://flathub.org) を開けば、Linux で動くアプリが一つの場所に並んでいる。

| カテゴリ | アプリ |
|---|---|
| ブラウザ | Firefox、Google Chrome、Chromium、Brave |
| オフィス | ONLYOFFICE Desktop Editors、LibreOffice |
| コミュニケーション | Zoom、Slack、Discord、Element、Signal |
| メディア | Spotify、VLC、Audacity、OBS Studio |
| クリエイティブ | GIMP、Inkscape、Krita、Blender、darktable |
| 開発 | Zed、VSCodium、Visual Studio Code、PyCharm、IntelliJ IDEA、Android Studio |
| ユーティリティ | Bitwarden、Joplin、Obsidian、Thunderbird |

Windows で言えば、Microsoft Store のような場所だ。しかし、Microsoft Store より **むしろ揃っている**。

**Microsoft Store には Google Chrome が無い**。Microsoft が自社の Edge を優遇しているため、競合ブラウザを排除している。Chrome をインストールしたいユーザーは、Microsoft Store で検索しても見つけられず、別の方法で探すことになる。一方、Flathub には Chrome も Firefox も Brave も並んでいる。**ベンダーの都合で並びが歪められない**。

**Microsoft Store は広告を表示する**。アプリを探しているのに、関係ない有料アプリが「おすすめ」として割り込んでくる。Flathub には広告がない。

**Microsoft Store は Microsoft アカウントへのサインインを求める場面が多い**。Flathub はアカウント不要。何も登録せずに、好きなアプリを入れられる。

つまり、現代の Linux は **二層構造** になっている。

- **日常のアプリ**: Flathub から GUI で入れる。コマンドは要らない。
- **設定や開発**: コマンドで操作する。ここでこそ AI が真価を発揮する。

この二層が、AI 時代の Linux の強さだ。Windows はどちらも中途半端 ── GUI は深い設定までは届かず、PowerShell のコマンドは AI にとっても扱いにくい。

## Claude と一緒に学ぶ

このサイトには、Claude を横に置きながら学ぶための二つの教科書がある。

[**Claude と一緒に学ぶ Debian**](/claude-debian/) は、Debian への移行を Claude との対話で進めるための 23 章の教科書だ。何を Claude に伝えるか、どう環境情報を取り出すか、ログをどう渡すか、詰まったときに何を試すか ── これらは、Linux の知識そのものよりも、**AI を使って学ぶための作法** に近い。

[**AI ネイティブな仕事の作法**](/ai-native-ways/) は、Debian に移った先で何をするかを書いている。Excel の VBA を Python に、Word を Markdown に、CSV を JSON や SQLite に ── AI が同僚になる時代の道具立てを、14 章で整理している。

一度この作法を身につければ、Debian だけでなく、**この先 AI と一緒に何かを学ぶ・作るときの基礎** になる。

## 今が、Debian を始める時

「Windows 10 が止まったから仕方なく」ではない。「Debian + AI + Flathub が揃った今だから、ちょうど良い」だ。

3 年前なら違った。Linux のコマンドは難しく、Flathub の品揃えも今ほどではなく、AI も無かった。**この三つが同時に整ったのは、2026 年の今だ**。

PC の廃棄はいつでもできる。買い替えもいつでもできる。しかし、**「今ある PC を、もう一段使い倒す」入口は、Windows 10 サポート終了という今この瞬間に開いている**。世界中で同じことが同時に起きれば、膨大な電子ゴミになり、新しい PC を作るための鉱物資源と化石燃料を消費する ── その流れに加わるかどうかも、今、選べる。

Microsoft が「もう面倒を見ない」と言った日は、ハードウェアの寿命ではない。
AI が横にいる今、Linux のコマンドはもう、難しくない。

[Claude と一緒に学ぶ Debian →](/claude-debian/)

---

*関連記事: [「Windows が壊れていく」── ナデラが Windows を見限った構造](/blog/windows-breaking-down/)*

*関連記事: [「それでも Windows と Office を使い続けますか?」── 詳細な構造分析と一次情報・参考文献](/blog/windows-office-facts/)*

*関連記事: [「日本の Windows 災害リスク」── 一斉サポート終了の社会的インパクト](/blog/japan-windows-disaster-risk/)*

*関連記事: [「AI 時代には『特化したエンジニアになれ』は構造を取り違えている」── ソフトウェア工学からリベラルアーツへの基盤転換](/blog/software-three-transitions/)*
