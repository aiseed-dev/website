"""シリーズ .adoc の読み書き——本文(ifdef ブロックの中身)だけを安全に差し替える。

編集アプリ(main.py)から使う薄いバックエンド。フロントマターや区切り
コメントには触れず、指定記事・指定言語の本文行だけを行単位で splice する。
保存後は必ず parse_series_file で再パースし、壊れていたら元に戻す。
"""

from __future__ import annotations

import os
import socket
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))

from build.series import (  # noqa: E402
    _ENDIF_RE,
    _IFDEF_RE,
    _SENTINEL_RE,
    SERIES_MAP,
    parse_series_file,
    select_lang_meta,
)

PYTHON = REPO / ".venv" / "bin" / "python"
BUILD_SCRIPT = REPO / "tools" / "build_article.py"
SERVE_SCRIPT = REPO / "tools" / "serve.py"
PREVIEW_PORT = int(os.environ.get("AISEED_PREVIEW_PORT", "8000"))

# シリーズファイル名 → (管理画面での表示名, アイコン用の短い区分)
SERIES_LABELS = {
    "blog.adoc": "Blog(構造分析ノート)",
    "insights.adoc": "Insights(構造分析)",
    "claude-debian.adoc": "Claudeと一緒に学ぶDebian",
    "claude-debian-server.adoc": "└ サーバー編",
    "ai-native-ways.adoc": "AIネイティブな仕事の作法",
    "ai-native-ways-software.adoc": "└ ソフトウェア開発編",
    "phosphorus-and-farming.adoc": "リンと農業",
    "fable.adoc": "Fable 5 が帰ってきた",
}


@dataclass
class Article:
    article_id: str
    slug: str
    date: str
    number: str
    title_ja: str
    title_en: str
    langs: list


def series_path(name: str) -> Path:
    return REPO / "articles" / name


def list_series() -> list[tuple[str, str]]:
    """存在するシリーズの [(ファイル名, 表示名)]。SERIES_LABELS の順。"""
    return [
        (name, label)
        for name, label in SERIES_LABELS.items()
        if series_path(name).exists()
    ]


def load_articles(name: str) -> list[Article]:
    units = parse_series_file(series_path(name))
    out = []
    for u in units:
        mj = select_lang_meta(u.meta, "ja")
        me = select_lang_meta(u.meta, "en")
        out.append(
            Article(
                article_id=u.article_id,
                slug=mj.get("slug", ""),
                date=mj.get("date", ""),
                number=mj.get("number", ""),
                title_ja=mj.get("title", ""),
                title_en=me.get("title", ""),
                langs=u.langs(),
            )
        )
    return out


def article_url(name: str, slug: str) -> str:
    """記事の公開URLパス(日本語版)。ビルダーのURL規則に合わせる。"""
    if name == "claude-debian.adoc":
        return f"/claude-debian/{slug.removeprefix('claude-debian-')}/"
    if name == "claude-debian-server.adoc":
        return f"/claude-debian/server/{slug.removeprefix('claude-debian-server-')}/"
    root = {
        "blog.adoc": "blog",
        "insights.adoc": "insights",
        "ai-native-ways.adoc": "ai-native-ways",
        "ai-native-ways-software.adoc": "ai-native-ways/software",
        "phosphorus-and-farming.adoc": "phosphorus-and-farming",
        "fable.adoc": "fable",
    }[name]
    return f"/{root}/{slug}/"


# ---------------------------------------------------------------------------
# 本文の読み書き(行単位 splice)
# ---------------------------------------------------------------------------


def _article_range(lines: list[str], article_id: str) -> tuple[int, int]:
    start = None
    for i, line in enumerate(lines):
        m = _SENTINEL_RE.match(line)
        if not m:
            continue
        if start is not None:
            return start, i
        if m.group(1) == article_id:
            start = i
    if start is None:
        raise KeyError(f"記事が見つかりません: {article_id}")
    return start, len(lines)


def _body_span(lines: list[str], article_id: str, lang: str) -> tuple[int, int]:
    """ifdef::lang-<lang>[] の中身の行範囲 [i0, i1)(デリミタ行は含まない)。"""
    s, e = _article_range(lines, article_id)
    open_line = None
    for i in range(s, e):
        m = _IFDEF_RE.match(lines[i])
        if m and m.group(1) == lang:
            open_line = i
        elif open_line is not None and _ENDIF_RE.match(lines[i]):
            return open_line + 1, i
    raise KeyError(f"{article_id} に {lang} の本文ブロックがありません")


def read_body(name: str, article_id: str, lang: str) -> str:
    lines = series_path(name).read_text(encoding="utf-8").split("\n")
    i0, i1 = _body_span(lines, article_id, lang)
    return "\n".join(lines[i0:i1]).strip("\n")


def save_body(name: str, article_id: str, lang: str, text: str) -> None:
    """本文を差し替えて保存する。保存後に再パースし、壊れていたら復元して
    ValueError を投げる(編集画面にエラーメッセージを出すため)。"""
    path = series_path(name)
    original = path.read_text(encoding="utf-8")
    lines = original.split("\n")
    i0, i1 = _body_span(lines, article_id, lang)
    new_lines = text.strip("\n").split("\n")
    lines[i0:i1] = new_lines
    path.write_text("\n".join(lines), encoding="utf-8")
    try:
        parse_series_file(path)
    except SystemExit as exc:
        path.write_text(original, encoding="utf-8")
        raise ValueError(str(exc)) from None


# ---------------------------------------------------------------------------
# ビルドとプレビューサーバー
# ---------------------------------------------------------------------------


def build_series(name: str) -> tuple[bool, str]:
    """このシリーズだけビルド。(成功?, 失敗時の出力末尾) を返す。"""
    result = subprocess.run(
        [str(PYTHON), str(BUILD_SCRIPT), str(series_path(name))],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    if result.returncode == 0:
        return True, ""
    return False, (result.stderr.strip() or result.stdout.strip())[-1500:]


def preview_running() -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", PREVIEW_PORT)) == 0


def start_preview() -> subprocess.Popen | None:
    """プレビューサーバー(ライブリロード付き serve.py)を起動する。
    すでに動いていれば何もしない。"""
    if preview_running():
        return None
    return subprocess.Popen(
        [str(PYTHON), str(SERVE_SCRIPT), "--port", str(PREVIEW_PORT),
         "--no-initial-build"],
        cwd=REPO,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
