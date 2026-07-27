"""シリーズ .adoc の読み書き——本文(ifdef ブロックの中身)だけを安全に差し替える。

編集アプリ(main.py)から使う薄いバックエンド。フロントマターや区切り
コメントには触れず、指定記事・指定言語の本文行だけを行単位で splice する。
保存後は必ず parse_series_file で再パースし、壊れていたら元に戻す。
"""

from __future__ import annotations

import datetime
import os
import re
import shutil
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
    draft: bool = False


def is_draft_meta(meta: dict) -> bool:
    return str(meta.get("draft", "")).strip().lower() in ("true", "yes", "1")


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
                draft=is_draft_meta(u.meta),
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


def _write_validated(path: Path, original: str, text: str) -> None:
    """書き込み後に再パース検証し、壊れていたら復元して ValueError。"""
    path.write_text(text, encoding="utf-8")
    try:
        parse_series_file(path)
    except SystemExit as exc:
        path.write_text(original, encoding="utf-8")
        raise ValueError(str(exc)) from None


# ---------------------------------------------------------------------------
# フロントマターの読み書き
# ---------------------------------------------------------------------------


def _frontmatter_span(lines: list[str], article_id: str) -> tuple[int, int]:
    """フロントマターの中身の行範囲 [i0, i1)(--- 行は含まない)。"""
    s, e = _article_range(lines, article_id)
    first = None
    for i in range(s, e):
        if lines[i].strip() == "---":
            if first is None:
                first = i
            else:
                return first + 1, i
    raise KeyError(f"{article_id} のフロントマターが見つかりません")


def read_meta_raw(name: str, article_id: str) -> dict:
    """統合フロントマターを接尾辞キー(key.ja/key.en)のまま順序付きで返す。"""
    lines = series_path(name).read_text(encoding="utf-8").split("\n")
    i0, i1 = _frontmatter_span(lines, article_id)
    meta = {}
    for line in lines[i0:i1]:
        if ":" in line:
            k, v = line.split(":", 1)
            v = v.strip()
            if v.startswith('"') and v.endswith('"'):
                v = v[1:-1]
            meta[k.strip()] = v
    return meta


def save_meta(name: str, article_id: str, meta: dict) -> None:
    """フロントマターを dict の内容で置き換える(空値のキーは書かない)。"""
    path = series_path(name)
    original = path.read_text(encoding="utf-8")
    lines = original.split("\n")
    i0, i1 = _frontmatter_span(lines, article_id)
    lines[i0:i1] = [
        f"{k}: {v}" for k, v in meta.items() if str(v).strip() != ""
    ]
    _write_validated(path, original, "\n".join(lines))


# ---------------------------------------------------------------------------
# 記事の新規作成・削除・並び替え
# ---------------------------------------------------------------------------


def next_defaults(name: str) -> dict:
    """新規記事の既定値(次の番号・ラベル雛形・番号キーの有無)。"""
    units = parse_series_file(series_path(name))
    nums = []
    widths = []
    for u in units:
        m = re.match(r"(\d+)", u.article_id.split("/")[-1])
        if m:
            nums.append(int(m.group(1)))
            widths.append(len(m.group(1)))
    # 桁数は既存IDに合わせる(blogは001形式、章ものは01形式)
    width = max(widths) if widths else 2
    last_label = units[-1].meta.get("label", "") if units else ""
    return {
        "next_num": (max(nums) + 1) if nums else 1,
        "width": width,
        "label": last_label,
        "numbered": any("number" in u.meta for u in units),
    }


def add_article(name: str, slug: str, title_ja: str, title_en: str = "") -> str:
    """新しい記事の節をシリーズ末尾に追加する。**下書き(draft: true)で作る**
    (「公開」に切り替えるまでサイトには出ない)。記事IDを返す。"""
    slug = slug.strip().lower()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
        raise ValueError("スラッグは半角英小文字・数字・ハイフンで入力してください")
    d = next_defaults(name)
    num = str(d["next_num"]).zfill(d["width"])
    article_id = f"{num}-{slug}"

    path = series_path(name)
    original = path.read_text(encoding="utf-8")
    if any(u.article_id == article_id or u.meta.get("slug") == slug
           for u in parse_series_file(path)):
        raise ValueError(f"同じスラッグの記事があります: {slug}")

    today = datetime.date.today().strftime("%Y.%m.%d")
    label = d["label"]
    if label:
        # 「AI Native 01」のような連番ラベルは新しい番号に置き換える
        label = re.sub(r"\d+\s*$", lambda m: num.zfill(len(m.group(0).strip())), label)

    meta_lines = [f"slug: {slug}"]
    if d["numbered"]:
        meta_lines.append(f"number: {num}")
    meta_lines.append(f"date: {today}")
    if label:
        meta_lines.append(f"label: {label}")
    if title_en:
        meta_lines += [f"title.ja: {title_ja}", f"title.en: {title_en}"]
    else:
        meta_lines.append(f"title.ja: {title_ja}")
    meta_lines.append("draft: true")

    section = [f"// ===== article: {article_id} =====", "---", *meta_lines, "---",
               "ifdef::lang-ja[]", f"= {title_ja}", "", "(本文をここに書く)",
               "endif::[]"]
    if title_en:
        section += ["ifdef::lang-en[]", f"= {title_en}", "",
                    "(Write the English body here)", "endif::[]"]

    text = original.rstrip("\n") + "\n\n" + "\n".join(section) + "\n"
    _write_validated(path, original, text)
    return article_id


def delete_article(name: str, article_id: str) -> None:
    """記事の節を削除する(復元は git でできる——ゴミ箱は無い)。"""
    path = series_path(name)
    original = path.read_text(encoding="utf-8")
    lines = original.split("\n")
    s, e = _article_range(lines, article_id)
    del lines[s:e]
    _write_validated(path, original, "\n".join(lines))


def move_article(name: str, article_id: str, delta: int) -> bool:
    """記事を前後に動かす(delta=-1 で上、+1 で下)。並び順は prev/next
    連鎖にそのまま反映される。動かせなければ False。"""
    path = series_path(name)
    original = path.read_text(encoding="utf-8")
    lines = original.split("\n")
    units = parse_series_file(path)
    ids = [u.article_id for u in units]
    idx = ids.index(article_id)
    other = idx + delta
    if other < 0 or other >= len(ids):
        return False
    first_id, second_id = (ids[other], ids[idx]) if delta < 0 else (ids[idx], ids[other])
    sA, eA = _article_range(lines, first_id)
    sB, eB = _article_range(lines, second_id)
    block_a, between, block_b = lines[sA:eA], lines[eA:sB], lines[sB:eB]
    lines[sA:eB] = block_b + between + block_a
    _write_validated(path, original, "\n".join(lines))
    return True


# ---------------------------------------------------------------------------
# 資産(画像・PDF)
# ---------------------------------------------------------------------------

ASSET_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".avif", ".pdf"}


def assets_dir(name: str, article_id: str) -> Path:
    stem = name[: -len(".adoc")]
    return REPO / "articles" / "assets" / stem / article_id


def list_assets(name: str, article_id: str) -> list[str]:
    d = assets_dir(name, article_id)
    if not d.is_dir():
        return []
    return sorted(f.name for f in d.iterdir()
                  if f.is_file() and f.suffix.lower() in ASSET_EXTS)


def add_asset(name: str, article_id: str, src: str | None = None,
              data: bytes | None = None, filename: str | None = None) -> str:
    """画像・PDF を記事の資産フォルダへ取り込む(パスまたはバイト列)。"""
    fname = filename or (Path(src).name if src else None)
    if not fname:
        raise ValueError("ファイル名がありません")
    if Path(fname).suffix.lower() not in ASSET_EXTS:
        raise ValueError(f"対応していない形式です: {fname}")
    d = assets_dir(name, article_id)
    d.mkdir(parents=True, exist_ok=True)
    dest = d / fname
    if src:
        shutil.copy2(src, dest)
    elif data is not None:
        dest.write_bytes(data)
    else:
        raise ValueError("src か data のどちらかが必要です")
    return dest.name


# ---------------------------------------------------------------------------
# デプロイと変更の記録(git)
# ---------------------------------------------------------------------------

DEPLOY_SCRIPT = REPO / "tools" / "cloudflare_pages_deploy.py"
CF_PROJECT = "aiseed-dev"


def deploy(branch: str) -> tuple[bool, str]:
    """Cloudflare Pages へ公開する。branch は 'preview' か 'main'。"""
    result = subprocess.run(
        [str(PYTHON), str(DEPLOY_SCRIPT), "html",
         "--project", CF_PROJECT, "--branch", branch],
        capture_output=True, text=True, cwd=REPO, timeout=900,
    )
    out = (result.stdout.strip() + "\n" + result.stderr.strip()).strip()
    return result.returncode == 0, out[-1500:]


def git_dirty_count() -> int:
    result = subprocess.run(
        ["git", "status", "--porcelain", "articles"],
        capture_output=True, text=True, cwd=REPO,
    )
    return len([l for l in result.stdout.splitlines() if l.strip()])


def git_commit(message: str) -> tuple[bool, str]:
    """articles/ の変更をコミットする(記事編集の記録)。"""
    add = subprocess.run(["git", "add", "articles"], capture_output=True,
                         text=True, cwd=REPO)
    if add.returncode != 0:
        return False, add.stderr[-500:]
    result = subprocess.run(
        ["git", "commit", "-m", message or "記事を更新"],
        capture_output=True, text=True, cwd=REPO,
    )
    out = (result.stdout.strip() + "\n" + result.stderr.strip()).strip()
    return result.returncode == 0, out[-800:]


def git_recent(n: int = 5) -> list[str]:
    result = subprocess.run(
        ["git", "log", "--oneline", f"-{n}"],
        capture_output=True, text=True, cwd=REPO,
    )
    return result.stdout.strip().split("\n") if result.returncode == 0 else []


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
