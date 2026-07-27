"""cf-publish — Cloudflare Pages へフォルダを直接デプロイする（wrangler/npm 不要）。

PyPI で配って `pip install cf-publish` → `cf-publish ./public --project name` で使う想定の
パッケージ版。デプロイのロジックは UI 非依存（`pages.deploy()` は値を返し例外を投げる）なので、
CLI からも将来の GUI からも import して使える。
"""

__version__ = "0.1.0"
