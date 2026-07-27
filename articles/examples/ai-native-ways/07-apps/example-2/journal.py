#!/usr/bin/env python3
"""journal — 一行メモ・日報・検索・エクスポートの最小 CLI(click + SQLite)。

第 8 章: CLI から始めて、必要に応じて Flet / Flutter に上げる ── の最初の段。
業務で「メモ書き → 翌週まとめ → 月次報告」という流れを 1 コマンドで全部。

サブコマンド:
  journal add     "テキスト"          ── メモ追加
  journal list    [--limit N]          ── 一覧
  journal search  "キーワード"          ── 検索
  journal stats                        ── 集計
  journal export  --since YYYY-MM-DD   ── Markdown へエクスポート
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

import click

DB = Path(__file__).parent / "out" / "journal.db"
DB.parent.mkdir(exist_ok=True)


def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            tag  TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
    return c


@click.group()
def cli():
    """一行メモから月次報告まで、ひとつの CLI で。"""


@cli.command()
@click.argument("text")
@click.option("--tag", default="", help="タグ(任意)")
def add(text, tag):
    """メモを追加。"""
    with conn() as c:
        cur = c.execute("INSERT INTO notes (text, tag) VALUES (?, ?)", (text, tag))
        click.echo(f"  added #{cur.lastrowid}: {text[:60]}{'…' if len(text) > 60 else ''}")


@cli.command(name="list")
@click.option("--limit", default=10, type=int, help="最大件数")
@click.option("--tag", default=None, help="タグで絞り込み")
def list_cmd(limit, tag):
    """最新のメモを一覧。"""
    with conn() as c:
        if tag:
            rows = c.execute("SELECT * FROM notes WHERE tag = ? ORDER BY id DESC LIMIT ?",
                             (tag, limit)).fetchall()
        else:
            rows = c.execute("SELECT * FROM notes ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    if not rows:
        click.echo("  (なし)")
        return
    for r in rows:
        ts = r["created_at"][:16]
        tg = f"[{r['tag']}] " if r["tag"] else ""
        click.echo(f"  {r['id']:3d}  {ts}  {tg}{r['text']}")


@cli.command()
@click.argument("keyword")
def search(keyword):
    """全文検索(LIKE)。"""
    with conn() as c:
        rows = c.execute(
            "SELECT * FROM notes WHERE text LIKE ? ORDER BY id DESC",
            (f"%{keyword}%",),
        ).fetchall()
    click.echo(f"  '{keyword}' に一致: {len(rows)} 件")
    for r in rows:
        click.echo(f"    {r['id']:3d}  {r['created_at'][:10]}  {r['text']}")


@cli.command()
def stats():
    """件数・タグ別集計を JSON で。"""
    with conn() as c:
        total = c.execute("SELECT COUNT(*) AS n FROM notes").fetchone()["n"]
        by_tag = c.execute(
            "SELECT COALESCE(NULLIF(tag,''), '(no-tag)') AS tag, COUNT(*) AS n "
            "FROM notes GROUP BY tag ORDER BY n DESC"
        ).fetchall()
    out = {"total": total, "by_tag": [dict(r) for r in by_tag]}
    click.echo(json.dumps(out, ensure_ascii=False, indent=2))


@cli.command()
@click.option("--since", default=None, help="YYYY-MM-DD 以降")
@click.option("--out", "out_path", type=click.Path(), default=None, help="出力先 .md")
def export(since, out_path):
    """Markdown 形式でエクスポート(月次報告用)。"""
    with conn() as c:
        if since:
            rows = c.execute("SELECT * FROM notes WHERE date(created_at) >= ? ORDER BY id",
                             (since,)).fetchall()
        else:
            rows = c.execute("SELECT * FROM notes ORDER BY id").fetchall()
    md = ["# 業務日報\n"]
    if since:
        md.append(f"期間: {since} 以降\n")
    md.append(f"件数: {len(rows)}\n")
    current_day = None
    for r in rows:
        day = r["created_at"][:10]
        if day != current_day:
            md.append(f"\n## {day}\n")
            current_day = day
        tg = f"`{r['tag']}` " if r["tag"] else ""
        md.append(f"- {r['created_at'][11:16]}  {tg}{r['text']}")
    text = "\n".join(md) + "\n"
    if out_path:
        Path(out_path).write_text(text)
        click.echo(f"  → {out_path}  ({len(text)} B, {len(rows)} 件)")
    else:
        click.echo(text)


if __name__ == "__main__":
    cli()
