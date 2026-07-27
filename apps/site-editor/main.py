"""aiseed.dev 記事エディタ — WordPress の管理画面風の Flet アプリ(フル機能版)。

シリーズ単位 AsciiDoc(articles/<series>.adoc)を、WordPress と同じ操作感で
管理する:

- 左サイドバー: シリーズ一覧 + 「変更を記録(git)」「サイトを公開」
- 一覧画面: 新規追加 / 検索 / 状態(公開・下書き) / 並び替え(↑↓) / 削除
- 編集画面: タイトル・サブタイトル・説明のフォーム(日英タブ) + 本文エディタ
  + 公開ボックス(状態・日付・スラッグ・更新・プレビュー・削除)
  + 画像ボックス(一覧・タグをコピー・追加(ファイル選択)・アイキャッチ指定)
- 新規記事は**下書き**で作られ、「公開」に切り替えるまでサイトに出ない
- 起動時にライブリロード付きプレビューサーバーを自動起動——「更新」を
  押すと数秒でビルドされ、開いているプレビューは自動で最新になる
- 削除にゴミ箱は無いが、「変更を記録」(git)からいつでも復元できる

起動:
    cd ~/dev/website-adoc && ./.venv/bin/python apps/site-editor/main.py
"""

from __future__ import annotations

import asyncio
import atexit
import datetime
import logging
import os
import webbrowser

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
)

import flet as ft

import store

# WordPress 管理画面の配色
WP_DARK = "#1d2327"
WP_DARK_ACTIVE = "#2271b1"
WP_DIM = "#c3c4c7"
WP_BG = "#f0f0f1"
WP_TEXT = "#1d2327"
WP_LINK = "#2271b1"
WP_OK = "#00a32a"
WP_WARN = "#dba617"
WP_ERR = "#d63638"
WP_MUTED = "#50575e"

PREVIEW_BASE = f"http://localhost:{store.PREVIEW_PORT}"

_preview_proc = store.start_preview()
if _preview_proc is not None:
    atexit.register(_preview_proc.terminate)

file_picker = ft.FilePicker()
clipboard = ft.Clipboard()


def _now() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")


def _meta_get(meta: dict, key: str, lang: str) -> str:
    return meta.get(f"{key}.{lang}", meta.get(key, ""))


def _meta_set(meta: dict, key: str, lang: str, value: str, langs: list) -> None:
    """言語別フィールドの書き込み。共有(裸)キーを言語別に編集したときは
    .ja/.en に分割してから書く(もう一方の言語の値を巻き込まないため)。"""
    if f"{key}.ja" in meta or f"{key}.en" in meta:
        meta[f"{key}.{lang}"] = value
    elif len(langs) == 1:
        meta[key] = value
    else:
        old = meta.pop(key, "")
        meta[f"{key}.ja"] = old
        meta[f"{key}.en"] = old
        meta[f"{key}.{lang}"] = value


# ---------------------------------------------------------------------------
# サイドバーとトップバー
# ---------------------------------------------------------------------------


@ft.component
def Sidebar(current, on_select, on_git, on_deploy):
    items = [
        ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.SPA, color="white", size=20),
                    ft.Text("aiseed.dev", color="white", size=16,
                            weight=ft.FontWeight.BOLD),
                ],
                spacing=8,
            ),
            padding=14,
        ),
        ft.Container(
            content=ft.Text("記事", color=WP_DIM, size=11),
            padding=ft.Padding(14, 10, 14, 4),
        ),
    ]
    for name, label in store.list_series():
        active = name == current
        items.append(
            ft.Container(
                content=ft.Text(label, color="white" if active else WP_DIM, size=13),
                bgcolor=WP_DARK_ACTIVE if active else None,
                padding=ft.Padding(18, 9, 10, 9),
                on_click=lambda e, n=name: on_select(n),
                ink=True,
            )
        )
    items.append(ft.Container(expand=True))
    for icon, text, handler in (
        (ft.Icons.HISTORY, "変更を記録", on_git),
        (ft.Icons.CLOUD_UPLOAD, "サイトを公開", on_deploy),
    ):
        items.append(
            ft.Container(
                content=ft.Row(
                    [ft.Icon(icon, color=WP_DIM, size=16),
                     ft.Text(text, color=WP_DIM, size=13)],
                    spacing=8,
                ),
                padding=ft.Padding(18, 9, 10, 9),
                on_click=lambda e, h=handler: h(),
                ink=True,
            )
        )
    items.append(
        ft.Container(
            content=ft.Text("プレビュー: " + PREVIEW_BASE, color=WP_DIM, size=10),
            padding=10,
        )
    )
    return ft.Container(
        content=ft.Column(items, spacing=0, expand=True),
        width=230,
        bgcolor=WP_DARK,
    )


@ft.component
def TopBar(status, status_color):
    return ft.Container(
        content=ft.Row(
            [
                ft.Text("サイト管理", color="white", size=13),
                ft.TextButton(
                    "サイトを表示",
                    style=ft.ButtonStyle(color="white"),
                    icon=ft.Icons.OPEN_IN_NEW,
                    on_click=lambda _: webbrowser.open(PREVIEW_BASE),
                ),
                ft.Container(expand=True),
                ft.Text(status, color=status_color, size=13),
            ],
            spacing=16,
        ),
        bgcolor=WP_DARK,
        padding=ft.Padding(16, 6, 16, 6),
    )


# ---------------------------------------------------------------------------
# 記事一覧
# ---------------------------------------------------------------------------


@ft.component
def ArticleList(series, articles, on_edit, on_new, on_delete, on_move):
    query, set_query = ft.use_state("")

    q = query.strip().lower()
    visible = [
        a for a in articles
        if not q
        or q in a.title_ja.lower()
        or q in a.title_en.lower()
        or q in a.slug.lower()
    ]

    rows = []
    for a in visible:
        title = a.title_ja or a.title_en or a.slug
        open_it = lambda e, art=a: on_edit(art)  # noqa: E731
        status_text = ("下書き", WP_WARN) if a.draft else ("公開", WP_OK)
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Column(
                            [
                                ft.Text(title, color=WP_LINK, size=14,
                                        weight=ft.FontWeight.W_500),
                                ft.Text(a.slug, size=11, color="#8c8f94"),
                            ],
                            spacing=2,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        on_tap=open_it,
                    ),
                    ft.DataCell(ft.Text(a.date, size=13, color=WP_MUTED),
                                on_tap=open_it),
                    ft.DataCell(
                        ft.Text(status_text[0], size=13, color=status_text[1],
                                weight=ft.FontWeight.W_500),
                        on_tap=open_it,
                    ),
                    ft.DataCell(
                        ft.Text(" / ".join(l.upper() for l in a.langs),
                                size=12, color=WP_MUTED),
                        on_tap=open_it,
                    ),
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.IconButton(
                                    ft.Icons.ARROW_UPWARD, icon_size=16,
                                    tooltip="上へ(並び順=連載順)",
                                    on_click=lambda e, art=a: on_move(art, -1),
                                ),
                                ft.IconButton(
                                    ft.Icons.ARROW_DOWNWARD, icon_size=16,
                                    tooltip="下へ",
                                    on_click=lambda e, art=a: on_move(art, 1),
                                ),
                                ft.IconButton(
                                    ft.Icons.DELETE_OUTLINE, icon_size=16,
                                    icon_color=WP_ERR, tooltip="削除",
                                    on_click=lambda e, art=a: on_delete(art),
                                ),
                            ],
                            spacing=0,
                        )
                    ),
                ],
            )
        )

    label = dict(store.list_series()).get(series, series)
    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text(label, size=23, color=WP_TEXT),
                    ft.OutlinedButton(
                        "新規追加",
                        icon=ft.Icons.ADD,
                        on_click=lambda _: on_new(),
                        style=ft.ButtonStyle(color=WP_LINK),
                    ),
                    ft.Container(expand=True),
                    ft.TextField(
                        hint_text="記事を検索",
                        value=query,
                        on_change=lambda e: set_query(e.control.value),
                        width=240,
                        height=40,
                        content_padding=8,
                        bgcolor="white",
                    ),
                ],
                spacing=16,
            ),
            ft.Text(f"{len(visible)} 件", size=12, color=WP_MUTED),
            ft.Container(
                content=ft.Column(
                    [
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("タイトル",
                                                      weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("日付",
                                                      weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("状態",
                                                      weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("言語",
                                                      weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("操作",
                                                      weight=ft.FontWeight.BOLD)),
                            ],
                            rows=rows,
                            heading_row_color="#f6f7f7",
                            data_row_min_height=52,
                            data_row_max_height=64,
                            column_spacing=20,
                            expand=True,
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                bgcolor="white",
                border=ft.Border.all(1, "#c3c4c7"),
                border_radius=3,
                expand=True,
            ),
        ],
        spacing=10,
        expand=True,
    )


# ---------------------------------------------------------------------------
# 編集画面
# ---------------------------------------------------------------------------


@ft.component
def Editor(series, article, draft, meta, assets, on_back, on_delete,
           on_reload_assets, set_status):
    saving, set_saving = ft.use_state(False)
    try:
        return _editor_body(series, article, draft, meta, assets, on_back,
                            on_delete, on_reload_assets, set_status,
                            saving, set_saving)
    except Exception:
        import traceback
        tb = traceback.format_exc()
        print(f"[editor build error]\n{tb}", flush=True)
        return ft.Text(f"編集画面の構築でエラー:\n{tb}", color=WP_ERR, size=12)


def _editor_body(series, article, draft, meta, assets, on_back, on_delete,
                 on_reload_assets, set_status, saving, set_saving):
    async def save(e):
        set_saving(True)
        try:
            await asyncio.to_thread(
                store.save_meta, series, article.article_id, dict(meta)
            )
            for lang, text in draft.items():
                await asyncio.to_thread(
                    store.save_body, series, article.article_id, lang, text
                )
        except ValueError as exc:
            set_status((f"保存できません: {exc}", WP_ERR))
            set_saving(False)
            return
        if store.preview_running():
            set_status((f"更新しました {_now()} — プレビューに反映中…", WP_OK))
        else:
            ok, err = await asyncio.to_thread(store.build_series, series)
            set_status(
                (f"更新してビルドしました {_now()}", WP_OK) if ok
                else (f"保存済み・ビルド失敗: {err[:120]}", WP_ERR)
            )
        set_saving(False)

    def open_preview(e):
        webbrowser.open(PREVIEW_BASE + store.article_url(series, article.slug))

    def make_copy_tag(name):
        # sync ラムダから async を呼ぶと await されないので、async クロージャを渡す
        async def handler(e):
            await clipboard.set(f"image::{name}[説明]")
            set_status((f"タグをコピーしました: {name} — 本文に貼り付けてください",
                        WP_OK))
        return handler

    async def pick_images(e):
        files = await file_picker.pick_files(
            dialog_title="画像・PDFを追加",
            allow_multiple=True,
            with_data=True,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["jpg", "jpeg", "png", "gif", "svg", "webp",
                                "avif", "pdf"],
        )
        added = 0
        for f in files or []:
            try:
                if getattr(f, "path", None):
                    store.add_asset(series, article.article_id, src=f.path)
                elif getattr(f, "bytes", None):
                    store.add_asset(series, article.article_id,
                                    data=f.bytes, filename=f.name)
                added += 1
            except ValueError as exc:
                set_status((str(exc), WP_ERR))
        if added:
            set_status((f"{added} 件の画像を追加しました", WP_OK))
            on_reload_assets()

    # --- 本文タブ(日英) ---
    lang_names = {"ja": "日本語", "en": "English"}
    tab_labels = []
    tab_views = []
    for lang in article.langs:
        tab_labels.append(ft.Tab(label=lang_names.get(lang, lang)))
        tab_views.append(
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.TextField(
                        label="タイトル",
                        value=_meta_get(meta, "title", lang),
                        bgcolor="white",
                        text_size=18,
                        on_change=lambda e, l=lang: _meta_set(
                            meta, "title", l, e.control.value, article.langs
                        ),
                    ),
                    ft.TextField(
                        label="サブタイトル",
                        value=_meta_get(meta, "subtitle", lang),
                        bgcolor="white",
                        on_change=lambda e, l=lang: _meta_set(
                            meta, "subtitle", l, e.control.value, article.langs
                        ),
                    ),
                    ft.TextField(
                        label="説明(検索結果・SNSに出る要約)",
                        value=_meta_get(meta, "description", lang),
                        multiline=True,
                        min_lines=2,
                        max_lines=3,
                        bgcolor="white",
                        on_change=lambda e, l=lang: _meta_set(
                            meta, "description", l, e.control.value, article.langs
                        ),
                    ),
                    ft.Container(
                        content=ft.TextField(
                            value=draft[lang],
                            multiline=True,
                            expand=True,
                            border=ft.InputBorder.NONE,
                            text_style=ft.TextStyle(
                                font_family="monospace", size=14, color=WP_TEXT
                            ),
                            on_change=lambda e, l=lang: draft.__setitem__(
                                l, e.control.value
                            ),
                        ),
                        bgcolor="white",
                        border=ft.Border.all(1, "#c3c4c7"),
                        border_radius=3,
                        padding=12,
                        expand=True,
                    ),
                ],
                spacing=8,
                expand=True,
            )
        )
    tabs = ft.Tabs(
        length=len(tab_labels),
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                ft.TabBar(tabs=tab_labels),
                ft.TabBarView(expand=True, controls=tab_views),
            ],
        ),
    )

    # --- 右カラム: 公開ボックス ---
    is_draft = store.is_draft_meta(meta)
    publish_box = ft.Container(
        content=ft.Column(
            [
                ft.Text("公開", size=14, weight=ft.FontWeight.BOLD, color=WP_TEXT),
                ft.Switch(
                    label="公開する(オフ=下書き)",
                    value=not is_draft,
                    on_change=lambda e: meta.update(
                        {"draft": "" if e.control.value else "true"}
                    ),
                ),
                ft.TextField(
                    label="日付", value=meta.get("date", ""), bgcolor="white",
                    on_change=lambda e: meta.update({"date": e.control.value}),
                ),
                ft.TextField(
                    label="スラッグ(URL)", value=meta.get("slug", ""),
                    bgcolor="white",
                    on_change=lambda e: meta.update({"slug": e.control.value}),
                ),
                ft.Row(
                    [
                        ft.Button(
                            "更新中…" if saving else "更新",
                            bgcolor=WP_DARK_ACTIVE, color="white",
                            disabled=saving, on_click=save,
                        ),
                        ft.OutlinedButton("プレビュー", on_click=open_preview),
                    ],
                    spacing=8,
                ),
                ft.TextButton(
                    content=ft.Text("この記事を削除", color=WP_ERR, size=12),
                    on_click=lambda _: on_delete(article),
                ),
            ],
            spacing=10,
        ),
        bgcolor="white",
        border=ft.Border.all(1, "#c3c4c7"),
        border_radius=3,
        padding=14,
    )

    # --- 右カラム: 画像ボックス ---
    asset_rows = [
        ft.Row(
            [
                ft.Icon(
                    ft.Icons.PICTURE_AS_PDF if n.lower().endswith(".pdf")
                    else ft.Icons.IMAGE,
                    size=16, color=WP_MUTED,
                ),
                ft.Text(n, size=12, color=WP_TEXT, expand=True,
                        overflow=ft.TextOverflow.ELLIPSIS),
                ft.IconButton(
                    ft.Icons.CONTENT_COPY, icon_size=14,
                    tooltip="本文用のタグをコピー",
                    on_click=make_copy_tag(n),
                ),
            ],
            spacing=4,
        )
        for n in assets
    ]
    hero_options = [ft.DropdownOption(key="", text="(なし)")] + [
        ft.DropdownOption(key=n, text=n) for n in assets
        if not n.lower().endswith(".pdf")
    ]
    images_box = ft.Container(
        content=ft.Column(
            [
                ft.Text("画像", size=14, weight=ft.FontWeight.BOLD, color=WP_TEXT),
                ft.Dropdown(
                    label="アイキャッチ(hero_image)",
                    value=meta.get("hero_image", ""),
                    options=hero_options,
                    bgcolor="white",
                    # 0.86 では on_change ではなく on_select
                    on_select=lambda e: meta.update(
                        {"hero_image": e.control.value or ""}
                    ),
                ),
                *asset_rows,
                ft.OutlinedButton("画像・PDFを追加", icon=ft.Icons.UPLOAD,
                                  on_click=pick_images),
            ],
            spacing=8,
        ),
        bgcolor="white",
        border=ft.Border.all(1, "#c3c4c7"),
        border_radius=3,
        padding=14,
    )

    return ft.Column(
        [
            ft.Row(
                [
                    ft.TextButton(
                        content=ft.Text("← 記事一覧に戻る", color=WP_LINK),
                        on_click=lambda _: on_back(),
                    ),
                    ft.Container(expand=True),
                    ft.Text(f"記事ID: {article.article_id}", size=11,
                            color="#8c8f94"),
                ]
            ),
            ft.Row(
                [
                    ft.Column([tabs], expand=True),
                    ft.Column(
                        [publish_box, images_box],
                        width=280,
                        spacing=12,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ],
                spacing=16,
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
        ],
        spacing=8,
        expand=True,
    )


# ---------------------------------------------------------------------------
# アプリ本体(画面切替とダイアログ)
# ---------------------------------------------------------------------------


@ft.component
def App():
    first = store.list_series()[0][0]
    view, set_view = ft.use_state(
        {"screen": "list", "series": first, "articles": store.load_articles(first)}
    )
    status, set_status = ft.use_state(("", WP_OK))
    forms = ft.use_state({"slug": "", "tja": "", "ten": "", "git": ""})[0]
    dlg_err, set_dlg_err = ft.use_state("")
    show_new, set_show_new = ft.use_state(False)
    del_target, set_del_target = ft.use_state(None)
    show_git, set_show_git = ft.use_state(False)
    show_deploy, set_show_deploy = ft.use_state(False)
    deploy_state, set_deploy_state = ft.use_state({"busy": False, "result": ""})

    def refresh_list(series=None):
        s = series or view["series"]
        set_view({"screen": "list", "series": s,
                  "articles": store.load_articles(s)})

    def select_series(name):
        refresh_list(name)

    def open_editor(article):
        s = view["series"]
        draft = {
            lang: store.read_body(s, article.article_id, lang)
            for lang in article.langs
        }
        set_view({
            **view, "screen": "edit", "article": article, "draft": draft,
            "meta": store.read_meta_raw(s, article.article_id),
            "assets": store.list_assets(s, article.article_id),
        })

    def reload_assets():
        set_view({**view, "assets":
                  store.list_assets(view["series"], view["article"].article_id)})

    def move(article, delta):
        if store.move_article(view["series"], article.article_id, delta):
            refresh_list()
            set_status((f"並び順を変更しました {_now()}", WP_OK))

    # --- 新規記事ダイアログ ---
    async def do_create(e):
        try:
            aid = await asyncio.to_thread(
                store.add_article, view["series"], forms["slug"],
                forms["tja"], forms["ten"],
            )
        except ValueError as exc:
            set_dlg_err(str(exc))
            return
        forms.update({"slug": "", "tja": "", "ten": ""})
        set_dlg_err("")
        set_show_new(False)
        set_status((f"下書きを作成しました: {aid}", WP_OK))
        refresh_list()

    ft.use_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("新規記事(下書きとして作成)"),
            content=ft.Column(
                [
                    ft.TextField(label="スラッグ(URL用・半角英数)",
                                 on_change=lambda e: forms.update(
                                     {"slug": e.control.value})),
                    ft.TextField(label="タイトル(日本語)",
                                 on_change=lambda e: forms.update(
                                     {"tja": e.control.value})),
                    ft.TextField(label="Title(英語・空欄なら日本語のみ)",
                                 on_change=lambda e: forms.update(
                                     {"ten": e.control.value})),
                    ft.Text(dlg_err, color=WP_ERR, size=12),
                ],
                tight=True,
                width=420,
                spacing=10,
            ),
            actions=[
                ft.Button("下書きを作成", bgcolor=WP_DARK_ACTIVE, color="white",
                          on_click=do_create),
                ft.TextButton("キャンセル",
                              on_click=lambda _: set_show_new(False)),
            ],
            on_dismiss=lambda _: set_show_new(False),
        )
        if show_new else None
    )

    # --- 削除確認ダイアログ ---
    async def do_delete(e):
        art = del_target
        try:
            await asyncio.to_thread(
                store.delete_article, view["series"], art.article_id
            )
        except ValueError as exc:
            set_status((f"削除できません: {exc}", WP_ERR))
            set_del_target(None)
            return
        set_del_target(None)
        set_status((f"削除しました: {art.slug}(「変更を記録」で確定・gitで復元可)",
                    WP_OK))
        refresh_list()

    ft.use_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("記事を削除しますか？"),
            content=ft.Text(
                f"「{(del_target.title_ja or del_target.slug) if del_target else ''}」"
                "を削除します。ゴミ箱はありませんが、「変更を記録」(git)から"
                "いつでも復元できます。"
            ),
            actions=[
                ft.Button("削除", bgcolor=WP_ERR, color="white",
                          on_click=do_delete),
                ft.TextButton("キャンセル",
                              on_click=lambda _: set_del_target(None)),
            ],
            on_dismiss=lambda _: set_del_target(None),
        )
        if del_target else None
    )

    def request_delete(article):
        set_del_target(article)

    # --- 変更を記録(git)ダイアログ ---
    async def do_commit(e):
        ok, out = await asyncio.to_thread(
            store.git_commit, forms["git"] or "記事を更新"
        )
        forms.update({"git": ""})
        set_show_git(False)
        set_status(("変更を記録しました " + _now(), WP_OK) if ok
                   else (f"記録できません: {out[:120]}", WP_ERR))

    dirty = store.git_dirty_count() if show_git else 0
    recent = store.git_recent(5) if show_git else []
    ft.use_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("変更を記録(バックアップ)"),
            content=ft.Column(
                [
                    ft.Text(
                        f"未記録の変更: {dirty} ファイル" if dirty
                        else "未記録の変更はありません",
                        color=WP_WARN if dirty else WP_MUTED, size=13,
                    ),
                    ft.TextField(
                        label="メモ(何を変えたか)", value=forms["git"],
                        on_change=lambda e: forms.update({"git": e.control.value}),
                    ),
                    ft.Text("最近の記録:", size=12, color=WP_MUTED),
                    *[ft.Text(l, size=11, color=WP_MUTED,
                              font_family="monospace") for l in recent],
                ],
                tight=True,
                width=460,
                spacing=8,
            ),
            actions=[
                ft.Button("記録する", bgcolor=WP_DARK_ACTIVE, color="white",
                          disabled=not dirty, on_click=do_commit),
                ft.TextButton("閉じる", on_click=lambda _: set_show_git(False)),
            ],
            on_dismiss=lambda _: set_show_git(False),
        )
        if show_git else None
    )

    # --- サイト公開(デプロイ)ダイアログ ---
    def make_deploy(branch):
        async def handler(e):
            set_deploy_state({"busy": True, "result": f"{branch} へ公開中…"})
            ok, out = await asyncio.to_thread(store.deploy, branch)
            set_deploy_state({
                "busy": False,
                "result": ("公開が完了しました。\n" if ok
                           else "公開に失敗しました。\n") + out[-600:],
            })
        return handler

    ft.use_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("サイトを公開(Cloudflare Pages)"),
            content=ft.Column(
                [
                    ft.Text("公開前に「更新」で保存済みか確認してください。"
                            "まずプレビューURLで確認し、問題なければ本番へ。",
                            size=13, color=WP_MUTED),
                    ft.Text(deploy_state["result"], size=12,
                            font_family="monospace", selectable=True),
                ],
                tight=True,
                width=520,
                spacing=10,
            ),
            actions=[
                ft.OutlinedButton(
                    "プレビューURLへ公開",
                    disabled=deploy_state["busy"],
                    on_click=make_deploy("preview"),
                ),
                ft.Button(
                    "本番へ公開",
                    bgcolor=WP_ERR, color="white",
                    disabled=deploy_state["busy"],
                    on_click=make_deploy("main"),
                ),
                ft.TextButton(
                    "閉じる",
                    disabled=deploy_state["busy"],
                    on_click=lambda _: set_show_deploy(False),
                ),
            ],
            on_dismiss=lambda _: set_show_deploy(False),
        )
        if show_deploy else None
    )

    # --- 画面 ---
    if view["screen"] == "edit":
        content = Editor(
            series=view["series"],
            article=view["article"],
            draft=view["draft"],
            meta=view["meta"],
            assets=view["assets"],
            on_back=lambda: refresh_list(),
            on_delete=request_delete,
            on_reload_assets=reload_assets,
            set_status=set_status,
        )
    else:
        content = ArticleList(
            series=view["series"],
            articles=view["articles"],
            on_edit=open_editor,
            on_new=lambda: (set_dlg_err(""), set_show_new(True)),
            on_delete=request_delete,
            on_move=move,
        )

    return ft.Row(
        [
            Sidebar(
                current=view["series"],
                on_select=select_series,
                on_git=lambda: set_show_git(True),
                on_deploy=lambda: set_show_deploy(True),
            ),
            ft.Column(
                [
                    TopBar(status=status[0], status_color=status[1]),
                    ft.Container(content=content, padding=20, expand=True),
                ],
                spacing=0,
                expand=True,
            ),
        ],
        spacing=0,
        expand=True,
    )


def main(page: ft.Page):
    page.on_error = lambda e: print(f"[page error] {getattr(e, 'data', e)}",
                                    flush=True)
    page.title = "aiseed.dev 記事エディタ"
    page.bgcolor = WP_BG
    page.padding = 0
    page.services.append(file_picker)
    page.services.append(clipboard)
    page.render(App)


if __name__ == "__main__":
    if os.environ.get("SITE_EDITOR_WEB"):
        ft.run(
            main,
            view=ft.AppView.WEB_BROWSER,
            port=int(os.environ.get("SITE_EDITOR_PORT", "8552")),
        )
    else:
        ft.run(main)
