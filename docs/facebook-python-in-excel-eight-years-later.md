# Facebook 投稿用 ── 8年越しの答え合わせ

---

## 短め版(タイムライン向け、約 400 字)

8年前の予言の答え合わせ。

2017 年 12 月、私は Qiita に「ExcelにPythonが搭載?」と書いた。

「Pandas が使えれば、Excel なしでも動く。VS Code で編集、Git で管理、ローカルで自由に動く ── 本格的な開発環境が Excel に乗る」と期待した。

2023 年、ExcelにPythonが本当に搭載された。

しかし、8年前に書いた利点は **すべて削り取られている**。

❌ オフラインでは動かない(Azure に強制送信)
❌ VS Code でのデバッグ不可
❌ Git でのバージョン管理不可
❌ ローカル DB との連携不可
❌ Linux で動かない

技術的な制約ではない。PyXLL や xlwings Lite は同じことを既に実現している。Microsoft は **敢えてクラウドでしか動かない設計を選んだ** ── Azure サブスクを消費させ続けるために。

巨大ベンダーのビジネスモデルのために、自分のデータが人質に取られる時代は終わった。

詳しい話はブログに書いた:
👉 https://aiseed.dev/blog/python-in-excel-eight-years-later/

#AI #Python #Excel #Microsoft

---

## 長め版(グループ投稿向け、約 900 字)

【8年越しの答え合わせ ── ExcelにPythonが搭載、けれど】

2017 年 12 月、私は Qiita に「[ExcelにPythonが搭載?](https://qiita.com/yniji/items/2e80ace081c4b59bc327)」という記事を書いた。

期待は技術的に具体的だった。Pandas が使えれば、Excel なしでも動く。Linux サーバーでも問題なく使える。VS Code で編集、Git で履歴管理、デバッグもターミナル操作もできる。SQL Server から PostgreSQL へのデータ移行も Pandas 経由で簡単。**Excel をデータの GUI として使いながら、本格的な開発環境を持ち込める** ── 現場のエンジニアが共有していた、技術的に合理的な構想だった。

そして 2023 年、ExcelにPythonが本当に搭載された。Copilot も統合された。

しかし、8年前に描いた希望はそこに無い。

▼ 意図的に削り取られた利点

- オフライン動作不可。Python コードは **Azure Container Instances に強制送信**
- VS Code でのデバッグ不可
- Git でバージョン管理不可
- ローカル DB やローカルファイルへの自由なアクセス不可
- Linux サーバーで動かない

**これは技術的な制約ではない**。PyXLL や xlwings Lite といったサードパーティ製ツールは、ローカル実行も Git 管理も任意のライブラリ利用も、既に完全に実現している。Microsoft は技術を持ちながら、**敢えて「クラウドでしか動かない」設計を選んだ**。

理由は単純で、ローカル実行を許せば Azure のリソースは消費されない。前払いされた月額課金を消費させ続けるための、強制連行設計だ。

そして、Microsoft 自身のベンチマーク SpreadsheetBench での Excel Agent Mode の正答率は **57.2%**。約 4 割は間違える機能が、業務システムの中核に統合されている。

▼ 新しい時代の働き方

8 年前の希望は、Microsoft の檻に閉じ込められた。

だが、AI の進化でもはや Excel に依存する必要がなくなった。Claude のような対話型 AI が、設計・コード生成・データ処理・文書作成、すべての領域で人間を手伝う。**動き出した人から実現している現実**だ。

問題は Microsoft だけではない。Google Workspace も同じ構造。データとロジックが特定ベンダーのクラウドに **人質**に取られている点では変わらない。

巨大ベンダーのビジネスモデルのために、自分のデータとシステムが人質に取られる時代は終わった。

詳細はブログに書いた(Mermaid 図つき):
👉 https://aiseed.dev/blog/python-in-excel-eight-years-later/

シリーズ「AIネイティブな仕事の作法」も公開しています:
👉 https://aiseed.dev/ai-native-ways/

#AI #Python #Excel #Microsoft #働き方 #AIネイティブ

---

## 投稿時のメモ

- **短め版** は個人タイムライン向け。スクロール中の人の目を止める長さ。
- **長め版** は「AIネイティブ時代の仕事の作法」グループ([https://www.facebook.com/groups/timej](https://www.facebook.com/groups/timej))や、より技術的な読者層に向けて。
- どちらもブログへのリンクで詳細誘導。
- 画像を添える場合は、ブログの hero image(`IMG_3470.jpg`)を流用するか、Mermaid 図のスクリーンショットでも効果的。
