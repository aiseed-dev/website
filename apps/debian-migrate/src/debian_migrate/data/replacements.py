"""Static map: source-OS app name → Debian-side alternatives.

Match is **case-insensitive substring** on the detected app name. The
first matching entry wins. Keep the order from most-specific to
most-generic, and prefer matching the publisher-prefixed product name
where it disambiguates (e.g. "Microsoft Word", "Adobe Photoshop").

`confidence` is the realism of the swap, not a feature parity score:
  - "ok"      = drop-in for everyday use
  - "review"  = covers core use, but workflows differ; user should try
  - "missing" = no real Debian equivalent; need a workaround or keep VM
"""

from __future__ import annotations

from typing import TypedDict


class ReplacementEntry(TypedDict):
    match: str
    alternatives: list[str]
    confidence: str
    note: str


TABLE: list[ReplacementEntry] = [
    # --- Microsoft Office family ---
    {
        "match": "microsoft word",
        "alternatives": ["LibreOffice Writer", "ONLYOFFICE Desktop", "Markdown + Pandoc"],
        "confidence": "ok",
        "note": "対外文書は PDF にして送ると相手側で書式崩れが出ない (本書 第11章)。",
    },
    {
        "match": "microsoft excel",
        "alternatives": ["LibreOffice Calc", "ONLYOFFICE Desktop", "JupyterLab + Polars"],
        "confidence": "ok",
        "note": "VBA マクロは Python に書き換える (本書 第13章 / AIネイティブな仕事の作法 第2章)。",
    },
    {
        "match": "microsoft powerpoint",
        "alternatives": ["LibreOffice Impress", "Marp", "reveal.js"],
        "confidence": "ok",
        "note": "Markdown スライド (Marp) なら同じ原稿から PDF / HTML 両対応。",
    },
    {
        "match": "microsoft outlook",
        "alternatives": ["Thunderbird", "Evolution"],
        "confidence": "ok",
        "note": "Exchange アカウントは Evolution の方が相性が良い。",
    },
    {
        "match": "microsoft onenote",
        "alternatives": ["Joplin", "Obsidian (AppImage)", "Markdown フォルダ"],
        "confidence": "review",
        "note": "OneNote のセクション/ページ階層は Joplin に近い。",
    },
    {
        "match": "microsoft teams",
        "alternatives": ["Teams (PWA / ブラウザ)", "Element", "Jitsi Meet"],
        "confidence": "review",
        "note": "公式 Linux 版は提供終了。ブラウザの PWA が現実解。",
    },
    {
        "match": "microsoft edge",
        "alternatives": ["Firefox", "Chromium", "Brave"],
        "confidence": "ok",
        "note": "ブックマーク / パスワードは事前にエクスポート。",
    },
    {
        "match": "onedrive",
        "alternatives": ["Nextcloud", "Syncthing", "rclone + cron"],
        "confidence": "review",
        "note": "Microsoft 公式の Linux クライアントはない。rclone での同期が一般的。",
    },
    # --- Apple ---
    {
        "match": "icloud",
        "alternatives": ["Nextcloud", "Syncthing"],
        "confidence": "review",
        "note": "写真ライブラリは事前にエクスポートが必要。",
    },
    {
        "match": "safari",
        "alternatives": ["Firefox", "Chromium"],
        "confidence": "ok",
        "note": "ブックマーク / Keychain パスワードは事前にエクスポート。",
    },
    {
        "match": "finder",
        "alternatives": ["Files (Nautilus)", "Dolphin", "Nemo"],
        "confidence": "ok",
        "note": "デスクトップ環境ごとに標準ファイラが違う (本書 第9章)。",
    },
    {
        "match": "preview",
        "alternatives": ["Evince", "Okular", "Xournal++"],
        "confidence": "ok",
        "note": "PDF への注釈・署名は Xournal++。",
    },
    # --- Adobe ---
    {
        "match": "adobe photoshop",
        "alternatives": ["GIMP", "Krita", "Photopea (Web)"],
        "confidence": "review",
        "note": "PSD は GIMP で開けるが、Smart Object など一部の互換性は弱い。",
    },
    {
        "match": "adobe illustrator",
        "alternatives": ["Inkscape"],
        "confidence": "review",
        "note": "AI ファイルは保存時に PDF 互換にしておくと Inkscape で開ける。",
    },
    {
        "match": "adobe premiere",
        "alternatives": ["DaVinci Resolve", "Kdenlive"],
        "confidence": "review",
        "note": "DaVinci Resolve は無料版でも 4K まで対応。色補正が強い。",
    },
    {
        "match": "adobe lightroom",
        "alternatives": ["darktable", "RawTherapee"],
        "confidence": "review",
        "note": "カタログ移行はできないので、書き出した RAW + サイドカーで再構築。",
    },
    {
        "match": "adobe acrobat",
        "alternatives": ["Evince", "Okular", "qpdf (CLI)", "pdftk"],
        "confidence": "ok",
        "note": "結合 / 分割 / OCR は qpdf / ocrmypdf を組み合わせる。",
    },
    {
        "match": "adobe after effects",
        "alternatives": ["Natron", "Blender (Compositing)"],
        "confidence": "missing",
        "note": "完全な代替は無い。プロ業務なら macOS / Windows を VM で残す検討を。",
    },
    # --- Communication ---
    {
        "match": "slack",
        "alternatives": ["Slack (Linux 公式)", "Element"],
        "confidence": "ok",
        "note": "Slack の Linux 版は .deb / Flatpak で提供されている。",
    },
    {
        "match": "discord",
        "alternatives": ["Discord (Linux 公式)"],
        "confidence": "ok",
        "note": ".deb / Flatpak で提供。アカウントはそのまま使える。",
    },
    {
        "match": "zoom",
        "alternatives": ["Zoom (Linux 公式)", "Jitsi Meet"],
        "confidence": "ok",
        "note": ".deb で提供。仮想背景などの一部機能は GPU 性能依存。",
    },
    {
        "match": "skype",
        "alternatives": ["Skype (Linux)", "Element", "Jitsi Meet"],
        "confidence": "review",
        "note": "Microsoft は Skype のサポートを縮小中。代替の検討を推奨。",
    },
    {
        "match": "line",
        "alternatives": ["LINE (Chrome 拡張)", "LINE (Web)"],
        "confidence": "review",
        "note": "公式 Linux デスクトップ版なし。Chrome 拡張か Web 版。",
    },
    # --- Dev tools ---
    {
        "match": "visual studio code",
        "alternatives": ["VSCodium", "Code (Microsoft 公式)"],
        "confidence": "ok",
        "note": "VSCodium はテレメトリ無し OSS ビルド。同じ拡張機能が使える。",
    },
    {
        "match": "visual studio",
        "alternatives": ["VSCode + 言語拡張", "JetBrains Rider"],
        "confidence": "review",
        "note": "Win/Mac 専用機能を多用していると完全移行は難しい。",
    },
    {
        "match": "iterm",
        "alternatives": ["GNOME Terminal", "Konsole", "Tilix", "Alacritty"],
        "confidence": "ok",
        "note": "プロファイル機能なら Tilix が近い。",
    },
    {
        "match": "windows terminal",
        "alternatives": ["GNOME Terminal", "Konsole", "Tilix"],
        "confidence": "ok",
        "note": "タブ / ペイン分割は標準的に揃っている。",
    },
    {
        "match": "git extensions",
        "alternatives": ["git (CLI)", "Gitg", "GitKraken"],
        "confidence": "ok",
        "note": "CLI に慣れる絶好の機会 (本書 第13章)。",
    },
    {
        "match": "docker desktop",
        "alternatives": ["Docker Engine (CLI)", "Podman"],
        "confidence": "ok",
        "note": "Linux ではエンジン直起動の方が軽い。",
    },
    # --- Browsers ---
    {
        "match": "google chrome",
        "alternatives": ["Google Chrome (Linux)", "Chromium", "Firefox"],
        "confidence": "ok",
        "note": "Google アカウント連携は Linux 版 Chrome でそのまま動く。",
    },
    {
        "match": "firefox",
        "alternatives": ["Firefox (Linux)"],
        "confidence": "ok",
        "note": "プロファイルは ~/.mozilla を持っていけば移行できる。",
    },
    {
        "match": "brave",
        "alternatives": ["Brave (Linux)"],
        "confidence": "ok",
        "note": ".deb で提供。",
    },
    # --- Media ---
    {
        "match": "spotify",
        "alternatives": ["Spotify (Linux)"],
        "confidence": "ok",
        "note": ".deb / Snap / Flatpak で提供。",
    },
    {
        "match": "vlc",
        "alternatives": ["VLC (Linux)"],
        "confidence": "ok",
        "note": "クロスプラットフォーム標準。",
    },
    {
        "match": "audacity",
        "alternatives": ["Audacity (Linux)"],
        "confidence": "ok",
        "note": "Linux ネイティブ、機能差なし。",
    },
    # --- Productivity ---
    {
        "match": "1password",
        "alternatives": ["1Password (Linux 公式)", "KeePassXC", "Bitwarden"],
        "confidence": "ok",
        "note": "1Password は Linux 公式版あり。",
    },
    {
        "match": "evernote",
        "alternatives": ["Joplin", "Obsidian"],
        "confidence": "review",
        "note": "ノートは ENEX エクスポート → Joplin インポート。",
    },
    {
        "match": "notion",
        "alternatives": ["Notion (Web / PWA)", "Joplin", "Obsidian + Anytype"],
        "confidence": "review",
        "note": "公式 Linux 版は無いが、PWA で代替可。",
    },
    {
        "match": "dropbox",
        "alternatives": ["Dropbox (Linux)", "Syncthing", "Nextcloud"],
        "confidence": "ok",
        "note": "Dropbox の Linux 版は公式提供あり。",
    },
    # --- Japanese input (special) ---
    {
        "match": "atok",
        "alternatives": ["Fcitx5 + Mozc", "Fcitx5 + Anthy"],
        "confidence": "review",
        "note": "ATOK Linux 版は終了。Mozc が現実的な代替 (本書 第10章)。",
    },
    {
        "match": "google 日本語入力",
        "alternatives": ["Fcitx5 + Mozc"],
        "confidence": "ok",
        "note": "Mozc は Google 日本語入力のオープンソース版がベース。",
    },
    {
        "match": "ms-ime",
        "alternatives": ["Fcitx5 + Mozc"],
        "confidence": "ok",
        "note": "本書 第10章で詳細な設定手順。",
    },
    # --- Games / DRM-heavy ---
    {
        "match": "steam",
        "alternatives": ["Steam (Linux + Proton)"],
        "confidence": "review",
        "note": "Proton で Windows ゲームの大半が動くが、アンチチート系は不可。",
    },
]


def find_replacement(detected_name: str) -> ReplacementEntry | None:
    """Return the first matching entry, or None."""
    name = detected_name.lower()
    for entry in TABLE:
        if entry["match"] in name:
            return entry
    return None
