"""Claude 用プロンプトテンプレート集.

各画面の「Claude にこの状態を渡す」ボタンが、このモジュールの関数を
呼んで生成したテキストをクリップボードにコピーする。生成されたテキストは
そのまま claude.ai に貼り付ければ会話を始められる構成にする。
"""

from __future__ import annotations

import platform
from textwrap import dedent

from debian_migrate.state import (
    DetectedApp,
    HardwareInfo,
    Replacement,
    UsbDevice,
)


def system_header() -> str:
    return dedent(
        f"""
        # 環境
        - OS: {platform.system()} {platform.release()}
        - アーキ: {platform.machine()}
        - 言語: 日本語

        # 経緯
        私は Windows / macOS から Debian Linux への移行を検討しています。
        aiseed.dev の「Claudeと一緒に学ぶDebian」(https://aiseed.dev/claude-debian/)
        を参考にしながら、デスクトップアプリ「Debian 移行ウィザード」で
        棚卸しを進めています。以下はその情報です。
        """
    ).strip()


def inventory_prompt(apps: list[DetectedApp]) -> str:
    """検出されたアプリ一覧を Claude に渡すプロンプト."""
    lines = [system_header(), "", "# 検出されたアプリ"]
    if not apps:
        lines.append("(検出できず — 手動で重要なアプリを書き出す予定)")
    else:
        for a in apps[:120]:  # 過度に長くなるのを防ぐ
            v = f" ({a.version})" if a.version else ""
            pub = f" — {a.publisher}" if a.publisher else ""
            lines.append(f"- {a.name}{v}{pub}")
        if len(apps) > 120:
            lines.append(f"...他 {len(apps) - 120} 件")
    lines += [
        "",
        "# 質問",
        "この一覧から、私が日常で本当に使っているものはどれだと推測できますか。",
        "また、Debian 移行で特に注意すべきアプリ (代替が無い・データ移行が面倒) を挙げてください。",
    ]
    return "\n".join(lines)


def replacements_prompt(reps: list[Replacement]) -> str:
    """代替候補リストを Claude に渡すプロンプト."""
    lines = [system_header(), "", "# 代替検討の状況"]
    for r in reps:
        alts = " / ".join(r.alternatives) if r.alternatives else "(候補なし)"
        choice = f" — 選択: {r.user_choice}" if r.user_choice else ""
        lines.append(f"- {r.detected} → {alts} [{r.confidence}]{choice}")
        if r.note:
            lines.append(f"  注: {r.note}")
    lines += [
        "",
        "# 質問",
        "上記の中で、私のワークフロー (主に [ ← ここに自分の業務を書く ]) に",
        "とって致命的になりそうな置き換えはどれですか。具体的に何が崩れるか、",
        "代替手段は何が現実的か、教えてください。",
    ]
    return "\n".join(lines)


def hardware_prompt(hw: HardwareInfo) -> str:
    """ハードウェア情報を Claude に渡すプロンプト."""
    disks = "\n".join(
        f"  - {d['device']} ({d['fstype']}): 全 {d['total_gb']}GB / 空き {d['free_gb']}GB"
        for d in hw.disks
    ) or "  - (検出なし)"
    warns = "\n".join(f"- ⚠ {w}" for w in hw.warnings) or "- (警告なし)"
    body = dedent(
        f"""
        # ハードウェア
        - OS: {hw.os_name} {hw.os_version}
        - アーキ: {hw.arch}
        - CPU: {hw.cpu_model} ({hw.cpu_cores} コア)
        - メモリ: {hw.ram_gb} GB
        - GPU: {hw.gpu}
        - ディスク:
        {disks}

        # 検出された注意点
        {warns}

        # 質問
        この構成で Debian (12 / 13 系) をインストールする場合、
        - 推奨されるデスクトップ環境 (GNOME / KDE / XFCE 等) は何か
        - インストール前に決めておくべき設定 (ファームウェア・ディスクパーティション)
        - 既知の落とし穴
        を、ステップで教えてください (本書 第6章 / 第7章 / 第8章 を踏まえて)。
        """
    ).strip()
    return f"{system_header()}\n\n{body}"


def usb_prompt(devices: list[UsbDevice], selected: str | None) -> str:
    """USB インストーラ作成段階のプロンプト."""
    lines = [system_header(), "", "# 候補 USB デバイス"]
    if not devices:
        lines.append("(検出できず — USB を差し込んでから再スキャンが必要)")
    else:
        for d in devices:
            mark = " ← 選択中" if selected and selected == d.path else ""
            lines.append(f"- {d.path}: {d.label} ({d.size_gb}GB){mark}")
    lines += [
        "",
        "# 質問",
        "選択した USB に Debian の ISO を書き込む手順を、私の OS に合わせて",
        "コマンド単位で教えてください。書き込みのリスク (デバイスを間違えると",
        "システムを壊す) を最初に明示してから、安全に進める順番でお願いします。",
        "Balena Etcher を使う場合の手順も併記してください (本書 第7章)。",
    ]
    return "\n".join(lines)


def summary_prompt(
    apps: list[DetectedApp],
    reps: list[Replacement],
    hw: HardwareInfo,
    selected_usb: str | None,
) -> str:
    """最終まとめ — 全状況を一括で Claude に渡す."""
    lines = [
        system_header(),
        "",
        "# 全体まとめ",
        f"- 検出アプリ数: {len(apps)}",
        f"- 代替検討済み: {sum(1 for r in reps if r.user_choice)} / {len(reps)}",
        f"- ハードウェア警告数: {len(hw.warnings)}",
        f"- インストール先 USB: {selected_usb or '(未選択)'}",
        "",
        "# 重要な代替検討メモ",
    ]
    for r in reps:
        if r.confidence in ("review", "missing"):
            choice = f" — 選択: {r.user_choice}" if r.user_choice else ""
            lines.append(f"- {r.detected} → {' / '.join(r.alternatives) or '(候補なし)'} [{r.confidence}]{choice}")
            if r.note:
                lines.append(f"  注: {r.note}")
    lines += [
        "",
        "# 質問",
        "ここまでの情報をもとに、私の Debian 移行プランをチェックして、",
        "順番 (この週末は何を、来週末は何を) と、各ステップの判断基準を",
        "教えてください。並行稼働期間も含めて (本書 全 24 章 を踏まえて)。",
    ]
    return "\n".join(lines)
