# ONLYOFFICE → Euro-Office 移行メモ

2026-08-06 調査。**Euro-Office は ONLYOFFICE の改称ではなく、フォーク(別製品)。**
一括置換は事実誤認になるので、正式版の出そろいを待って段階的に移行する。

## 事実(2026-08-06 時点)

- **2026-03-27** 欧州企業連合が ONLYOFFICE のコードからフォークを発表。
  参加: IONOS、Nextcloud、Eurostack、XWiki、OpenProject、Soverin、Abilian、
  BTactic、Office EU、Open-Xchange。動機は欧州のデジタル主権。
- **ライセンス係争は決着済み。** 開発元 Ascensio System SIA (ONLYOFFICE) は当初
  AGPLv3 違反を主張し Nextcloud との提携を停止したが、FSF と法律家が
  「AGPL 第10条により再配布時に追加的制限条項を除去できる」と支持。
  6月のリリースまでに収束した。Euro-Office は **AGPL-3.0-only**。
- **2026-06-09 初の安定版。** ただし対象は **Euro-Office Docs
  (DocumentServer＝ブラウザの共同編集エンジン)**。Nextcloud Hub 26 Spring に統合。

### ここが重要 ── デスクトップ版はまだ無い

| 製品 | Euro-Office の状況 | 本サイトでの参照箇所 |
|---|---|---|
| **Docs / DocumentServer**(サーバ・ブラウザ) | **安定版あり**(1.0 / 2026-06-09) | `docs/linux-apps.md` の「OnlyOffice Docs（Document Server）」、自立編 2-05 |
| **デスクトップエディタ** | **リリース無し**(GitHub `Euro-Office/desktop-apps` は releases 0件、deb/rpm/AppImage/flatpak の配布資産なし。Flatpak は 2026-04 時点で要望中 issue #12) | `apps/debian-migrate`(flatpak 導入)、claude-debian、blog ほか |

つまり「正式版が出れば移行」が効くのは**デスクトップ側**。サーバ側は既に移行可能。

## 移行時の作業(正式版が出たら実行)

対象は 232 箇所。性質で3つに分かれる。

1. **実行されるコード(最優先・壊れるので機械的置換は不可)**
   - `apps/debian-migrate/src/debian_migrate/data/install_commands.py`
     現在 `flatpak install -y flathub org.onlyoffice.desktopeditors`。
     Euro-Office の**アプリID・配布経路が確定してから**差し替える
     (Flathub に載るのか、独自 deb リポジトリかで手順が変わる)。
   - 同 `data/replacements.py`、`tests/test_post_install.py`
   - `tools/scaffolds/contact/tools/form-builder/form_xlsx.py`
2. **推奨として書いている記事**(ai-native-ways-software 82、ai-native-ways 79、
   claude-debian 51、blog 12、insights 8)
   → 推奨先を Euro-Office に切り替える。ただし**過去の事実記述**
   (「ONLYOFFICE が〜した」「ONLYOFFICE Desktop Editors は無料」等)は
   ONLYOFFICE のままにする。置換ではなく書き換えが要る。
3. **スキル定義**(`.agents/skills/writing-aiways-voice`、
   `building-ai-native-software-series`)→ 用語例の更新。

## 記事の題材としての価値

フォークの経緯そのものが本サイトの主題(デジタル主権・脱Microsoft・
オープンウェイト/オープンソースの統治)と重なる。「欧州がコードで主権を取る」
「AGPL 第10条が効いた」という筋は、[[zero-trust-blog-series]] や
ソフトウェア開発編の議論に接続できる。

## 出典

- https://en.wikipedia.org/wiki/Euro-Office
- https://nextcloud.com/blog/euro-office-general-availability-set-for-june-9/
- https://github.com/Euro-Office/desktop-apps (releases 0件を確認)
- https://alternativeto.net/news/2026/4/onlyoffice-ends-its-partnership-with-nextcloud-over-new-unauthorized-euro-office-fork
