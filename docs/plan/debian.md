# Windows 10のPCがある人へ

2025年10月、MicrosoftはWindows 10のサポートを終了した。ESUで1年延ばしている人、何もせずに使い続けている人——その先に、買い替え以外の道がある。

家にある古いPCに「Windows 11に対応していません」と表示される人が、世界中で数億人いる。第8世代より前のCPU、TPM 2.0非搭載——Microsoftの基準では「もう使えない」ことになっている。

しかし、ハードウェアは何も壊れていない。同じハードウェアで、Debianは普通に動く。むしろ軽快に動く。古いPCこそ、Linuxの方が向いている。

## Debianという選択

Debianは、30年以上続いている Linux ディストリビューションのひとつ。商業ベンダーの都合ではなく、世界中のボランティアによって維持されている。だから「サポートを切る商業判断」が起きにくい。

サポート切れのWindows 10が動いていたハードウェアで、Debian 13は普通に動く。Wi-Fi、画面、音、サスペンド——多くの場合、インストール後に追加設定はほとんど要らない。

## 「Linuxは難しい」は、AI時代に逆転した

Linuxは難しい、という印象は根強い。コマンドを打つ黒い画面、聞いたことのない用語、Windowsのような直感的な操作ができない——これは、人間が一人で覚える前提の話だった。

しかし、2026年の今、状況は二つの大きな変化で逆転している。

**ひとつ目は、AI が「コマンド」と相性がいいことだ。**

意外に思われるかもしれないが、Claudeのような AI は **WindowsのGUI操作を教えるのが苦手で、Linuxのコマンドを教えるのが得意**だ。

GUIを言葉で説明するのは難しい。「設定の左メニューの上から3番目」はバージョンで変わる。「歯車のアイコンをクリック」は画面のどこにあるかで違う。スクリーンショットを撮っても、AIが指せるのは大まかな場所だけ。

コマンドは違う。テキストで完結する。Claudeが書いたコマンドを、あなたがコピーして貼り付ければ、そのまま動く。エラーが出ても、その文字列をそのまま Claude に渡せば、原因を特定できる。

**Linuxの「コマンドが多い」という弱点は、AIが横にいる時代には強みに変わった。**

**ふたつ目は、Flathubだ。**

普段使いのアプリのインストールは、コマンドさえ要らなくなった。[flathub.org](https://flathub.org) を開けば、Linuxで動くアプリが一つの場所に並んでいる。

| カテゴリ | アプリ |
|---|---|
| ブラウザ | Firefox、Google Chrome、Chromium、Brave |
| オフィス | ONLYOFFICE Desktop Editors、LibreOffice |
| コミュニケーション | Zoom、Slack、Discord、Element、Signal |
| メディア | Spotify、VLC、Audacity、OBS Studio |
| クリエイティブ | GIMP、Inkscape、Krita、Blender、darktable |
| 開発 | Zed、VSCodium、Visual Studio Code、PyCharm、IntelliJ IDEA、Android Studio |
| ユーティリティ | Bitwarden、Joplin、Obsidian、Thunderbird |

Windowsで言えば、Microsoft Storeのような場所だ。しかし、Microsoft Storeより**むしろ揃っている**。

**Microsoft Storeには Google Chrome が無い**。Microsoftが自社のEdgeを優遇しているため、競合ブラウザを排除している。Chromeをインストールしたいユーザーは、Microsoft Storeで検索しても見つけられず、別の方法で探すことになる。一方、Flathubには Chrome も Firefox も Brave も並んでいる。ベンダーの都合で並びが歪められない。

**Microsoft Storeは広告を表示する**。アプリを探しているのに、関係ない有料アプリが「おすすめ」として割り込んでくる。Flathubには広告がない。

**Microsoft Storeは Microsoftアカウントへのサインインを求める場面が多い**。Flathubはアカウント不要。何も登録せずに、好きなアプリを入れられる。

つまり、現代のLinuxは**二層構造**になっている。

- **日常のアプリ**: FlathubからGUIで入れる。コマンドは要らない。
- **設定や開発**: コマンドで操作する。ここでこそ AI が真価を発揮する。

この二層が、AI時代のLinuxの強さだ。Windowsはどちらも中途半端——GUIは深い設定までは届かず、PowerShellのコマンドはAIにとっても扱いにくい。

## Claudeと一緒に学ぶ

このサイトには、Claude を横に置きながら学ぶための二つの教科書がある。

[**Claudeと一緒に学ぶDebian**](https://aiseed.dev/claude-debian/) は、Debian への移行を Claude との対話で進めるための23章の教科書だ。何を Claude に伝えるか、どう環境情報を取り出すか、ログをどう渡すか。詰まったときに何を試すか。これらは、Linux の知識そのものよりも、AI を使って学ぶための作法に近い。

[**AIネイティブな仕事の作法**](https://aiseed.dev/ai-native-ways/) は、Debian に移った先で何をするかを書いている。Excel の VBA を Python に、Word を Markdown に、CSV を JSON や SQLite に——AI が同僚になる時代の道具立てを、12章で整理している。

一度この作法を身につければ、Debian だけでなく、この先 AI と一緒に何かを学ぶ・作るときの基礎になる。

## 「捨てる」のは、いつでもできる

PCの廃棄は、いつでもできる。逆は難しい。

一度捨ててしまえば、買い替えに数万円から十数万円かかる。世界中で同じことが同時に起きれば、膨大な電子ゴミになり、新しいPCを作るための鉱物資源と化石燃料を消費する。

捨てる前に、一度だけ別の道を試してみる価値はある。動かなければ、それから捨てればいい。

Microsoft が「もう面倒を見ない」と言った日は、ハードウェアの寿命ではない。  
AIが横にいる時代、Linuxのコマンドはもう、難しくない。

[Claudeと一緒に学ぶDebian →](https://aiseed.dev/claude-debian/)

