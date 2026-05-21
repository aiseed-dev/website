"""Smoke tests for the replacement table."""

from __future__ import annotations

from debian_migrate.data.replacements import TABLE, find_replacement


def test_table_not_empty():
    assert len(TABLE) > 0


def test_match_microsoft_word():
    entry = find_replacement("Microsoft Word 2021")
    assert entry is not None
    assert "LibreOffice Writer" in entry["alternatives"]


def test_match_adobe_photoshop_2024():
    entry = find_replacement("Adobe Photoshop 2024")
    assert entry is not None
    assert entry["confidence"] in ("ok", "review", "missing")


def test_no_match_unknown_app():
    assert find_replacement("MyTotallyMadeUpApp 1.0") is None


def test_case_insensitive_match():
    e1 = find_replacement("VISUAL STUDIO CODE")
    e2 = find_replacement("Visual Studio Code")
    assert e1 is not None and e2 is not None
    assert e1 == e2
