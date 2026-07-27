"""SQLite ストア — 文書と断片(チャンク)、FTS5 trigram 全文索引。

trigram トークナイザは日本語を分かち書きなしで索引できる。
制約: 3文字未満の検索語は照合できない(trigram の性質)。
"""

from __future__ import annotations

import sqlite3
import unicodedata
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS docs(
  id INTEGER PRIMARY KEY,
  source TEXT NOT NULL,
  doc_key TEXT NOT NULL,
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  license TEXT NOT NULL DEFAULT '',
  fetched_at TEXT NOT NULL,
  UNIQUE(source, doc_key)
);
CREATE TABLE IF NOT EXISTS chunks(
  id INTEGER PRIMARY KEY,
  doc_id INTEGER NOT NULL REFERENCES docs(id) ON DELETE CASCADE,
  seq INTEGER NOT NULL,
  heading TEXT NOT NULL DEFAULT '',
  text TEXT NOT NULL
);
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
  text, content='chunks', content_rowid='id', tokenize='trigram'
);
CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
  INSERT INTO chunks_fts(rowid, text) VALUES (new.id, new.text);
END;
CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
  INSERT INTO chunks_fts(chunks_fts, rowid, text) VALUES('delete', old.id, old.text);
END;
"""


def norm(s: str) -> str:
    return unicodedata.normalize("NFKC", s)


def _like_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


class Store:
    def __init__(self, path: str | Path = ":memory:"):
        if path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(path))
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript(SCHEMA)

    def add_doc(self, source: str, doc_key: str, title: str, url: str,
                license: str, chunks: list[tuple[str, str]]) -> int:
        """文書を(既存なら置き換えて)登録し、チャンク数を返す。"""
        cur = self.db.cursor()
        row = cur.execute(
            "SELECT id FROM docs WHERE source=? AND doc_key=?", (source, doc_key)
        ).fetchone()
        if row:
            cur.execute("DELETE FROM chunks WHERE doc_id=?", (row[0],))
            cur.execute("DELETE FROM docs WHERE id=?", (row[0],))
        cur.execute(
            "INSERT INTO docs(source, doc_key, title, url, license, fetched_at)"
            " VALUES(?,?,?,?,?,datetime('now'))",
            (source, doc_key, norm(title), url, license),
        )
        doc_id = cur.lastrowid
        for i, (heading, text) in enumerate(chunks):
            cur.execute(
                "INSERT INTO chunks(doc_id, seq, heading, text) VALUES(?,?,?,?)",
                (doc_id, i, norm(heading), norm(text)),
            )
        self.db.commit()
        return len(chunks)

    def search(self, query: str, k: int = 8) -> list[dict]:
        """AND 検索。trigram が照合できない3文字未満の語は LIKE で補完する。"""
        terms = [t for t in norm(query).split() if t]
        if not terms:
            return []
        long_terms = [t for t in terms if len(t) >= 3]
        short_terms = [t for t in terms if len(t) < 3]
        keys = ("source", "doc_key", "title", "url", "heading", "text", "score")

        base = """
            SELECT d.source, d.doc_key, d.title, d.url, c.heading, c.text, {score}
            FROM {from_} JOIN docs d ON d.id = c.doc_id
            WHERE {where} LIMIT ?
        """
        if long_terms:
            fts_q = " AND ".join(
                '"%s"' % t.replace('"', '""') for t in long_terms)
            where = "chunks_fts MATCH ?"
            params: list = [fts_q]
            for t in short_terms:
                where += " AND c.text LIKE ? ESCAPE '\\'"
                params.append("%" + _like_escape(t) + "%")
            sql = base.format(
                score="bm25(chunks_fts) AS score",
                from_="chunks_fts JOIN chunks c ON c.id = chunks_fts.rowid",
                where=where + " ORDER BY score",
            )
        else:
            # 短い語だけの検索: 走査(個人規模のコーパスでは十分速い)。
            # スコアは出現回数の合計の負数(小さいほど上位、bm25 と向きを揃える)。
            occurs = " + ".join(
                "(length(c.text) - length(replace(c.text, ?, ''))) / length(?)"
                for _ in short_terms)
            where = " AND ".join(
                "c.text LIKE ? ESCAPE '\\'" for _ in short_terms)
            params = []
            for t in short_terms:
                params += [t, t]
            for t in short_terms:
                params.append("%" + _like_escape(t) + "%")
            sql = base.format(
                score=f"-({occurs}) AS score",
                from_="chunks c",
                where=where + " ORDER BY score",
            )
        rows = self.db.execute(sql, (*params, k)).fetchall()
        return [dict(zip(keys, r)) for r in rows]

    def doc_chunks(self, doc_key: str) -> list[dict]:
        """1文書の全チャンクを seq 順で返す(辞典生成の grounding 用)。"""
        rows = self.db.execute(
            "SELECT d.source, d.doc_key, d.title, d.url, c.heading, c.text"
            " FROM chunks c JOIN docs d ON d.id = c.doc_id"
            " WHERE d.doc_key = ? ORDER BY c.seq", (doc_key,)
        ).fetchall()
        keys = ("source", "doc_key", "title", "url", "heading", "text")
        return [dict(zip(keys, r)) for r in rows]

    def list_docs(self) -> list[dict]:
        rows = self.db.execute(
            "SELECT d.source, d.doc_key, d.title, d.url, d.fetched_at,"
            " (SELECT count(*) FROM chunks c WHERE c.doc_id = d.id)"
            " FROM docs d ORDER BY d.source, d.doc_key"
        ).fetchall()
        keys = ("source", "doc_key", "title", "url", "fetched_at", "chunks")
        return [dict(zip(keys, r)) for r in rows]
