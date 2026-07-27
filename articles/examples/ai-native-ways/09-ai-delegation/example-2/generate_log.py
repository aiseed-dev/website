#!/usr/bin/env python3
"""Apache combined log 形式の架空アクセスログを 100,000 行生成する。

業務 Web のアクセスログをイメージ:
  - 95% は通常リクエスト(200/304)
  - 一部 404, 500
  - スパイク的にエラーが集中する時間帯あり
  - 一部のクライアント IP が異常多数(攻撃のシミュレーション)
"""
from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

OUT = Path(__file__).parent / "access.log"

PATHS = [
    "/", "/about", "/pricing", "/blog/", "/blog/post-1", "/blog/post-2",
    "/api/orders", "/api/stats", "/api/customers", "/login", "/dashboard",
    "/static/style.css", "/static/main.js", "/favicon.ico", "/robots.txt",
    "/admin", "/wp-login.php", "/.env", "/config.php",  # 攻撃試行
]
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0)",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "curl/8.0",
]


def generate():
    n = 100_000
    start = datetime(2026, 5, 1, 0, 0, 0)
    attacker_ip = "203.0.113.42"
    with OUT.open("w") as f:
        for i in range(n):
            t = start + timedelta(seconds=i * 2 + random.randint(-1, 1))
            # 攻撃 IP は全行の 5%
            if random.random() < 0.05:
                ip = attacker_ip
                path = random.choice(["/admin", "/wp-login.php", "/.env",
                                       "/config.php", "/admin/login.php"])
                status = random.choice([404, 401, 403])
                ua = "curl/8.0"
            else:
                # 通常の IP プールから
                ip = f"198.51.100.{random.randint(1, 200)}"
                path = random.choices(PATHS, weights=[
                    20, 8, 5, 6, 4, 4, 5, 3, 3, 6, 5, 12, 8, 4, 1, 0, 0, 0, 0
                ])[0]
                # ステータス分布
                r = random.random()
                if r < 0.85:
                    status = 200
                elif r < 0.92:
                    status = 304
                elif r < 0.97:
                    status = 404
                else:
                    status = 500
                ua = random.choice(USER_AGENTS)
            size = random.randint(200, 60_000) if status in (200, 304) else random.randint(100, 1500)
            ts = t.strftime("[%d/%b/%Y:%H:%M:%S +0000]")
            f.write(f'{ip} - - {ts} "GET {path} HTTP/1.1" {status} {size} "-" "{ua}"\n')
    sz = OUT.stat().st_size
    print(f"  生成完了: {n:,} 行 / {sz/1024/1024:.1f} MB → {OUT}")


if __name__ == "__main__":
    generate()
