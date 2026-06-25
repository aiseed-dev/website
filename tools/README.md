# tools/

aiseed.dev サイトの**ビルド・配信・ミラー・初期化**スクリプト群。
各ツールの詳しいマニュアルは [`docs/manuals/`](../docs/manuals/) に置く。

## スクリプト

| スクリプト | 役割 | マニュアル |
|---|---|---|
| `build_article.py` | Markdown → HTML の記事・ブログビルダー。`--all` で全記事＋インデックス＋sitemap を生成。 | [build_article.md](../docs/manuals/build_article.md) |
| `serve.py` | 開発サーバー。`articles/`・テンプレを監視して自動リビルドし、`html/` を HTTP 配信。 | `--help` / docstring |
| `cloudflare_pages_deploy.py` | Cloudflare Pages へ直接アップロード（wrangler・npm 不要。Direct Upload API の Python 実装）。 | [deploy-and-publish.md](../docs/manuals/deploy-and-publish.md) |
| `deploy.py` | ビルド → デプロイの薄いラッパ（`cloudflare_pages_deploy` を呼ぶ）。 | [deploy-and-publish.md](../docs/manuals/deploy-and-publish.md) |
| `mirror_site.py` | 既存の動的サイトをブラウザでレンダーし、静的ファイル束へミラー（SiteSucker 相当）。 | [mirror_site.md](../docs/manuals/mirror_site.md) |
| `init_site.py` | `tools/scaffolds/default/` から新規サイトの雛形を生成。 | `--help` / docstring |
| `html_to_md.py` | 既存 HTML 記事を frontmatter 付き Markdown へ変換。 | `--help` / docstring |

## ディレクトリ

| パス | 中身 |
|---|---|
| `build/` | `build_article.py` の実装（`config.py` / `markdown.py` / `images.py` / `template_vars.py`）。 |
| `templates/` | Jinja2 テンプレート（`article.html` / `index.html`）。 |
| `scaffolds/default/` | `init_site.py` がコピーする新規サイトの雛形。 |
| `dashboard/` | データダッシュボード生成（独自パッケージ。`dashboard/README.md` 参照）。 |

## 依存

```bash
pip install -r requirements.txt          # ビルド系（Jinja2・markdown-it-py・Pillow）
./.venv/bin/pip install playwright       # mirror_site.py 用
./.venv/bin/pip install httpx blake3     # cloudflare_pages_deploy.py 用
```

詳細は各スクリプト先頭の docstring（`python3 tools/<name>.py --help`）、または
[`docs/manuals/`](../docs/manuals/) を参照。
