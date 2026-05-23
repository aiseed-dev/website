"""Debian での代替アプリのインストール方法を返す.

Replacement テーブルが返す `alternatives` の文字列を入力に取り、
- `apt` / `flatpak` / `snap` / 公式 `.deb` などの導入方法
- 1 行のコマンド
- 注意点 (リポジトリ追加が要る等)
を返す。

未登録のアプリは「公式サイトを確認」のフォールバックを返す。
"""

from __future__ import annotations

from typing import TypedDict


class InstallEntry(TypedDict):
    method: str  # "apt", "flatpak", "snap", "manual"
    command: str
    note: str


# 完全一致 (小文字化、(...) 内の補足は事前に剥がす) で検索する。
TABLE: dict[str, InstallEntry] = {
    # --- Office suites ---
    "libreoffice writer": {"method": "apt", "command": "sudo apt install libreoffice",
                            "note": "Writer / Calc / Impress / Draw / Math が一括で入る"},
    "libreoffice calc": {"method": "apt", "command": "sudo apt install libreoffice",
                           "note": "Writer / Calc / Impress / Draw / Math が一括で入る"},
    "libreoffice impress": {"method": "apt", "command": "sudo apt install libreoffice",
                              "note": "Writer / Calc / Impress / Draw / Math が一括で入る"},
    "libreoffice draw": {"method": "apt", "command": "sudo apt install libreoffice",
                          "note": "Writer / Calc / Impress / Draw / Math が一括で入る"},
    "onlyoffice desktop": {"method": "flatpak", "command": "flatpak install -y flathub org.onlyoffice.desktopeditors",
                            "note": "Flathub に登録済み (個人利用は無料版)"},

    # --- Browsers ---
    "firefox": {"method": "apt", "command": "sudo apt install firefox-esr",
                "note": "Debian リポジトリにあるのは ESR (長期サポート版)"},
    "chromium": {"method": "apt", "command": "sudo apt install chromium",
                 "note": "オープンソース版 Chrome"},
    "brave": {"method": "manual", "command": "curl -fsS https://dl.brave.com/install.sh | sh",
              "note": "公式リポジトリを追加してから apt install する"},
    "google chrome (linux)": {"method": "manual",
                                "command": "wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && sudo apt install /tmp/chrome.deb",
                                "note": "Google 公式 .deb"},

    # --- Mail / PIM ---
    "thunderbird": {"method": "apt", "command": "sudo apt install thunderbird",
                    "note": "日本語パックは別 (thunderbird-l10n-ja)"},
    "evolution": {"method": "apt", "command": "sudo apt install evolution",
                  "note": "Exchange 連携は evolution-ews を追加"},

    # --- Image / Design ---
    "gimp": {"method": "apt", "command": "sudo apt install gimp",
             "note": "PSD は限定的に開ける"},
    "krita": {"method": "apt", "command": "sudo apt install krita",
              "note": "イラスト寄り。レイヤーやブラシが豊富"},
    "inkscape": {"method": "apt", "command": "sudo apt install inkscape",
                 "note": "SVG ベクター。AI ファイルは PDF 互換で書き出しておくと開ける"},
    "darktable": {"method": "apt", "command": "sudo apt install darktable",
                  "note": "Lightroom 代替の RAW 現像"},
    "rawtherapee": {"method": "apt", "command": "sudo apt install rawtherapee",
                    "note": "darktable と並ぶ RAW 現像"},
    "digikam": {"method": "apt", "command": "sudo apt install digikam",
                "note": "写真ライブラリ管理"},
    "shotwell": {"method": "apt", "command": "sudo apt install shotwell",
                 "note": "GNOME 標準寄りの写真管理"},

    # --- Video ---
    "kdenlive": {"method": "apt", "command": "sudo apt install kdenlive",
                 "note": "オープンソースの動画編集"},
    "davinci resolve": {"method": "manual",
                          "command": "(BlackMagicDesign のサイトから .deb / .run をダウンロード)",
                          "note": "無料版でも 4K まで。プロ向け編集 / カラコレ"},
    "vlc": {"method": "apt", "command": "sudo apt install vlc",
            "note": "ほぼ全ての動画形式が再生可"},
    "mpv": {"method": "apt", "command": "sudo apt install mpv",
            "note": "VLC より軽量。CLI でも使える"},
    "natron": {"method": "flatpak", "command": "flatpak install -y flathub fr.natron.Natron",
               "note": "ノードベースのコンポジット"},
    "blender (compositing)": {"method": "apt", "command": "sudo apt install blender",
                                "note": "Blender はコンポジットだけでなく 3D / 動画編集も可"},
    "obs studio (linux)": {"method": "apt", "command": "sudo apt install obs-studio",
                             "note": "配信 / 録画の標準"},

    # --- Audio ---
    "audacity": {"method": "apt", "command": "sudo apt install audacity",
                 "note": "波形編集、機能差なし"},
    "ardour": {"method": "apt", "command": "sudo apt install ardour",
               "note": "プロ向け DAW"},
    "reaper (linux)": {"method": "manual",
                         "command": "(reaper.fm から .tar.xz をダウンロード)",
                         "note": "シェアウェア (試用無期限)"},
    "rhythmbox": {"method": "apt", "command": "sudo apt install rhythmbox",
                  "note": "iTunes 風のミュージックプレイヤー"},
    "strawberry": {"method": "apt", "command": "sudo apt install strawberry",
                   "note": "Clementine の派生。コレクター向け"},
    "spotify (linux)": {"method": "flatpak", "command": "flatpak install -y flathub com.spotify.Client",
                          "note": "公式 Flatpak"},
    "lmms": {"method": "apt", "command": "sudo apt install lmms",
             "note": "GarageBand 代替の作曲ツール"},

    # --- Communication ---
    "slack (linux 公式)": {"method": "flatpak", "command": "flatpak install -y flathub com.slack.Slack",
                              "note": "Flathub または .deb。Flatpak は更新が楽"},
    "discord (linux 公式)": {"method": "flatpak", "command": "flatpak install -y flathub com.discordapp.Discord",
                                 "note": "公式 Flatpak"},
    "zoom (linux 公式)": {"method": "manual",
                              "command": "(zoom.us/download から .deb をダウンロード)",
                              "note": "公式 .deb は zoom.us 配布のみ"},
    "skype (linux)": {"method": "flatpak", "command": "flatpak install -y flathub com.skype.Client",
                       "note": "公式 Flatpak (将来は終了予定)"},
    "element": {"method": "flatpak", "command": "flatpak install -y flathub im.riot.Riot",
                "note": "Matrix クライアント"},
    "jitsi meet": {"method": "manual",
                    "command": "(ブラウザで meet.jit.si を開く)",
                    "note": "アプリ不要。ブラウザだけで会議が始められる"},

    # --- Notes / Productivity ---
    "joplin": {"method": "flatpak", "command": "flatpak install -y flathub net.cozic.joplin_desktop",
               "note": "Evernote / OneNote 代替"},
    "obsidian (appimage)": {"method": "flatpak", "command": "flatpak install -y flathub md.obsidian.Obsidian",
                              "note": "Flathub または公式 AppImage"},
    "1password (linux 公式)": {"method": "manual",
                                  "command": "curl -sS https://downloads.1password.com/linux/keys/1password.asc | sudo gpg --dearmor --output /usr/share/keyrings/1password-archive-keyring.gpg",
                                  "note": "公式リポジトリを追加して apt install 1password"},
    "keepassxc": {"method": "apt", "command": "sudo apt install keepassxc",
                  "note": "Linux ネイティブ、Linux 上では一番堅い"},
    "bitwarden": {"method": "flatpak", "command": "flatpak install -y flathub com.bitwarden.desktop",
                  "note": "公式 Flatpak"},
    "calibre": {"method": "apt", "command": "sudo apt install calibre",
                "note": "電子書籍管理。DRM なしの形式に限る"},
    "foliate": {"method": "flatpak", "command": "flatpak install -y flathub com.github.johnfactotum.Foliate",
                "note": "epub リーダー"},

    # --- Dev tools ---
    "vscodium": {"method": "flatpak", "command": "flatpak install -y flathub com.vscodium.codium",
                  "note": "Microsoft テレメトリ無し OSS ビルド"},
    "code (microsoft 公式)": {"method": "manual",
                                 "command": "(code.visualstudio.com から .deb をダウンロード)",
                                 "note": "Microsoft 公式リポジトリ追加でも可"},
    "intellij idea (linux)": {"method": "flatpak", "command": "flatpak install -y flathub com.jetbrains.IntelliJ-IDEA-Community",
                                 "note": "Community 版。Ultimate は別パッケージ"},
    "pycharm (linux)": {"method": "flatpak", "command": "flatpak install -y flathub com.jetbrains.PyCharm-Community",
                          "note": "Community 版"},
    "sublime text (linux)": {"method": "manual",
                                "command": "(sublimetext.com から .deb をダウンロード)",
                                "note": "シェアウェア"},
    "postman (linux)": {"method": "flatpak", "command": "flatpak install -y flathub com.getpostman.Postman",
                          "note": "公式 Flatpak"},
    "bruno": {"method": "flatpak", "command": "flatpak install -y flathub com.usebruno.Bruno",
              "note": "Postman 代替、ローカル保存"},
    "insomnia": {"method": "flatpak", "command": "flatpak install -y flathub rest.insomnia.Insomnia",
                 "note": "API テスト"},
    "git cli": {"method": "apt", "command": "sudo apt install git",
                "note": "標準で入っていることが多い"},
    "gitg": {"method": "apt", "command": "sudo apt install gitg",
             "note": "GNOME 系の Git GUI"},
    "gitkraken": {"method": "manual",
                  "command": "(gitkraken.com から .deb をダウンロード)",
                  "note": "クロスプラットフォーム Git GUI"},
    "docker engine (cli)": {"method": "manual",
                              "command": "curl -fsSL https://get.docker.com | sudo sh",
                              "note": "公式 get.docker.com スクリプト"},
    "podman": {"method": "apt", "command": "sudo apt install podman",
               "note": "Daemonless コンテナランタイム"},

    # --- Terminals ---
    "gnome terminal": {"method": "apt", "command": "sudo apt install gnome-terminal",
                       "note": "GNOME 環境では標準"},
    "konsole": {"method": "apt", "command": "sudo apt install konsole",
                "note": "KDE 環境の標準"},
    "tilix": {"method": "apt", "command": "sudo apt install tilix",
              "note": "タブ + ペイン分割"},
    "alacritty": {"method": "apt", "command": "sudo apt install alacritty",
                  "note": "GPU 加速の軽量端末"},

    # --- Backup ---
    "back in time": {"method": "apt", "command": "sudo apt install backintime-qt",
                     "note": "Time Machine 風の rsync ベース"},
    "borg": {"method": "apt", "command": "sudo apt install borgbackup",
             "note": "重複排除 + 暗号化"},
    "restic": {"method": "apt", "command": "sudo apt install restic",
               "note": "クラウド対応バックアップ"},

    # --- Sync ---
    "dropbox (linux)": {"method": "manual",
                          "command": "(dropbox.com/install-linux から .deb)",
                          "note": "公式 .deb"},
    "syncthing": {"method": "apt", "command": "sudo apt install syncthing",
                  "note": "P2P 同期"},
    "nextcloud": {"method": "flatpak", "command": "flatpak install -y flathub com.nextcloud.desktopclient.nextcloud",
                   "note": "Nextcloud デスクトップクライアント"},
    "rclone + cron": {"method": "apt", "command": "sudo apt install rclone",
                       "note": "OneDrive / Google Drive / S3 を扱える"},

    # --- Remote desktop ---
    "teamviewer (linux 公式)": {"method": "manual",
                                  "command": "(teamviewer.com/download/linux から .deb)",
                                  "note": "公式 .deb"},
    "anydesk (linux 公式)": {"method": "manual",
                                "command": "(anydesk.com/downloads/linux から .deb)",
                                "note": "公式 .deb"},
    "rustdesk": {"method": "manual",
                  "command": "(github.com/rustdesk/rustdesk/releases から .deb)",
                  "note": "オープンソースのリモートデスクトップ"},
    "citrix workspace (linux 公式)": {"method": "manual",
                                          "command": "(citrix.com から .deb)",
                                          "note": "企業 VDI 接続向け"},

    # --- VM ---
    "virtualbox": {"method": "apt", "command": "sudo apt install virtualbox",
                   "note": "contrib リポジトリを有効化する必要あり"},
    "qemu/kvm": {"method": "apt", "command": "sudo apt install qemu-system-x86 libvirt-daemon-system virt-manager",
                  "note": "Linux ホストで一番速い"},

    # --- Screenshot / Recording ---
    "flameshot": {"method": "apt", "command": "sudo apt install flameshot",
                  "note": "編集機能付きスクリーンショット"},
    "gnome screenshot": {"method": "apt", "command": "sudo apt install gnome-screenshot",
                          "note": "GNOME 標準"},
    "spectacle (kde)": {"method": "apt", "command": "sudo apt install kde-spectacle",
                          "note": "KDE 標準"},
    "peek": {"method": "apt", "command": "sudo apt install peek",
             "note": "簡単な GIF 録画"},
    "kazam": {"method": "apt", "command": "sudo apt install kazam",
              "note": "デスクトップ録画"},

    # --- Archives ---
    "p7zip": {"method": "apt", "command": "sudo apt install p7zip-full",
              "note": "7z / zip / rar の展開"},
    "file roller": {"method": "apt", "command": "sudo apt install file-roller",
                    "note": "GNOME 標準のアーカイバ"},
    "ark (kde)": {"method": "apt", "command": "sudo apt install ark",
                  "note": "KDE 標準のアーカイバ"},

    # --- Japanese input ---
    "fcitx5 + mozc": {"method": "apt", "command": "sudo apt install fcitx5 fcitx5-mozc fcitx5-config-qt",
                       "note": "本書 第 10 章で詳細"},
    "fcitx5 + anthy": {"method": "apt", "command": "sudo apt install fcitx5 fcitx5-anthy",
                        "note": "Mozc が動かない時の代替"},

    # --- File managers ---
    "files (nautilus)": {"method": "apt", "command": "sudo apt install nautilus",
                          "note": "GNOME 標準ファイラ"},
    "dolphin": {"method": "apt", "command": "sudo apt install dolphin",
                "note": "KDE 標準ファイラ"},
    "nemo": {"method": "apt", "command": "sudo apt install nemo",
             "note": "Cinnamon 標準ファイラ"},

    # --- PDF viewers ---
    "evince": {"method": "apt", "command": "sudo apt install evince",
               "note": "GNOME 標準 PDF ビューア"},
    "okular": {"method": "apt", "command": "sudo apt install okular",
               "note": "KDE 標準 PDF ビューア。注釈もできる"},
    "xournal++": {"method": "apt", "command": "sudo apt install xournalpp",
                   "note": "PDF 注釈と手書き署名"},
    "qpdf (cli)": {"method": "apt", "command": "sudo apt install qpdf",
                    "note": "結合 / 分割 / 暗号化"},
    "pdftk": {"method": "apt", "command": "sudo apt install pdftk-java",
              "note": "PDF の構造操作"},

    # --- Security ---
    "clamav": {"method": "apt", "command": "sudo apt install clamav clamav-daemon",
               "note": "オープンソースのウイルススキャナ"},
    "ufw": {"method": "apt", "command": "sudo apt install ufw && sudo ufw enable",
            "note": "Uncomplicated Firewall"},
    "rkhunter": {"method": "apt", "command": "sudo apt install rkhunter",
                 "note": "Rootkit ハンター"},

    # --- Gaming ---
    "steam (linux + proton)": {"method": "flatpak",
                                  "command": "flatpak install -y flathub com.valvesoftware.Steam",
                                  "note": "本書 第11章 第九節推奨。設定→互換性→「すべてのタイトルで Steam Play を有効化」で Proton 透過実行。"},
    "heroic games launcher": {"method": "flatpak",
                                  "command": "flatpak install -y flathub com.heroicgameslauncher.hgl",
                                  "note": "Epic / GOG / Amazon ライブラリ用。内部で Proton を使う。"},
    "lutris": {"method": "apt",
                  "command": "sudo apt install lutris",
                  "note": "Battle.net や個別タイトル用のインストーラスクリプト集。動作は protondb 要確認。"},

    # --- Japanese ---
    "gnucash": {"method": "apt", "command": "sudo apt install gnucash",
                "note": "複式簿記の会計"},
    "freee / money forward (web)": {"method": "manual",
                                       "command": "(ブラウザで freee.co.jp / moneyforward.com を開く)",
                                       "note": "Web アプリ。Linux ネイティブ不要"},
    "libreoffice + 差し込み印刷": {"method": "apt", "command": "sudo apt install libreoffice",
                                       "note": "差し込み印刷で住所録 → 年賀状"},
    "python + reportlab": {"method": "apt", "command": "sudo apt install python3-reportlab",
                             "note": "Python でハガキレイアウトを書くと正確"},
}


def find_install(alternative_name: str) -> InstallEntry | None:
    """Look up the install method for a given replacement-table alternative."""
    key = alternative_name.lower().strip()
    if key in TABLE:
        return TABLE[key]
    # Strip parenthetical suffixes and retry once
    if "(" in key:
        head = key.split("(", 1)[0].strip()
        if head in TABLE:
            return TABLE[head]
    return None
