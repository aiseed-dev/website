"""aiseed.dev 物理量ダッシュボードのバックエンド・パイプライン。

仕様: docs/physical-dashboard-spec.md（v0.1）。
取得 → 計算 → 静的 JSON 出力。常駐プロセスなし・重い依存なし（stdlib のみ）。
"""
