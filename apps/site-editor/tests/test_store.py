"""store.py のテスト——本文 splice の安全性が主対象。"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import store  # noqa: E402

SAMPLE = """\
// テスト用シリーズ
// ===== article: 01-first =====
---
slug: first
number: 01
title.ja: 最初の記事
title.en: First article
---
ifdef::lang-ja[]
= 最初の記事

日本語の本文。
endif::[]
ifdef::lang-en[]
= First article

English body.
endif::[]

// ===== article: 02-second =====
---
slug: second
number: 02
title.ja: 二つ目
---
ifdef::lang-ja[]
= 二つ目

本文その2。
endif::[]
"""


@pytest.fixture
def series_file(tmp_path, monkeypatch):
    d = tmp_path / "articles"
    d.mkdir()
    f = d / "blog.adoc"
    f.write_text(SAMPLE, encoding="utf-8")
    monkeypatch.setattr(store, "REPO", tmp_path)
    return f


def test_read_body(series_file):
    assert store.read_body("blog.adoc", "01-first", "ja") == (
        "= 最初の記事\n\n日本語の本文。"
    )
    assert "English body." in store.read_body("blog.adoc", "01-first", "en")
    assert "本文その2。" in store.read_body("blog.adoc", "02-second", "ja")


def test_save_body_roundtrip_touches_only_target_block(series_file):
    before = series_file.read_text(encoding="utf-8")
    store.save_body("blog.adoc", "01-first", "ja", "= 最初の記事\n\n書き換えた本文。")
    after = series_file.read_text(encoding="utf-8")
    assert "書き換えた本文。" in after
    assert "日本語の本文。" not in after
    # 他言語・他記事・フロントマターは無傷
    assert "English body." in after
    assert "本文その2。" in after
    assert "title.en: First article" in after
    # 差し替え対象以外の行は変わらない
    changed = set(before.split("\n")) ^ set(after.split("\n"))
    assert changed == {"日本語の本文。", "書き換えた本文。"}


def test_save_body_rejects_broken_edit_and_restores(series_file):
    before = series_file.read_text(encoding="utf-8")
    # 記事の区切りを本文に紛れ込ませる(次の記事のフロントマターが壊れて
    # パースが落ちる)→ 保存は拒否され、ファイルは元のまま
    with pytest.raises(ValueError):
        store.save_body(
            "blog.adoc", "01-first", "ja",
            "本文\n// ===== article: 99-broken =====\nゴミ",
        )
    assert series_file.read_text(encoding="utf-8") == before


def test_unknown_article_raises(series_file):
    with pytest.raises(KeyError):
        store.read_body("blog.adoc", "99-nope", "ja")


def test_missing_lang_raises(series_file):
    with pytest.raises(KeyError):
        store.read_body("blog.adoc", "02-second", "en")


def test_article_url_rules():
    assert store.article_url("blog.adoc", "foo") == "/blog/foo/"
    assert store.article_url("claude-debian.adoc", "claude-debian-setup") == \
        "/claude-debian/setup/"
    assert store.article_url("claude-debian-server.adoc",
                             "claude-debian-server-dns") == \
        "/claude-debian/server/dns/"
    assert store.article_url("ai-native-ways-software.adoc", "auth") == \
        "/ai-native-ways/software/auth/"


def test_load_articles_real_repo():
    """実リポジトリのシリーズが読めて、記事メタが取れること。"""
    arts = store.load_articles("fable.adoc")
    assert len(arts) == 9
    assert arts[0].slug
    assert arts[0].langs == ["ja"]


def test_meta_roundtrip(series_file):
    meta = store.read_meta_raw("blog.adoc", "01-first")
    assert meta["title.ja"] == "最初の記事"
    meta["subtitle.ja"] = "追加のサブタイトル"
    store.save_meta("blog.adoc", "01-first", meta)
    again = store.read_meta_raw("blog.adoc", "01-first")
    assert again["subtitle.ja"] == "追加のサブタイトル"
    assert "English body." in store.read_body("blog.adoc", "01-first", "en")


def test_add_article_is_draft_and_parseable(series_file):
    aid = store.add_article("blog.adoc", "new-post", "新しい記事", "New post")
    assert aid == "03-new-post"
    arts = store.load_articles("blog.adoc")
    assert arts[-1].slug == "new-post"
    assert arts[-1].draft is True
    assert arts[-1].langs == ["ja", "en"]


def test_add_article_rejects_bad_slug_and_duplicate(series_file):
    with pytest.raises(ValueError):
        store.add_article("blog.adoc", "日本語スラッグ", "x")
    with pytest.raises(ValueError):
        store.add_article("blog.adoc", "first", "重複")


def test_delete_article_removes_only_target(series_file):
    store.delete_article("blog.adoc", "01-first")
    arts = store.load_articles("blog.adoc")
    assert [a.article_id for a in arts] == ["02-second"]
    assert "本文その2。" in store.read_body("blog.adoc", "02-second", "ja")


def test_move_article_swaps_order(series_file):
    assert store.move_article("blog.adoc", "02-second", -1) is True
    arts = store.load_articles("blog.adoc")
    assert [a.article_id for a in arts] == ["02-second", "01-first"]
    # 端では動かない
    assert store.move_article("blog.adoc", "02-second", -1) is False


def test_assets_add_and_list(series_file, tmp_path):
    img = tmp_path / "photo.jpg"
    img.write_bytes(b"\xff\xd8fake")
    name = store.add_asset("blog.adoc", "01-first", src=str(img))
    assert name == "photo.jpg"
    assert store.list_assets("blog.adoc", "01-first") == ["photo.jpg"]
    name2 = store.add_asset("blog.adoc", "01-first", data=b"pdf", filename="doc.pdf")
    assert name2 == "doc.pdf"
    with pytest.raises(ValueError):
        store.add_asset("blog.adoc", "01-first", data=b"x", filename="evil.exe")


# --- 取り込み(Claude Docs などの Markdown 書き出し)--------------------------

IMPORT_MD = """\
# 取り込んだ記事

**太字**のある段落と、[リンク](https://example.com/)。

## 節の見出し

- 箇条書き 1
- 箇条書き 2

> 引用の行

| 見出し1 | 見出し2 |
|---|---|
| 値1 | 値2 |
"""


def test_markdown_to_adoc_extracts_title_and_converts():
    title, body, warnings = store.markdown_to_adoc(IMPORT_MD)
    assert title == "取り込んだ記事"
    # 見出し・強調・リンク・箇条書き・引用・表が AsciiDoc の語彙になる
    assert body.startswith("*太字*のある段落と、https://example.com/[リンク]。")
    assert "== 節の見出し" in body
    assert "* 箇条書き 1" in body
    assert "____" in body
    assert "|===" in body
    # タイトル行は本文に残さない(取り込み側が `= 題` を付け直す)
    assert "# 取り込んだ記事" not in body
    assert "= 取り込んだ記事" not in body
    assert warnings == []


def test_import_markdown_creates_draft_with_converted_body(series_file):
    article_id, warnings = store.import_markdown(
        "blog.adoc", IMPORT_MD, "torikomi", "取り込んだ記事")
    assert article_id == "03-torikomi"
    assert warnings == []
    # 下書きとして作られる——公開に切り替えるまでサイトに出ない
    assert store.is_draft_meta(store.read_meta_raw("blog.adoc", article_id))
    body = store.read_body("blog.adoc", article_id, "ja")
    assert body.startswith("= 取り込んだ記事\n\n")
    assert "== 節の見出し" in body
    # 既存の記事は無傷
    assert "日本語の本文。" in series_file.read_text(encoding="utf-8")


def test_import_markdown_uses_heading_when_title_omitted(series_file):
    article_id, _ = store.import_markdown("blog.adoc", IMPORT_MD, "midashi", "")
    meta = store.read_meta_raw("blog.adoc", article_id)
    assert meta["title.ja"] == "取り込んだ記事"


def test_import_markdown_rejects_empty_and_titleless(series_file):
    with pytest.raises(ValueError):
        store.import_markdown("blog.adoc", "   ", "kara", "題")
    with pytest.raises(ValueError):
        # 見出しもタイトル欄も無ければ、何の記事か決まらない
        store.import_markdown("blog.adoc", "本文だけ。\n", "nashi", "")


def test_import_markdown_leaves_series_untouched_on_failure(series_file):
    before = series_file.read_text(encoding="utf-8")
    with pytest.raises(ValueError):
        store.import_markdown("blog.adoc", IMPORT_MD, "Bad Slug!", "題")
    assert series_file.read_text(encoding="utf-8") == before


# --- site.json で宣言したシリーズ ---------------------------------------------

SITE_JSON = """\
{"builder": {"series": [
  {"file": "newseries.adoc", "label": "新しい連載", "url_base": "/newseries"},
  {"file": "blog.adoc", "label": "Blog"}
]}}
"""


@pytest.fixture
def site_with_custom(tmp_path, monkeypatch):
    d = tmp_path / "articles"
    d.mkdir()
    (d / "blog.adoc").write_text(SAMPLE, encoding="utf-8")
    (d / "newseries.adoc").write_text(SAMPLE, encoding="utf-8")
    (tmp_path / "site.json").write_text(SITE_JSON, encoding="utf-8")
    monkeypatch.setattr(store, "REPO", tmp_path)
    return tmp_path


def test_list_series_includes_site_json_series_first(site_with_custom):
    got = store.list_series()
    # site.json の順と表示名に従う
    assert got[0] == ("newseries.adoc", "新しい連載")
    assert ("blog.adoc", "Blog") in got


def test_list_series_falls_back_to_builtin_labels(series_file):
    # site.json が無いサイトでは、これまでどおり組み込みの表を使う
    got = store.list_series()
    assert got == [("blog.adoc", "Blog(構造分析ノート)")]


def test_article_url_uses_url_base_for_site_json_series(site_with_custom):
    assert store.article_url("newseries.adoc", "aru-kiji") == "/newseries/aru-kiji/"


def test_article_url_keeps_builtin_rules(series_file):
    assert store.article_url("blog.adoc", "aru-kiji") == "/blog/aru-kiji/"
    assert store.article_url("ai-native-ways-software.adoc", "x") == "/ai-native-ways/software/x/"
