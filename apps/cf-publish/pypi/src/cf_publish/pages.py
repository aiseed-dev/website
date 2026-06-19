"""Cloudflare Pages 直接アップロード（Direct Upload API）の UI 非依存ロジック。

`tools/cloudflare_pages_deploy.py`（リポジトリの参照実装）と同じ振る舞いを、
パッケージとして配れる形に整えたもの。CLI 向けの `sys.exit` / `print` は持たず、
- エラーは ``PagesError`` を raise する
- 進捗は ``on_progress(str)`` コールバックで通知する
ので、CLI でも GUI でも同じコアを再利用できる。
"""

from __future__ import annotations

import base64
import json
import mimetypes
import os
from pathlib import Path
from typing import Callable

import httpx
from blake3 import blake3

API = "https://api.cloudflare.com/client/v4"
MAX_FILE_SIZE = 25 * 1024 * 1024  # Pages の 1 ファイル上限（25MiB）
BATCH_BYTES = 30 * 1024 * 1024  # 1 回のアップロード呼び出しの目安
ENV_FILE = Path.home() / ".config" / "cloudflare" / "pages.env"

ProgressFn = Callable[[str], None]


class PagesError(Exception):
    """デプロイ中の想定エラー（認証不足・API エラー・入力不正など）。"""


def _noop(_msg: str) -> None:
    pass


def load_env_file(path: Path = ENV_FILE) -> None:
    """KEY=VALUE 形式の env ファイルを読む（既に環境変数があればそちらを優先）。"""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def file_hash(data: bytes, suffix: str) -> str:
    """wrangler と同じ方式：blake3(base64(中身) + 拡張子) の先頭 32 桁。"""
    b64 = base64.b64encode(data).decode()
    return blake3((b64 + suffix).encode()).hexdigest()[:32]


def collect(root: Path) -> dict[str, Path]:
    """公開ディレクトリ配下のファイルを集める（隠しファイル/ディレクトリは除外）。"""
    files: dict[str, Path] = {}
    seen_dirs: set[str] = set()
    for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
        real = os.path.realpath(dirpath)
        if real in seen_dirs:
            dirnames[:] = []
            continue
        seen_dirs.add(real)
        dirnames[:] = sorted(n for n in dirnames if not n.startswith("."))
        d = Path(dirpath)
        for name in sorted(filenames):
            if name.startswith("."):
                continue
            p = d / name
            if not p.is_file():
                continue
            rel = p.relative_to(root).as_posix()
            if p.stat().st_size > MAX_FILE_SIZE:
                raise PagesError(f"{p} が 25MiB を超えている（Pages の上限）")
            files["/" + rel] = p
    if not files:
        raise PagesError(f"{root} にファイルがない")
    return files


class Pages:
    def __init__(self, account_id: str, token: str):
        self.base = f"{API}/accounts/{account_id}/pages"
        self.client = httpx.Client(
            timeout=120.0, headers={"Authorization": f"Bearer {token}"}
        )

    def _ok(self, resp: httpx.Response) -> dict:
        body = resp.json()
        if not body.get("success"):
            raise PagesError(
                f"API エラー: {resp.request.url}\n"
                f"{json.dumps(body.get('errors'), ensure_ascii=False)}"
            )
        return body["result"]

    def project_exists(self, project: str) -> bool:
        resp = self.client.get(f"{self.base}/projects/{project}")
        return resp.status_code == 200 and resp.json().get("success", False)

    def create_project(self, project: str) -> None:
        self._ok(self.client.post(
            f"{self.base}/projects",
            json={"name": project, "production_branch": "main"},
        ))

    def upload_token(self, project: str) -> str:
        return self._ok(
            self.client.get(f"{self.base}/projects/{project}/upload-token")
        )["jwt"]

    def deploy(self, project: str, manifest: dict[str, str], branch: str) -> dict:
        return self._ok(self.client.post(
            f"{self.base}/projects/{project}/deployments",
            data={"branch": branch},
            files={"manifest": (None, json.dumps(manifest))},
        ))


def upload_assets(token: str, by_hash: dict[str, Path], on_progress: ProgressFn) -> None:
    client = httpx.Client(
        timeout=300.0, headers={"Authorization": f"Bearer {token}"}
    )

    def ok(resp: httpx.Response):
        body = resp.json()
        if not body.get("success"):
            raise PagesError(
                f"アップロード API エラー: "
                f"{json.dumps(body.get('errors'), ensure_ascii=False)}"
            )
        return body.get("result")

    missing = ok(client.post(
        f"{API}/pages/assets/check-missing",
        json={"hashes": list(by_hash)},
    ))
    on_progress(f"アップロード対象: {len(missing)} / {len(by_hash)} ファイル（残りはキャッシュ済み）")

    batch: list[dict] = []
    batch_size = 0

    def flush():
        nonlocal batch, batch_size
        if batch:
            ok(client.post(f"{API}/pages/assets/upload", json=batch))
            on_progress(f"  {len(batch)} ファイル送信")
            batch, batch_size = [], 0

    for h in missing:
        p = by_hash[h]
        data = p.read_bytes()
        ctype = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        batch.append({
            "key": h,
            "value": base64.b64encode(data).decode(),
            "metadata": {"contentType": ctype},
            "base64": True,
        })
        batch_size += len(data)
        if batch_size >= BATCH_BYTES or len(batch) >= 500:
            flush()
    flush()

    ok(client.post(f"{API}/pages/assets/upsert-hashes",
                   json={"hashes": list(by_hash)}))


def deploy(directory: str | Path, project: str, branch: str = "main",
           create: bool = True, on_progress: ProgressFn = _noop) -> str:
    """ディレクトリを Pages プロジェクトへデプロイし、URL を返す。

    トークンは環境変数 → ~/.config/cloudflare/pages.env の順で読む。
    エラー時は ``PagesError`` を投げる。進捗は ``on_progress`` に通知する。
    """
    load_env_file()
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    account = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    if not token or not account:
        raise PagesError(
            "CLOUDFLARE_API_TOKEN と CLOUDFLARE_ACCOUNT_ID を"
            f"環境変数か {ENV_FILE} に設定すること"
        )

    root = Path(directory)
    if not root.is_dir():
        raise PagesError(f"ディレクトリがない: {root}")

    files = collect(root)
    manifest: dict[str, str] = {}
    by_hash: dict[str, Path] = {}
    for url_path, p in files.items():
        h = file_hash(p.read_bytes(), p.suffix.lstrip("."))
        manifest[url_path] = h
        by_hash[h] = p
    on_progress(f"{len(files)} ファイル（一意 {len(by_hash)}）")

    pages = Pages(account, token)
    if not pages.project_exists(project):
        if create:
            pages.create_project(project)
            on_progress(f"プロジェクトを作成: {project}")
        else:
            raise PagesError(f"プロジェクトがない: {project}")

    jwt = pages.upload_token(project)
    upload_assets(jwt, by_hash, on_progress)
    result = pages.deploy(project, manifest, branch)
    url = result.get("url", "(URL 不明)")
    on_progress(f"デプロイ完了: {url}")
    return url
