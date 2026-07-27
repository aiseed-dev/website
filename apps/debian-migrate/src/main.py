"""アプリバンドル(`flet build`)のエントリポイント。

flet build は `[tool.flet.app] path` のディレクトリを**アプリのルート**として
展開し、その中の `main.py` を実行する。したがって path はパッケージ本体では
なく**その親**(= src/)を指す必要がある——パッケージ本体を指すと中身が
フラットに展開され、`from debian_migrate... import` が実行時に
ModuleNotFoundError になる(aiseed-builder の実機ビルドで確認)。

このファイルは薄い入口で、実体は debian_migrate/main.py。
"""

from debian_migrate.main import main

main()
