# 今後の作業プラン ── 「文章からアプリを作るのは得意」以降の会話から

> このファイルは `/root/.claude/plans/cozy-honking-truffle.md` (Plan モードの保存先)
> のコピー。コンテナ側のプランファイルはセッション終了で消えるため、リポジトリの
> docs/ に永続版として置く。後続セッションで参照しやすいよう、ペアになる
> `docs/manual-driven-development.md` の隣に配置。

## Context

2026-05-22、Debian 移行ウィザード v0.4.0 (apps/debian-migrate/、11 step、本書 24 章を wizard 化、32 テスト全通過、HTTP 200 + WS 101 確認済み) の完成後、ユーザーの一言「文章からアプリを作るのは得意なようですね。」から始まった一連の会話で、以下の論点が固まった:

1. **トークン効率** ── Markdown vs Word (2x)、Python vs Java (2-5x)、ワークフロー (10-100x)
2. **マニュアル駆動開発** ── マニュアルがアプリの仕様として機能する原理
3. **業務アプリ 6 ステップ** ── 現場 + ビルダー + AI の協創
4. **マニュアル協創** (Step 1 の 4 モード) ── 現場が一人で書けない場合の代替案
5. **ビルダー巡回モデル** ── 中世のマスター・メイソンの現代版
6. **SIer モデルとの 10-100x コスト比較** ── 残る領域 / 消える領域
7. **知的生産環境への一般化** ── 業務アプリ / 著作 / 研究 / 教育 / 士業
8. **AI 時代の自由人の物質的定義** ── 自分の知的生産環境を所有する個人
9. **採用の波 (5 段階)** と **SIer 業界の縮小タイムライン**
10. **徒弟制度モデル** ── Debian 移行が最良のカリキュラム
11. **増殖メカニズム** ── 1 マスター → 5 徒弟 → 25-50 件/年

(1)〜(9) は `docs/manual-driven-development.md` (508 行) に保存済 (コミット `203864b`)。(10) (11) は未追記。

これら 11 論点を、後続セッションで別々に展開する。論点の粒度が異なるため、1 セッションで全部はやらない。

---

## 作業項目 (推奨順)

依存関係: A → (B, C, D, E) → (F, G) / H は独立

### A. docs/ に徒弟制度セクションを追記 [小・前提]

**目的**: 徒弟制度モデル (会話の論点 10, 11) を docs に保存し、後続記事化セッションから参照できる状態にする。

**ファイル**: `docs/manual-driven-development.md`

**追記内容** (新・第九節として、第四「ビルダー巡回」と第八「広がり方」の中間に挿入。既存節を 1 つずつ繰り下げ):

- 「最初の移行を誰がやるか」が adoption の最大の摩擦である
- 双方向交換としての徒弟制度 (マスター得るもの / 徒弟得るもの 4×4 表)
- **Debian 移行は最良のカリキュラム** ── 7 つの実地スキル領域 (terminal / Git / package mgmt / data formats / Python / Claude 対話 / 判断練習)
- 多人数版 6 ステップ (Step 3 で徒弟が手を動かす、マスターは画面共有でレビュー)
- 増殖メカニズム (1 → 5 → 25-50/年)
- 具体的に始める形 (期間: 週末 2-3 回 × 4-5 時間)

**所要**: 1 セッション、推敲込みで 1-2 時間

**検証**: `git diff docs/manual-driven-development.md` で新節が挿入されていること、既存節の番号が正しく繰り下がっていることを確認。

---

### B. ソフトウェア開発編 第 12 章: 業務アプリ 6 ステップ + ビルダー巡回 [大]

**目的**: docs の第一〜五節 + 新・第九節 (徒弟制度) を、ソフトウェア開発編の続編として記事化。SIer 委託モデルを置き換える業務形態を、ビルダー側読者に届ける。

**ファイル**: `articles/ai-native-ways/software/12-manual-driven-builder/{ja,en}.md`

**ケーススタディ**: 今夜の Debian 移行ウィザード (apps/debian-migrate/、HTTP 200 + 32 テスト + 11 ステップ + 本書 24 章対応)。

**前提**: `building-ai-native-software-series` SKILL を読んでサブシリーズ規約を確認 (number、label、prev/next、template)。

**併せて更新**:
- `articles/ai-native-ways/software/README.md` 章一覧 (11 → 12)
- `.agents/skills/building-ai-native-software-series/SKILL.md` の章リスト
- 第 11 章「数年で完了する構造転換」の next_slug

**長さ**: 5000-7000 字

**検証**: `python3 tools/build_article.py --all` で全 build が通る、ソフトウェア開発編目次に 12 章が出る、HTTP の prev/next リンクが繋がる。

---

### C. 親シリーズ 第 14 章: 自分の知的生産環境を持つ [大]

**目的**: docs の第六〜七節を、親シリーズ序章「AI 時代の自由人」の物質的続編として記事化。読者層は知的生産者全般 (著作・研究・士業)。

**ファイル**: `articles/ai-native-ways/14-own-environment/{ja,en}.md`

**章番号**: 現状 00 序章 + 01-13 = 14 章。新規追加で 00 + 01-14 = 15 章になる。

**前提**: `authoring-aiways-chapter` + `writing-aiways-voice` SKILL を読んで親シリーズ規約を確認。

**併せて更新**:
- `articles/ai-native-ways/README.md` 章一覧 (14 → 15、新章追加)
- 第 13 章 (one-plus-ai) の next_slug を新章の slug に
- 新章の prev_slug を one-plus-ai に、next_slug を空に
- `framing-second-renaissance` SKILL の章マッピング表 (15 概念 ↔ 章の対応)
- `writing-aiways-voice` SKILL の章範囲 (00-13 → 00-14)
- 最上位 `README.md` の全 14 章 → 全 15 章

**ケーススタディ**: aiseed.dev リポジトリ自体 (articles + tools + 14 章 + 11 章 + 24 章 + 13 章 + 13 章 + 42 ブログ + 例集 が一つの環境で動く実演)。

**長さ**: 4500-6000 字

**検証**: 全 build pass、親シリーズ index に新章が並ぶ、step counter が 15 になる。

---

### D. 採用の波・SIer 縮小タイムライン (Insights 記事) [中]

**目的**: docs の第八節を、構造分析シリーズの記事として独立化。読者層は経営者・SIer 出身者・転職検討中のエンジニア。

**ファイル**: `articles/insights/N-sier-transition-timeline/{ja,en}.md` (番号は既存 insights を見て決める)

**内容の中心**:
- 加速する 6 つの力
- 採用の 5 段階 (今〜10 年)
- SIer 業界の縮小予測 (2027 / 2028 / 2030)
- 急速な広がりに伴うリスク (失敗ケースと反動、12-18 ヶ月の揺り戻し)
- 失敗を「旧来モデルに戻れ」ではなく「AI ネイティブを学べ」に転換する語り口

**併せて更新**:
- `articles/insights/README.md` (もしあれば章一覧)
- top README の Insights セクション

**長さ**: 3500-4500 字

**前提**: 既存の `articles/insights/` の voice / format を読んで合わせる。

**検証**: build pass、insights index に出る。

---

### E. 「Debian 移行は最良のカリキュラム」(オプション・分割) [中]

**目的**: 徒弟制度モデル + Debian 移行カリキュラムを独立記事として書きたい場合の代替案。A で docs に追記済みなので必須ではない。判断は B が書けてから。

**ファイル候補**:
- `articles/ai-native-ways/software/N-apprenticeship-curriculum/{ja,en}.md` (ソフトウェア開発編の派生)
- または `articles/blog/N-debian-as-curriculum/{ja,en}.md` (時事的に)

**スキップ判定**: B 第 12 章で徒弟制度を十分扱えていれば、E は不要。B が手薄なら E を追加。

---

### F. トークン効率 Blog (任意・小) [小]

**目的**: 会話冒頭の「Claude Max で短時間に制限に当たる人」議論を独立記事に。

**ファイル**: `articles/blog/N-token-economy/{ja,en}.md`

**注意**: 既存 `articles/blog/018-python-in-excel-eight-years-later/` で部分的に触れているので、重複しないように差別化が要る。

**長さ**: 2500-3500 字

**判定**: 既存の 018 を再読してから、独立記事化か既存記事補強かを決める。

---

### G. ビルダー巡回サービスのメニュー化 [中]

**目的**: aiseed.dev に「ビルダー巡回サービス」の公式メニューを掲載。記事 B / C を読んで問い合わせる人の受け皿。

**ファイル**:
- `html/services/index.html` (新規ページ) または `html/about/` 拡張
- メニュー: 初回 3 日 (¥15-45 万)、月次アドバイザリー (¥5-10 万)、対象領域 (業務アプリ / 著作 / 研究)
- 申込方法 (メール? フォーム?)
- 既存ケーススタディへのリンク (Debian 移行アプリ、aiseed.dev リポジトリ自体)

**ナビ更新**: top page の menu に「サービス」を追加。

**併せて検討**: 徒弟募集ページ (`html/apprentice/`) を同時に置くか別途か。

**注意**: 商売側の決定 (価格・申込フロー・契約形態) はユーザーの判断事項。

**検証**: HTML として表示できる、各リンクが繋がる。

---

### H. Debian 移行アプリの配布 [中・独立]

**目的**: `apps/debian-migrate/` を実際に普通の人がダウンロードして使えるバイナリにする。

**前提**: 既に `.github/workflows/debian-migrate-build.yml` が `workflow_dispatch` と `release: created` をトリガーに 3 OS バイナリをビルドする workflow として置かれている (subosito/flutter-action 使用)。初回実行で Flutter SDK との整合性検証が要る。

**作業**:
1. **アプリの実機検証** (今日の作業として既に進行中)
   - Linux で `make run` でネイティブ起動を確認
   - 11 step を全部踏んでみる
   - 各 Claude プロンプトが claude.ai に貼って機能するか
   - Markdown レポートが期待通りに出力されるか
2. `flet build linux` を手元で 1 度走らせて、ローカルでバイナリができるかを確認
3. CI workflow を `workflow_dispatch` で 1 度走らせて、3 OS バイナリが artifact に出るかを確認
4. (整ったら) GitHub Release v0.4.0 を作成、`release: created` で workflow が発火して、リリースに自動添付されるか
5. apps/debian-migrate/README に「ダウンロード」セクションを追加 (release URL を貼る)
6. 最上位 README とトップページの「関連アプリ」セクションにダウンロードリンク
7. (任意) スクリーンショット 5-6 枚を `apps/debian-migrate/screenshots/` に置き、README に貼る

**注意**:
- Flutter SDK の取得は CI で数分かかる。初回は色々試行錯誤が想定される。
- `.github/workflows/debian-migrate-build.yml` の `subosito/flutter-action` のバージョンを最新確認。
- macOS バイナリは Apple Developer 署名が無いと初回起動で警告。これは「Right-click → Open」で回避できる旨を README に書く。

**検証**: 3 OS で実機がアプリを起動できる (Linux はこのコンテナで可能、Windows / macOS は手元 PC で要確認)。

---

## 取り掛かりの順序

1. **まず A** (徒弟制度を docs に追記) ── 30 分〜1 時間で済む、B/C の前提
2. **次に B または C** ── どちらから書いてもいいが、B (ソフトウェア開発編) の方が既存シリーズの自然な続編なので書きやすい
3. **B と C の間に H** を挟むのが現実的 (Debian アプリの配布を整えると、B/C のケーススタディとしてダウンロードリンクが置ける)
4. **D は B/C と並行か後** ── 構造分析の語り口は独立しているので、B/C 完成後に書いた方が一貫する
5. **G** ── B/C/D が公開されてから (実例があると説得力が出る)
6. **E, F** はオプション。判断は B/D 完成後に。

---

## 各セッションでの共通の検証手順

各セッションは以下で締めることを推奨:

1. `python3 tools/build_article.py --all` でビルドが通る
2. 新章の HTML が `html/ai-native-ways/.../index.html` に生成される
3. 該当シリーズ目次に新章が並ぶ
4. prev/next リンクが正しく繋がる
5. sitemap.xml に新 URL が登録される
6. `articles/ai-native-ways/README.md` などの章一覧表が更新されている
7. 関連 SKILL ファイル (章範囲記述があるもの) が同期している
8. git commit + push に至るまで実行

---

## 参考: 既に揃っている素材

新セッションで書き始める際に参照するもの:

| 素材 | 場所 |
|---|---|
| 草稿原稿 | `docs/manual-driven-development.md` (508 行) |
| 概念フレーム | `.agents/skills/framing-second-renaissance/SKILL.md` |
| サブシリーズ規約 | `.agents/skills/building-ai-native-software-series/SKILL.md` |
| 章スキャフォールド | `.agents/skills/authoring-aiways-chapter/SKILL.md` |
| Voice | `.agents/skills/writing-aiways-voice/SKILL.md` |
| Flet 開発作法 | `.agents/skills/building-flet-apps/SKILL.md` |
| ケーススタディ実装 | `apps/debian-migrate/` 全体 |
| ビルド workflow | `.github/workflows/debian-migrate-{test,build}.yml` |
| AI 活用マニュアル本体 | `articles/ai-native-ways/01-manual/{ja,en}.md` |
| 本書 (Debian 24 章) | `articles/claude-debian/` |
| Hegel 哲学読解 | `docs/hegel.md` |

---

*2026-05-22 作成、ExitPlanMode 後にユーザー承認済。`docs/` への永続化コピー。*
