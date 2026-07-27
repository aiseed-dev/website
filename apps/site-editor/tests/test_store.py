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
