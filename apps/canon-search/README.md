# canon-search — 正典検索

ウェブの多数決ではなく、**自分で選んだ一次資料(正典)だけ**を索引し、検索し、
AI に渡すコンテキストとして取り出すための道具。

生成 AI が記憶から語ることは「商業的に加重された世間の平均」であって正解ではない
(→ ブログ[「AIは無知だから間違えるのではない」](https://aiseed.dev/blog/ai-not-ignorance-but-average/))。
誤答を減らす王道は、規格・法令・公式文書という一次資料を索引し、AI には
「与えた資料を読んで整理する」仕事をさせることである。canon-search はその
「何を文脈に入れるか」の中間層を、自分のマシンで握るための最小実装。
ランキング関数とは機械化された正典選びであり、それを他人(検索エンジンの
商業的加重)に委ねない、というのが設計思想。

## 特徴

- **依存ゼロ**: Python 標準ライブラリのみ(SQLite FTS5 trigram 索引 + pdftotext)
- **日本語対応**: 分かち書き不要の trigram、3文字未満の語は LIKE 走査で補完
- **出典つき**: すべての検索結果・コンテキスト出力に原典 URL が付く
- **AI 連携はプラガブル**: `context` コマンドの出力をどのモデルに貼ってもよい。
  将来はオープンウェイトの小型モデル(Kimi K3 系の小型版が出れば、それ)を
  ローカルで接続する

## 使い方

```bash
cd apps/canon-search
export PYTHONPATH=src
alias cs='python3 -m canon_search.cli'

# 正典の登録
cs add law 著作権法
cs add rfc 9110
cs add pdf https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf \
   --title "NIST SP 800-207: Zero Trust Architecture" --key "NIST SP 800-207" \
   --license "US Government work"

# HTML ページ(robots.txt を RFC 9309 解釈で尊重: 4xx=許可, 5xx=拒否)
cs add url https://www.maff.go.jp/j/keikaku/syokubunka/k_ryouri/search_menu/menu/44_11_tokushima.html \
   --license "農林水産省 うちの郷土料理(政府標準利用規約)"

# 検索
cs search "軽微 利用"          # → 著作権法47条の5が最上位に出る
cs search "network location trust"  # → SP 800-207 のゼロトラスト原則

# コーパスは CANON_DB で使い分けられる(例: 伝統野菜・料理の正典)
CANON_DB=$PWD/data/vegitage.db cs add law 種苗法

# AI に貼るコンテキストの生成(「知識は文脈に」の実装)
cs context "検索エンジン 軽微" -k 3 | クリップボードへ / モデルへ

cs list                        # 登録済み文書
```

データベースは `data/canon.db`(gitignore 済み)。`CANON_DB` 環境変数で変更可。

## 法的根拠

対象は権利処理が明確な一次資料に限る。

- **法令**: 著作権法13条により、法令・判決等はそもそも権利の目的とならない
- **RFC**: IETF Trust のライセンスにより複製可
- **NIST 等の米国政府文書**: 米国内パブリックドメイン

なお、日本の著作権法は検索エンジンのための権利制限を明文で持つ
(47条の5: 所在検索・情報解析サービスの軽微利用、30条の4: 情報解析のための利用、
47条の5第2項: 準備行為としての収集・索引)。個人利用の範囲を超えて
公開サービス化する場合は、政令基準(robots.txt 尊重、削除申出への対応等)と
「軽微利用」の表示範囲を確認すること。

## 設計メモ

- チャンク単位: 法令は条単位(第N条+見出し)、RFC/PDF は節見出しを追跡した
  ~1200字の段落パック
- 検索: FTS5 trigram の BM25。3文字未満の語(日本語の2字熟語、"AI" など)は
  trigram が照合できないため、LIKE 走査でフォールバック(個人規模なら十分速い)
- 正規化: NFKC(全角/半角ゆれの吸収)

## AI辞典ワークフロー(ask → 執筆 → checkcite)

「AI版Wikipedia」を正典係留で作るための最小ループ。生成の各文が
一次資料に裏打ちされているかを機械検証し、幻覚(引用先に無い記述)を弾く。

```bash
export CANON_DB=$PWD/data/vegitage.db

# 1. grounding pack を出す(各チャンクに引用ID [n] を付与)
cs ask "金時草 金沢 栽培 由来" -k 1 > pack.txt

# 2. pack の範囲だけで辞典項目を執筆。各文末に根拠の [n] を付ける
#    (人間が書いても、モデルに pack を渡して書かせてもよい)

# 3. 草稿を正典と照合検証。各文の文字3-gram被覆率がしきい値未満なら弾く
cs checkcite draft.md "金時草 金沢 栽培 由来" -k 1
#   ✔ 0.94 …熱帯アジアが原産である。
#   ✘ 0.16 金時草は…スーパーフードとして人気を集めている。 → 引用元に根拠なし
```

実例は `vegitage-data/drafts/ai/金時草.md`(加賀野菜公式サイトの正典[1]のみ
から生成し、全11文が裏取りOK)。捏造した一文だけが検証で弾かれることを、
同ファイルの生成過程で確認済み。

注意: 同一言語の検証器は NLI ではなく文字n-gram被覆なので、正典に忠実でも
言い換えが強い文は偽陽性になりうる(=「正典の語に近く書け」という圧力)。

### クロスリンガル検証(この道具の一番の価値)

日本の野菜は日本人が原典を読んで検証できる。価値が最大化するのは、原典が
外国語で人間が直接検証できない場合 ── イタリア野菜の生産仕様書(disciplinare)
などだ。ここでは「日本語の主張」に「原語の逐語スパン」を 〔…〕 で併記する:

```
収穫は苞が開く前、9月1日から5月31日までに行う。〔prima dell'apertura delle brattee, ossia dal 1° settembre al 31 maggio〕[1]
```

検証は二段構え:
1. **機械(捏造引用の排除)**: 〔…〕が正典に部分文字列として実在するかを
   照合する。文字n-gram被覆と違い言語間で共通する機能語ノイズに惑わされず、
   引用IDの取り違えにも強い(実在すればどのチャンクかを自動特定する)。
2. **人間(翻訳の忠実性)**: 日本語↔原語スパンの対応だけを、対訳を見て監査する。
   原語を流暢に読めなくても、一文ずつの対応なら確認できる。

`ask --doc <doc_key>` で文書1本の全チャンクを pack にし、`checkcite --doc` で
照合する(キーワード検索だと必要チャンクが AND で落ちるため、辞典生成は
文書単位が正しい)。実例は
`vegitage-data/drafts/ai/carciofo-spinoso-di-sardegna.md`(サルデーニャ産
アーティチョーク DOP を伊語公式 disciplinare のみから生成、全10文が逐語一致で
裏取りOK、捏造した「東京市場」の一文だけが検出・排除された)。

## 応用例: 伝統野菜・料理辞典の照合検証

`vegitage-data/src/verify_certifications.py` は、品種CSVの認証主張(DOP/IGP等)を
正典索引(公式 disciplinare・うちの郷土料理)と突き合わせ、
「裏取りあり / 要確認 / 正典未収録」に分類する。未収録は誤りではなく
コーパスの未整備として明示する(暗黙に検証済み扱いしない)。

## ロードマップ

1. HTML本文抽出の改善(リンク密度によるナビゲーション断片の除去)
2. 埋め込みによる意味検索の併用(ハイブリッド検索)
3. ローカルのオープンウェイトモデル接続(`ask` コマンド: 検索→読解→出典つき回答)
4. コーパスのプリセット(セキュリティ正典、著作権正典、伝統野菜正典、など)

## テスト

```bash
python3 -m pytest tests/ -q   # pytest がなければ tests/test_core.py を直接実行
```
