# カタログエディタ — aiseed-builder の「商品」プラグイン設計

2026-07-28。vegitage(イタリア野菜図鑑)の編集を最初の利用者として、
aiseed-builder に「品目カタログ」の編集能力を足す。WordPress の語彙で言えば、
site-editor が「投稿」、これは「カスタムフィールド付きカスタム投稿タイプ=商品」。
スキーマ駆動にすることで、野菜図鑑も将来の EC 商品も同じエディタで扱える。

## 現状の確認(2026-07-28 時点)

- 正本: `vegitage-data/web/italian/` に 69 品目。1品目 =
  `<作物>.md`(YAML フロントマター+概要文)+ `history|cultivation|cuisine/<作物>.md`
  (サブガイド計135ファイル、全651枠中は歯抜けあり=無いタブは出ない仕様)
- フロントマター: `id`(master_lists と突合・暫定)、`name_ja/it/en`、`aliases`、
  `family/family_latin/botanical`、`index_group`(目次「科」タブ)、`type`(複数)、
  `certification`、`regions`、`season`、`uses`、`hero_image`。
  **行内コメントが情報を持っている**(例: `id: … # master_lists と要突合せ（暫定）`)
- ビルド: `vegitage-data/web/build.py`(markdown+PyYAML、全ビルドのみ)。
  出力 `web/site/italian/` ← `html/vegitage/italian` が symlink。
  つまり**ビルドすれば既存のプレビュー(serve.py)と公開(deploy)に自動で乗る**
- たたき台: `data/deep_research/italian/<作物>/` に 71 品目分。
  正本 69 との差=未取込の「入荷待ち」
- 状態管理: 無し(draft の概念が build.py に無い)

## 設計原則(aiseed-builder の既存原則を踏襲)

1. **パーサとスキーマの正はサイト(データ)側に一つだけ。** builder は読むだけ。
   → スキーマはカテゴリフォルダに置く: `vegitage-data/web/italian/schema.yaml`
2. **壊れる編集は拒否。** 保存時に必ず再パース+スキーマ検証し、通らなければ戻す
   (site-editor と同じ)。
3. **プラグインは登録制。** `plugins/catalog/` を足し、site.json の
   `builder.plugins` に `"catalog"` を追加するだけ。main.py に分岐は書かない。

## 1. スキーマ宣言 — schema.yaml

カテゴリ(=カタログ)ごとに1ファイル。フィールド定義・セクション構成・状態の
規約をここに集約する。builder はこれを読んでフォームを組み立てる。

```yaml
label: イタリア野菜図鑑
item_label: 品種            # UI の「新規追加」等の呼称
url_base: /vegitage/italian

fields:
  - {key: id,           label: 品目ID,  type: id}       # 読み取り専用表示
  - {key: name_ja,      label: 和名,    type: text, required: true}
  - {key: name_it,      label: 伊名,    type: text}
  - {key: name_en,      label: 英名,    type: text}
  - {key: aliases,      label: 別名,    type: tags}      # 自由入力の複数値
  - {key: family,       label: 科,      type: text}
  - {key: family_latin, label: 科(学名), type: text}
  - {key: botanical,    label: 学名,    type: text}
  - {key: index_group,  label: 目次グループ, type: select, options: existing}
  - {key: type,         label: 種類,    type: tags, options: existing}
  - {key: certification, label: 認証,   type: tags,
     options: [DOP, IGP, PAT, Slow Food], open: false}   # 閉じた語彙のみ検証で弾く
  - {key: regions,      label: 主な産地, type: tags, options: existing}
  - {key: season,       label: 旬,      type: tags,
     options: [春, 夏, 秋, 冬, 通年], open: false}
  - {key: uses,         label: 用途,    type: tags, options: existing}
  - {key: hero_image,   label: 画像,    type: image}

sections:                    # 本文タブ。dir: null は概要ファイル自身
  - {dir: null,        label: 概要}
  - {dir: history,     label: 歴史}
  - {dir: cultivation, label: 栽培}
  - {dir: cuisine,     label: 料理}

status:
  draft_key: draft           # フロントマターの draft: true で下書き
```

フィールド type は5種で足りる:

| type | UI | 検証 |
|---|---|---|
| `text` | 1行テキスト | required のみ |
| `tags` | チップ入力(複数値) | `open: false` なら options 外を拒否 |
| `select` | ドロップダウン(1値) | 同上 |
| `image` | ファイル選択+プレビュー | 参照先の存在 |
| `id` | 読み取り専用表示 | 触らない |

`options: existing` は「既存データから語彙を収集してサジェスト(開いた語彙)」。
閉じた語彙(`open: false`)だけが検証で弾かれる。**表記ゆれは閉じずに直す**——
一覧のファセットに「Lazio(12) / ラツィオ(1)」と出れば、ゆれは目で見える。

EC 商品への布石: `price` や `stock` が必要になったら type を足すのではなく
`text`+`format: number` を足す程度で済む。スキーマ形式自体は汎用。

## 2. 編集単位 — 品目バンドル

1品目 = 概要+サブガイド3+画像。エディタは品目単位で開く。

- **ファイル名(=URL)は日本語のまま。** 既公開 URL の維持が最優先。
  ファイル名がバンドルの結合キーなので、改名はエディタが4ファイル+画像を
  一括で改名する(手作業での不整合を防ぐのもエディタの仕事)。
- 概要ファイルのフロントマター書き戻しは **ruamel.yaml のラウンドトリップ**で
  行内コメントを保持する(`id: … # 要突合せ` のような注記が消えると困る)。
  依存は aiseed-builder 側にのみ追加。データ側 build.py は PyYAML のまま。
- サブガイドの追加: タブを開いて書き始めたらファイルが生まれる。空のまま
  保存したら作らない(歯抜けは仕様——ナビに出ないだけ)。

## 3. 状態管理 — 商品と同じ3状態

| 状態 | 定義 | 一覧での見え方 |
|---|---|---|
| たたき台 | `deep_research/italian/` にあり正本に無い | 灰色・「起こす」ボタン |
| 下書き | 正本にあり `draft: true` | 黄色バッジ・サイトに出ない |
| 公開 | 正本にあり draft 無し | 通常表示 |

- 「起こす」= たたき台のテキストを初期値に正本の雛形を生成(`draft: true` 付き)。
  deep_research → 人手仕上げ → 公開、という既存ワークフローをそのまま UI 化。
- **build.py への変更は draft スキップだけ**(数行)。スキーマ検証はエディタ側の
  仕事とし、ビルドは今までどおり寛容に通す(手書き修正を妨げない)。

## 4. UI — WooCommerce の商品画面に対応

```
一覧画面(カタログごと)
  検索(名前・別名) / 絞り込み(科・種類・旬・産地・状態) / 新規追加
  行: 名前 | 学名 | 科 | type | 状態 | セクション充足(○○○-)
編集画面
  左カラム: スキーマ駆動フォーム(フロントマター)
  右カラム: 公開ボックス(状態・更新・プレビュー・削除)+ 画像ボックス
  下: セクションタブ(概要|歴史|栽培|料理)= Markdown エディタ
```

サイドバーには site.json の `catalogs` 配列の順でカタログ名が並ぶ
(シリーズ一覧と同格)。「変更を記録(git)」「サイトを公開」は既存機能を共用。

## 5. site.json への登録

```json
"builder": {
  "plugins": ["forms", "audit", "catalog"],
  "catalogs": [
    {"schema": "vegitage-data/web/italian/schema.yaml",
     "build": "vegitage-data/web/build.py",
     "preview_path": "/vegitage/italian/"}
  ]
}
```

「更新」ボタン = サイトの venv の python で `build` を実行 → symlink 経由で
serve.py のプレビューに反映。「公開」= 既存デプロイ(html/ 一式)に乗る。

## 6. 実装の段取り

1. **vegitage 側の受け入れ準備**(半日): schema.yaml を書く。build.py に
   draft スキップ。既存 69 品目をスキーマに通して表記ゆれの棚卸し
   (閉じた語彙は実データから確定させる)
2. **catalog プラグイン**(2〜3日): `plugins/catalog/`(store には触らず
   `catalog.py` を新設——記事の store.py と対になるデータ層)。
   一覧+編集+保存+ビルド。ruamel.yaml 追加
3. **取込フロー**(1日): たたき台一覧と「起こす」
4. **2カタログ目で汎用性を証明**: 日本野菜(build.py の CATEGORIES を
   設定駆動化して `web/japanese/` を追加)。ここまで来れば「EC の商品」も
   スキーマ1枚の距離

## 決めたこと(推奨)と根拠

- スキーマの置き場所はデータ側(builder は汎用のまま) — 原則1
- ファイル名・URL は日本語維持 — 既公開 URL、品目の自然キー
- コメント保持に ruamel.yaml — フロントマターのコメントが台帳情報を持つ
- 検証はエディタで厳しく、ビルドは寛容 — 手書きの逃げ道を塞がない
- 閉じた語彙は certification と season だけから始める — ゆれの実態を
  ファセットで可視化してから閉じる
