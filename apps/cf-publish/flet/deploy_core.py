"""Cloudflare Pages Direct Upload — UI-agnostic deploy logic.

Ported from tools/cloudflare_pages_deploy.py in this repo, with two changes
so a GUI can drive it:

  * It RAISES exceptions instead of calling sys.exit / printing. The caller
    catches DeployError (and anything else) and shows it.
  * Progress is reported through an ``on_progress(str)`` callback instead of
    print(), so the GUI can append lines to a log area.

This implements the same half-official Direct Upload API that wrangler uses
under the hood (no npm / no wrangler needed). If Cloudflare changes the API
and this stops working, fall back to wrangler or the Git integration.

Credential load order (load_credentials): real environment variables first,
then ~/.config/cloudflare/pages.env (KEY=VALUE lines).
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
MAX_FILE_SIZE = 25 * 1024 * 1024  # Pages per-file limit (25 MiB)
BATCH_BYTES = 30 * 1024 * 1024  # rough target per upload call
BATCH_FILES = 500  # or this many files, whichever comes first

CONFIG_DIR = Path.home() / ".config" / "cloudflare"
ENV_FILE = CONFIG_DIR / "pages.env"

# Type of the progress callback. Default is a no-op.
ProgressFn = Callable[[str], None]


def _noop(_msg: str) -> None:
    pass


class DeployError(Exception):
    """Raised for any deploy failure (bad creds, API error, file too big...)."""


# ── credentials ────────────────────────────────────────────────────────────


def parse_env_file(path: Path = ENV_FILE) -> dict[str, str]:
    """Parse a KEY=VALUE env file into a dict (comments / blanks ignored)."""
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values


def load_credentials(path: Path = ENV_FILE) -> tuple[str | None, str | None]:
    """Return (token, account_id). Environment variables win over the file."""
    file_values = parse_env_file(path)
    token = os.environ.get("CLOUDFLARE_API_TOKEN") or file_values.get(
        "CLOUDFLARE_API_TOKEN"
    )
    account = os.environ.get("CLOUDFLARE_ACCOUNT_ID") or file_values.get(
        "CLOUDFLARE_ACCOUNT_ID"
    )
    return (token or None, account or None)


def save_credentials(
    token: str, account: str, path: Path = ENV_FILE
) -> None:
    """Write the env file (KEY=VALUE) and chmod it to 0600."""
    path.parent.mkdir(parents=True, exist_ok=True)
    body = (
        f"CLOUDFLARE_API_TOKEN={token.strip()}\n"
        f"CLOUDFLARE_ACCOUNT_ID={account.strip()}\n"
    )
    path.write_text(body, encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        # Non-POSIX filesystems may not support chmod; not fatal.
        pass


# ── file collection + hashing ──────────────────────────────────────────────


def file_hash(data: bytes, suffix: str) -> str:
    """Same scheme as wrangler: blake3(base64(content) + ext)[:32]."""
    b64 = base64.b64encode(data).decode()
    return blake3((b64 + suffix).encode()).hexdigest()[:32]


def collect(root: Path) -> dict[str, Path]:
    """Collect files under the public directory, keyed by url_path.

    Follows symlinks (files and dirs), guarding against cycles by tracking
    real directory paths. Skips dotfiles and dot-directories. Raises
    DeployError if a file exceeds the 25 MiB limit, or if nothing is found.
    """
    files: dict[str, Path] = {}
    seen_dirs: set[str] = set()
    for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
        real = os.path.realpath(dirpath)
        if real in seen_dirs:
            dirnames[:] = []
            continue
        seen_dirs.add(real)
        # Do not descend into hidden directories (.git etc.)
        dirnames[:] = sorted(n for n in dirnames if not n.startswith("."))
        d = Path(dirpath)
        for name in sorted(filenames):
            if name.startswith("."):
                continue
            p = d / name
            # is_file() follows links; broken links resolve to False.
            if not p.is_file():
                continue
            rel = p.relative_to(root).as_posix()
            if p.stat().st_size > MAX_FILE_SIZE:
                raise DeployError(
                    f"{p} exceeds the 25 MiB per-file limit for Pages"
                )
            files["/" + rel] = p
    if not files:
        raise DeployError(f"No files found under {root}")
    return files


def build_manifest(
    files: dict[str, Path],
) -> tuple[dict[str, str], dict[str, Path]]:
    """Build the manifest {url_path: hash} and by_hash {hash: path}."""
    manifest: dict[str, str] = {}
    by_hash: dict[str, Path] = {}
    for url_path, p in files.items():
        h = file_hash(p.read_bytes(), p.suffix.lstrip("."))
        manifest[url_path] = h
        by_hash[h] = p
    return manifest, by_hash


# ── Cloudflare Pages API ───────────────────────────────────────────────────


class Pages:
    def __init__(self, account_id: str, token: str):
        self.base = f"{API}/accounts/{account_id}/pages"
        self.client = httpx.Client(
            timeout=120.0, headers={"Authorization": f"Bearer {token}"}
        )

    def close(self) -> None:
        self.client.close()

    @staticmethod
    def _ok(resp: httpx.Response) -> dict:
        try:
            body = resp.json()
        except ValueError as exc:
            raise DeployError(
                f"Non-JSON response from {resp.request.url} "
                f"(HTTP {resp.status_code})"
            ) from exc
        if not body.get("success"):
            raise DeployError(
                f"API error at {resp.request.url}: "
                f"{json.dumps(body.get('errors'), ensure_ascii=False)}"
            )
        return body["result"]

    def project_exists(self, project: str) -> bool:
        resp = self.client.get(f"{self.base}/projects/{project}")
        return resp.status_code == 200 and resp.json().get("success", False)

    def create_project(self, project: str) -> None:
        self._ok(
            self.client.post(
                f"{self.base}/projects",
                json={"name": project, "production_branch": "main"},
            )
        )

    def upload_token(self, project: str) -> str:
        return self._ok(
            self.client.get(f"{self.base}/projects/{project}/upload-token")
        )["jwt"]

    def deploy(
        self, project: str, manifest: dict[str, str], branch: str
    ) -> dict:
        return self._ok(
            self.client.post(
                f"{self.base}/projects/{project}/deployments",
                data={"branch": branch},
                files={"manifest": (None, json.dumps(manifest))},
            )
        )


def upload_assets(
    jwt: str, by_hash: dict[str, Path], on_progress: ProgressFn = _noop
) -> None:
    """Upload only the assets Cloudflare is missing, then upsert all hashes."""
    client = httpx.Client(
        timeout=300.0, headers={"Authorization": f"Bearer {jwt}"}
    )

    def ok(resp: httpx.Response):
        try:
            body = resp.json()
        except ValueError as exc:
            raise DeployError(
                f"Non-JSON response from {resp.request.url} "
                f"(HTTP {resp.status_code})"
            ) from exc
        if not body.get("success"):
            raise DeployError(
                "Asset upload API error: "
                f"{json.dumps(body.get('errors'), ensure_ascii=False)}"
            )
        return body.get("result")

    try:
        missing = ok(
            client.post(
                f"{API}/pages/assets/check-missing",
                json={"hashes": list(by_hash)},
            )
        )
        on_progress(
            f"Uploading {len(missing)} / {len(by_hash)} files "
            "(the rest are already cached)"
        )

        batch: list[dict] = []
        batch_size = 0

        def flush() -> None:
            nonlocal batch, batch_size
            if batch:
                ok(client.post(f"{API}/pages/assets/upload", json=batch))
                on_progress(f"  sent {len(batch)} files")
                batch, batch_size = [], 0

        for h in missing:
            p = by_hash[h]
            data = p.read_bytes()
            ctype = (
                mimetypes.guess_type(p.name)[0] or "application/octet-stream"
            )
            batch.append(
                {
                    "key": h,
                    "value": base64.b64encode(data).decode(),
                    "metadata": {"contentType": ctype},
                    "base64": True,
                }
            )
            batch_size += len(data)
            if batch_size >= BATCH_BYTES or len(batch) >= BATCH_FILES:
                flush()
        flush()

        # Tell Cloudflare every hash is still in use (matches wrangler).
        ok(
            client.post(
                f"{API}/pages/assets/upsert-hashes",
                json={"hashes": list(by_hash)},
            )
        )
    finally:
        client.close()


# ── top-level orchestration ────────────────────────────────────────────────


def deploy(
    directory: str | Path,
    project: str,
    branch: str = "main",
    create: bool = True,
    token: str | None = None,
    account: str | None = None,
    on_progress: ProgressFn = _noop,
) -> str:
    """Deploy ``directory`` to the Pages ``project`` and return the URL.

    If token/account are not passed, they are loaded via load_credentials()
    (env vars, then ~/.config/cloudflare/pages.env). Raises DeployError on
    any failure; never calls sys.exit.
    """
    if token is None or account is None:
        loaded_token, loaded_account = load_credentials()
        token = token or loaded_token
        account = account or loaded_account
    if not token or not account:
        raise DeployError(
            "CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID must be set "
            f"(env vars or {ENV_FILE})"
        )

    root = Path(directory)
    if not root.is_dir():
        raise DeployError(f"Directory not found: {root}")

    on_progress(f"Scanning {root} ...")
    files = collect(root)
    manifest, by_hash = build_manifest(files)
    on_progress(f"{len(files)} files ({len(by_hash)} unique)")

    pages = Pages(account, token)
    try:
        on_progress(f"Checking project '{project}' ...")
        if not pages.project_exists(project):
            if create:
                on_progress(f"Creating project '{project}' ...")
                pages.create_project(project)
            else:
                raise DeployError(f"Project does not exist: {project}")

        on_progress("Requesting upload token ...")
        jwt = pages.upload_token(project)

        upload_assets(jwt, by_hash, on_progress=on_progress)

        on_progress(f"Creating deployment on branch '{branch}' ...")
        result = pages.deploy(project, manifest, branch)
    finally:
        pages.close()

    url = result.get("url", "(URL unknown)")
    on_progress(f"Deploy complete: {url}")
    return url
