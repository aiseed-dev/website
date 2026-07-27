import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from canon_search.chunker import chunk_paragraphs
from canon_search.store import Store


def test_chunker_packs_and_tracks_headings():
    text = (
        "1. Introduction\n\n"
        "This is the intro paragraph.\n\n"
        "2.1 Details\n\n" + ("x" * 700) + "\n\n" + ("y" * 700)
    )
    chunks = chunk_paragraphs(text, max_chars=1200)
    assert chunks[0][0] == "1. Introduction"
    assert any(h == "2.1 Details" for h, _ in chunks)
    # 詰め込み上限を大きく超えるチャンクがないこと(単独巨大段落は許容)
    assert all(len(t) <= 1500 for _, t in chunks)


def test_store_japanese_trigram_search():
    s = Store(":memory:")
    s.add_doc("law", "TEST", "テスト法", "https://example.com", "",
              [("第一条", "この法律は、軽微な利用について定める。"),
               ("第二条", "全く関係のない条文である。")])
    hits = s.search("軽微な利用")
    assert len(hits) == 1
    assert hits[0]["heading"] == "第一条"


def test_html_extractor_strips_chrome():
    from canon_search.fetchers import _TextExtractor
    ex = _TextExtractor()
    ex.feed("<html><head><title>T x</title><script>var a=1</script></head>"
            "<body><nav>menu</nav><p>hello</p><p>world</p></body></html>")
    text = "".join(ex.parts)
    assert "hello" in text and "world" in text
    assert "var a" not in text and "menu" not in text
    assert ex.title == "T x"


def test_crosslingual_span_verification():
    from canon_search.verify import span_in_source, verify_article
    src = 'coltivato in "pieno campo"; la raccolta deve essere eseguita a mano'
    # 逐語スパンは約物ゆれを無視して実在判定
    assert span_in_source("pieno campo", src)
    assert span_in_source("eseguita a mano", src)
    assert not span_in_source("mercati di Tokyo", src)
    # 日本語主張 + 伊語スパン: 実在スパンは通り、捏造は弾かれる
    lines = ["露地で栽培する。〔pieno campo〕[1]",
             "東京で高値。〔mercati di Tokyo〕[1]"]
    r = verify_article(lines, {1: src})
    assert r[0]["ok"] is True and r[0]["cite"] == 1
    assert r[1]["ok"] is False


def test_store_doc_chunks_ordered():
    s = Store(":memory:")
    s.add_doc("pdf", "D", "Doc", "u", "", [("A", "alpha"), ("B", "beta")])
    chunks = s.doc_chunks("D")
    assert [c["text"] for c in chunks] == ["alpha", "beta"]


def test_store_replaces_existing_doc():
    s = Store(":memory:")
    s.add_doc("rfc", "RFC 1", "Old", "u", "", [("", "old text here")])
    s.add_doc("rfc", "RFC 1", "New", "u", "", [("", "new text here")])
    docs = s.list_docs()
    assert len(docs) == 1 and docs[0]["title"] == "New"
    assert s.search("old text") == []
