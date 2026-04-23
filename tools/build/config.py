"""Site configuration and Jinja2 environment for the article builder.

Most values here (SITE_ROOT, SITE_URL, ARTICLES_DIR, env, ...) are rebound by
configure_site() after CLI parsing. Other modules should reference them as
attributes on this module (e.g. `config.SITE_URL`) so the live value is
observed after configuration, rather than `from .config import SITE_URL`
which captures the pre-configure default.
"""

import json
import os
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


_BUNDLED_TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

_DEFAULT_OG_IMAGE = "https://aiseed.dev/images/IMG_3285.jpg"
_DEFAULT_SITE_URL = "https://aiseed.dev"

DEFAULT_OG_IMAGE = _DEFAULT_OG_IMAGE
SITE_URL = _DEFAULT_SITE_URL

# Site-specific paths. configure_site() overwrites these before any build runs.
SITE_ROOT: Path = Path(__file__).parent.parent.parent
ARTICLES_DIR: Path = SITE_ROOT / "articles"
BLOG_DIR: Path = SITE_ROOT / "blog"
OUTPUT_BASE: Path = SITE_ROOT / "html" / "insights"
BLOG_OUTPUT_BASE: Path = SITE_ROOT / "html" / "blog"
TEMPLATES_DIR: Path = _BUNDLED_TEMPLATES_DIR

# Per-site overrides loaded from <site>/site.json. Keys consumed:
#   site_url (str), default_og_image (str),
#   site_name ({"ja": str, "en": str} or str),
#   copyright_text ({"ja": str, "en": str} or str)
_site_config: dict = {}

env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=False,
    keep_trailing_newline=True,
)


def _load_site_config(root: Path) -> dict:
    f = root / "site.json"
    if not f.exists():
        return {}
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Warning: failed to load {f}: {exc}", file=sys.stderr)
        return {}


def site_text(key: str, lang: str, default: str) -> str:
    """Look up a localized string from site.json, else return `default`.

    Supports values that are either a `{"ja": ..., "en": ...}` dict or a
    plain string (used for both languages).
    """
    val = _site_config.get(key)
    if isinstance(val, dict):
        return val.get(lang, default)
    if isinstance(val, str):
        return val
    return default


def configure_site(site: Path) -> None:
    """Point the builder at `site` (layout: articles/, blog/, html/).

    If `<site>/tools/templates/` exists it overrides the bundled templates,
    so a separate site can ship its own article/index layout without having
    to fork this script. `<site>/site.json` (optional) supplies per-site
    overrides for site_url, site_name, copyright_text, default_og_image.
    """
    global SITE_ROOT, ARTICLES_DIR, BLOG_DIR, OUTPUT_BASE, BLOG_OUTPUT_BASE
    global TEMPLATES_DIR, env, _site_config, SITE_URL, DEFAULT_OG_IMAGE

    SITE_ROOT = site.resolve()
    ARTICLES_DIR = SITE_ROOT / "articles"
    BLOG_DIR = SITE_ROOT / "blog"
    OUTPUT_BASE = SITE_ROOT / "html" / "insights"
    BLOG_OUTPUT_BASE = SITE_ROOT / "html" / "blog"

    site_templates = SITE_ROOT / "tools" / "templates"
    TEMPLATES_DIR = site_templates if site_templates.exists() else _BUNDLED_TEMPLATES_DIR
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,
        keep_trailing_newline=True,
    )

    _site_config = _load_site_config(SITE_ROOT)
    site_url = _site_config.get("site_url")
    SITE_URL = site_url.rstrip("/") if isinstance(site_url, str) and site_url else _DEFAULT_SITE_URL
    og_default = _site_config.get("default_og_image")
    DEFAULT_OG_IMAGE = og_default if isinstance(og_default, str) and og_default else _DEFAULT_OG_IMAGE


def resolve_site(argv: list[str]) -> tuple[Path, list[str]]:
    """Extract --site <path> (or --site=<path>) from argv.

    Falls back to AISEED_SITE env var, then to the repo root (parent of the
    `tools/` directory). Returns (site_path, remaining_argv_without_site_flag).
    """
    remaining: list[str] = []
    site: Path | None = None
    i = 0
    while i < len(argv):
        if argv[i] == "--site":
            if i + 1 >= len(argv):
                print("Error: --site requires a path", file=sys.stderr)
                sys.exit(1)
            site = Path(argv[i + 1])
            i += 2
            continue
        if argv[i].startswith("--site="):
            site = Path(argv[i].split("=", 1)[1])
            i += 1
            continue
        remaining.append(argv[i])
        i += 1

    if site is None:
        env_site = os.environ.get("AISEED_SITE")
        site = Path(env_site) if env_site else Path(__file__).parent.parent.parent
    return site.resolve(), remaining


def render(template_name: str, variables: dict) -> str:
    """Load a Jinja2 template and render with variables."""
    tpl = env.get_template(template_name)
    return tpl.render(**variables)
