---
slug: windows-10-to-debian
title: Windows 10 の PC がある人へ ── Linuxをインストールする時代
subtitle: AI 時代には、Linux の方が使いやすい
date: 2026.05.22
description: 2025 年 10 月に Windows 10 のサポートが終了した。Windows 11 に対応していない PC が世界中で数億台ある。しかしハードウェアは何も壊れていない。同じハードウェアで Debian は普通に動く ── むしろ古い PC こそ Linux の方が向いている。「Linux は難しい」という常識は、AI 時代に二重に逆転した: ひとつは AI がコマンドと相性がいいこと、もうひとつは Flathub が普段使いアプリの GUI 導入を Microsoft Store より整った形で提供していること。AI が横にいる今、Linux のコマンドはもう難しくない。Debian を試すなら今が時。
lang: ja
label: Blog
category: 構造分析ノート
hero_image: IMG_3482.webp
---

# Windows 10 の PC がある人へ ── Linuxをインストールする時代

2025 年 10 月、Microsoft は Windows 10 のサポートを終了した。ESU で 1 年延ばしている人でも、個人の場合は残り 5 か月で切れる。法人は今年の10月に122ドル払い来年の10月に244ドル払って再来年の10月で完全に終わり。

Windows 11 に対応していないPCが、世界中で数億台ある。第 8 世代より前の CPU、TPM 2.0 非搭載、それがMicrosoft では「もう使えない」ことになっている。

一方で、2026年は新しいPCを買う最悪のタイミングだ。**Microsoft**自身が引き起こしたAIバブルによるメモリの大量需要で、メモリーやディスクの価格は過去1年で大幅に上昇している。

Microsoftは Copilot+ PC という新しいカテゴリを作り、NPU 40 TOPS という新しい足切りラインを設けている。Copilot+ PC だと 20 万円を超える価格になっている。

ただし、NPU を載せたところで、**AI の処理がデータセンターに集中する構造は何も変わらない**。Copilot の主要機能 (Word の下書き・Excel の関数生成・PowerPoint の要約・Outlook の返信案・エージェント) は依然として Azure / OpenAI のクラウドを呼んでいる。NPU が手元で動かすのは Recall や Studio Effects、ライブキャプション程度の周辺機能だけ。「エッジで AI が動く」というマーケティングとは裏腹に、AI バブルの本体である Azure データセンターへの依存は減らない。

しかも、高額な Copilot+ PC を購入しても、何年保証されるかもわからず、Linux を直にインストールできるかどうかもわからない。

今は、新しい PC を買わないのが最善の選択肢だ。その場合、Linuxという選択肢がある。

## Debian という選択

Linuxには、多くのディストリビューションがあるが、世界中のボランティアによって30 年以上維持されている Debian は、最も有力な候補の一つである。商業ベンダーの都合に影響されにくいからである。

Windows 10 が動いていたハードウェアであれば、Debian 13 は普通に動くはずだ。

## 「Linux は難しい」は、AI 時代に逆転した

Linux は難しい、という印象は根強い。コマンドを打つ黒い画面、聞いたことのない用語、Windows のような直感的な操作ができない ── これは、**人間が一人で覚える前提**の話だった。

しかし、2026 年の今、状況は二つの大きな変化で逆転している。

### ひとつ目 ── GUI での操作・設定の方が、AI には難しい

意外に思われるかもしれないが、Claude のような AI にとって、**GUI で何かを操作する・設定する手順を教えるほうが、コマンドで教えるよりずっと難しい**。

GUI を言葉で説明するのは構造的に困難だ。「設定の左メニューの上から 3 番目」はバージョンで変わる。「歯車のアイコンをクリック」は画面のどこにあるかで違う。スクリーンショットを撮っても、AI が指せるのは大まかな場所だけ。設定画面が階層化されていればされているほど、人間に手順を渡すコストが上がる。Windows の深い設定はとくに、AI が言葉で導くのが難しい場所だ。

コマンドは違う。テキストで完結する。企業で最も多く使われているAIはClaudeであるが、Claudeが書いたコマンドを、あなたがコピーして貼り付ければ、そのまま動く。エラーが出ても、その文字列をそのまま Claude に渡せば、原因を特定できる。

**Linux の「コマンドが多い」という弱点は、AI が横にいる時代には強みに変わった**。そして同時に、**Windows の「すべて GUI で完結する」という強みは、AI 時代には弱みに変わった**。

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

AI 時代には、Linux の方が使いやすい。
コマンドは AI が書く。アプリは Flathub から入る。古い PC でも軽快に動く。
道具が揃ったのは、Windows ではなく Linux の側だった。

[Claude と一緒に学ぶ Debian →](/claude-debian/)

---

*関連記事: [「Windows が壊れていく」── ナデラが Windows を見限った構造](/blog/windows-breaking-down/)*

*関連記事: [「それでも Windows と Office を使い続けますか?」── 詳細な構造分析と一次情報・参考文献](/blog/windows-office-facts/)*

*関連記事: [「日本の Windows 災害リスク」── 一斉サポート終了の社会的インパクト](/blog/japan-windows-disaster-risk/)*

*関連記事: [「AI 時代には『特化したエンジニアになれ』は構造を取り違えている」── ソフトウェア工学からリベラルアーツへの基盤転換](/blog/software-three-transitions/)*
