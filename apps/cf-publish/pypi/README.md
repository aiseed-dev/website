# cf-publish (PyPI パッケージ版)

ローカルのフォルダを **Cloudflare Pages** へ直接アップロードして公開する CLI。
wrangler も npm も要らず、`pip install` だけで使える Python パッケージ。

3スタック試作（`apps/cf-publish/` の Rust / Flet / Flutter）に対する **4本目**で、
「**PyPI で配って `pip install` して使う**」ケースを想定した版。

## 使い方（配布される側）

```bash
pip install cf-publish            # （公開後）
export CLOUDFLARE_API_TOKEN=...    # 「Cloudflare Pages: 編集」権限のトークン
export CLOUDFLARE_ACCOUNT_ID=...
cf-publish ./public --project aiseed-dev
# トークンは ~/.config/cloudflare/pages.env (KEY=VALUE) にも置ける
```

- `--branch main` で本番、それ以外はプレビュー URL。
- `--no-create` でプロジェクトが無いときに作らずエラーにする。

## パッケージ構成

```
pyproject.toml              # hatchling。console script: cf-publish = cf_publish.cli:main
src/cf_publish/
  pages.py                  # UI 非依存のデプロイロジック（値を返す/例外を投げる）
  cli.py                    # argparse の薄い CLI
```

`pages.deploy(dir, project, branch, create, on_progress)` は **UI 非依存**（`sys.exit`/`print`
を持たず、`PagesError` を投げ、進捗は `on_progress` コールバックで通知）。CLI からも将来の
GUI からも import して再利用できる。

## ビルド・ローカル確認

```bash
uv build                                  # dist/ に wheel と sdist を生成
uv venv .venv && . .venv/bin/activate
uv pip install dist/cf_publish-0.1.0-py3-none-any.whl
cf-publish --help
```

## PyPI 公開（実施は別途・明示的に）

```bash
uv publish                                # または: python -m twine upload dist/*
```

実際の公開には PyPI アカウント/トークンが要る。CI なら **Trusted Publishing（OIDC）** が安全。
パッケージ名 `cf-publish` は PyPI での空きを公開前に確認すること。

> この環境には Cloudflare 認証情報が無いため、**実デプロイの動作確認まではしていない**。
> パッケージの **ビルド・インストール・`cf-publish --help` の起動**までを確認済み。
