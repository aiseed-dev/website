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
    # --- Apple iWork / native apps ---
    {
        "match": "pages",
        "alternatives": ["LibreOffice Writer", "ONLYOFFICE Desktop"],
        "confidence": "review",
        "note": ".pages は事前に .docx / PDF で書き出す。",
    },
    {
        "match": "numbers",
        "alternatives": ["LibreOffice Calc", "ONLYOFFICE Desktop"],
        "confidence": "review",
        "note": ".numbers は事前に .xlsx / CSV で書き出す。",
    },
    {
        "match": "keynote",
        "alternatives": ["LibreOffice Impress", "Marp"],
        "confidence": "review",
        "note": ".key は事前に .pptx / PDF で書き出す。",
    },
    {
        "match": "itunes",
        "alternatives": ["Rhythmbox", "Strawberry", "Lollypop"],
        "confidence": "review",
        "note": "ライブラリは XML エクスポート + ファイル本体を持っていく。",
    },
    {
        "match": "quicktime",
        "alternatives": ["VLC", "mpv"],
        "confidence": "ok",
        "note": "ほとんどの動画形式はそのまま再生できる。",
    },
    {
        "match": "photos",
        "alternatives": ["digiKam", "Shotwell"],
        "confidence": "review",
        "note": "Photos ライブラリは「写真を書き出す」で全 RAW + メタを取り出してから移行。",
    },
    {
        "match": "books",
        "alternatives": ["Calibre", "Foliate"],
        "confidence": "review",
        "note": "DRM 付き電子書籍は Calibre でも開けないので注意。",
    },
    {
        "match": "garageband",
        "alternatives": ["Ardour", "LMMS"],
        "confidence": "review",
        "note": "プロジェクトは互換性なし。録音素材は WAV で書き出してから持っていく。",
    },
    {
        "match": "logic pro",
        "alternatives": ["Ardour", "Reaper (Linux)"],
        "confidence": "review",
        "note": "プロ向けの選択肢は限定的。Reaper はクロスプラットフォームで Logic に近い。",
    },
    # --- 日本市場で多い業務系 ---
    {
        "match": "一太郎",
        "alternatives": ["LibreOffice Writer", "ONLYOFFICE Desktop"],
        "confidence": "review",
        "note": "JTD ファイルは LibreOffice でも崩れる。PDF / DOCX に書き出してから持っていく。",
    },
    {
        "match": "花子",
        "alternatives": ["Inkscape", "LibreOffice Draw"],
        "confidence": "review",
        "note": "図面は SVG / PDF で書き出してから移行。",
    },
    {
        "match": "筆まめ",
        "alternatives": ["LibreOffice + 差し込み印刷", "Python + ReportLab"],
        "confidence": "review",
        "note": "年賀状ソフトの Linux 版はない。住所録は CSV エクスポートして再構成。",
    },
    {
        "match": "筆王",
        "alternatives": ["LibreOffice + 差し込み印刷", "Python + ReportLab"],
        "confidence": "review",
        "note": "住所録を CSV / VCF にエクスポートしてから移行。",
    },
    {
        "match": "弥生会計",
        "alternatives": ["GnuCash", "freee / Money Forward (Web)"],
        "confidence": "missing",
        "note": "Linux ネイティブの代替はほぼ無い。クラウド会計 (freee 等) に移すのが現実的。",
    },
    {
        "match": "勘定奉行",
        "alternatives": ["freee / Money Forward (Web)"],
        "confidence": "missing",
        "note": "Linux 版なし。クラウド会計移行か、VM で Windows を残す。",
    },
    # --- リモートデスクトップ / 画面共有 ---
    {
        "match": "teamviewer",
        "alternatives": ["TeamViewer (Linux 公式)", "AnyDesk", "RustDesk"],
        "confidence": "ok",
        "note": "TeamViewer は Linux 公式版あり。",
    },
    {
        "match": "anydesk",
        "alternatives": ["AnyDesk (Linux 公式)"],
        "confidence": "ok",
        "note": ".deb で提供。",
    },
    {
        "match": "citrix workspace",
        "alternatives": ["Citrix Workspace (Linux 公式)"],
        "confidence": "ok",
        "note": "Linux 版あり。企業 VDI 接続が必要な人向け。",
    },
    {
        "match": "vmware",
        "alternatives": ["VirtualBox", "VMware Workstation (Linux)", "QEMU/KVM"],
        "confidence": "ok",
        "note": "Linux 上では KVM が最も性能が出る。",
    },
    # --- スクリーンショット / 録画 ---
    {
        "match": "snagit",
        "alternatives": ["Flameshot", "GNOME Screenshot", "Spectacle (KDE)"],
        "confidence": "review",
        "note": "編集機能込みなら Flameshot が近い。",
    },
    {
        "match": "screentogif",
        "alternatives": ["Peek", "Kazam"],
        "confidence": "ok",
        "note": "GIF 録画はどちらも軽い。",
    },
    {
        "match": "obs",
        "alternatives": ["OBS Studio (Linux)"],
        "confidence": "ok",
        "note": "ほぼ機能差なし。配信プロファイルは XML エクスポート/インポート可。",
    },
    {
        "match": "camtasia",
        "alternatives": ["OBS Studio + Kdenlive", "DaVinci Resolve"],
        "confidence": "review",
        "note": "録画 (OBS) と編集 (Kdenlive / Resolve) が分かれる構成になる。",
    },
    # --- 開発系の追加 ---
    {
        "match": "intellij",
        "alternatives": ["IntelliJ IDEA (Linux)"],
        "confidence": "ok",
        "note": "JetBrains 全製品の Linux 版がある。設定は同期可能。",
    },
    {
        "match": "pycharm",
        "alternatives": ["PyCharm (Linux)", "VSCodium + Python 拡張"],
        "confidence": "ok",
        "note": "PyCharm Linux 版あり。軽い用途なら VSCodium で十分。",
    },
    {
        "match": "sublime text",
        "alternatives": ["Sublime Text (Linux)"],
        "confidence": "ok",
        "note": "Linux 版あり、設定 (.sublime-settings) もそのまま使える。",
    },
    {
        "match": "postman",
        "alternatives": ["Postman (Linux)", "Bruno", "Insomnia"],
        "confidence": "ok",
        "note": "Bruno はオフライン + ローカル保存。",
    },
    {
        "match": "github desktop",
        "alternatives": ["git CLI", "Gitg", "GitKraken"],
        "confidence": "review",
        "note": "Linux 公式版はない。",
    },
    {
        "match": "sourcetree",
        "alternatives": ["git CLI", "GitKraken", "Gitg"],
        "confidence": "review",
        "note": "Linux 版はない。",
    },
    # --- バックアップ / 同期 ---
    {
        "match": "time machine",
        "alternatives": ["Back In Time", "Borg", "Restic"],
        "confidence": "review",
        "note": "rsync ベース。Borg / Restic は重複排除 + 暗号化が強い。",
    },
    {
        "match": "carbon copy cloner",
        "alternatives": ["rsync", "Borg"],
        "confidence": "review",
        "note": "ディスクイメージのまま運ぶなら dd / Clonezilla。",
    },
    # --- セキュリティ ---
    {
        "match": "norton",
        "alternatives": ["ClamAV", "rkhunter", "ufw"],
        "confidence": "review",
        "note": "Linux は基本的にウイルス対策を入れない運用が一般的。",
    },
    {
        "match": "kaspersky",
        "alternatives": ["ClamAV", "rkhunter"],
        "confidence": "review",
        "note": "Linux はパッケージ管理 + ファイアウォール (ufw) が中心。",
    },
    # --- メッセージング (日本) ---
    {
        "match": "chatwork",
        "alternatives": ["Chatwork (Web)"],
        "confidence": "ok",
        "note": "公式 Linux デスクトップ版なし。Web 版で代替。",
    },
    # --- ファイル管理 / アーカイブ ---
    {
        "match": "winrar",
        "alternatives": ["File Roller", "Ark (KDE)", "p7zip"],
        "confidence": "ok",
        "note": "RAR の展開は unrar パッケージで対応。",
    },
    {
        "match": "7-zip",
        "alternatives": ["p7zip", "File Roller", "Ark"],
        "confidence": "ok",
        "note": "Linux 側は p7zip コマンドが標準。",
    },
]


def find_replacement(detected_name: str) -> ReplacementEntry | None:
    """Return the first matching entry, or None."""
    name = detected_name.lower()
    for entry in TABLE:
        if entry["match"] in name:
            return entry
    return None
