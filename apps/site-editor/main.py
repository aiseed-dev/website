"""aiseed.dev 記事エディタ — WordPress の管理画面風の Flet アプリ。

シリーズ単位 AsciiDoc(articles/<series>.adoc)のうち、**本文(書いている
部分)だけ**を編集する。フロントマターや記事の区切りには触れないので、
壊す心配なく記事を直せる。

- 左サイドバー: シリーズ一覧(WPの「投稿」メニュー相当)
- 一覧画面: 記事のタイトル・スラッグ・日付(WPの投稿一覧相当)
- 編集画面: 日本語/English のタブ + 大きな本文エディタ + 更新ボタン
- 起動時にプレビューサーバー(ライブリロード付き)を自動起動——
  「更新」を押すと数秒でビルドされ、開いているプレビューは自動で
  最新になる

起動:
    cd ~/dev/website-adoc && ./.venv/bin/python apps/site-editor/main.py
"""

from __future__ import annotations

import asyncio
import atexit
import datetime
import os
import webbrowser

import flet as ft

import store

# WordPress 管理画面の配色
WP_DARK = "#1d2327"        # サイドバー・アドミンバー
WP_DARK_ACTIVE = "#2271b1"  # 選択中メニュー・主ボタン(WPブルー)
WP_DIM = "#c3c4c7"          # サイドバーの文字
WP_BG = "#f0f0f1"           # コンテンツ背景
WP_TEXT = "#1d2327"
WP_LINK = "#2271b1"
WP_OK = "#00a32a"
WP_ERR = "#d63638"

PREVIEW_BASE = f"http://localhost:{store.PREVIEW_PORT}"

_preview_proc = store.start_preview()
if _preview_proc is not None:
    atexit.register(_preview_proc.terminate)


def _now() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")


@ft.component
def Sidebar(current, on_select):
    items = [
        ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.SPA, color="white", size=20),
                    ft.Text("aiseed.dev", color="white", size=16, weight=ft.FontWeight.BOLD),
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
                content=ft.Text(
                    label,
                    color="white" if active else WP_DIM,
                    size=13,
                ),
                bgcolor=WP_DARK_ACTIVE if active else None,
                padding=ft.Padding(18, 9, 10, 9),
                on_click=lambda e, n=name: on_select(n),
                ink=True,
            )
        )
    items.append(ft.Container(expand=True))
    items.append(
        ft.Container(
            content=ft.Text(
                "プレビュー: " + PREVIEW_BASE,
                color=WP_DIM,
                size=10,
            ),
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


@ft.component
def ArticleList(series, articles, on_edit):
    query, set_query = ft.use_state("")

    q = query.strip().lower()
    visible = [
        a
        for a in articles
        if not q
        or q in a.title_ja.lower()
        or q in a.title_en.lower()
        or q in a.slug.lower()
    ]

    rows = []
    for a in visible:
        title = a.title_ja or a.title_en or a.slug
        open_it = lambda e, art=a: on_edit(art)  # noqa: E731
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(
                            title, color=WP_LINK, size=14, weight=ft.FontWeight.W_500
                        ),
                        on_tap=open_it,
                    ),
                    ft.DataCell(
                        ft.Text(a.slug, size=13, color="#50575e"), on_tap=open_it
                    ),
                    ft.DataCell(
                        ft.Text(a.date, size=13, color="#50575e"), on_tap=open_it
                    ),
                    ft.DataCell(
                        ft.Text(
                            " / ".join(l.upper() for l in a.langs),
                            size=12,
                            color="#50575e",
                        ),
                        on_tap=open_it,
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
                ]
            ),
            ft.Text(f"{len(visible)} 件", size=12, color="#50575e"),
            ft.Container(
                content=ft.Column(
                    [
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("タイトル", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("スラッグ", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("日付", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("言語", weight=ft.FontWeight.BOLD)),
                            ],
                            rows=rows,
                            heading_row_color="#f6f7f7",
                            data_row_min_height=44,
                            column_spacing=24,
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


@ft.component
def Editor(series, article, draft, on_back, set_status):
    saving, set_saving = ft.use_state(False)

    async def save(e):
        set_saving(True)
        try:
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
            if ok:
                set_status((f"更新してビルドしました {_now()}", WP_OK))
            else:
                set_status((f"保存済み・ビルド失敗: {err[:120]}", WP_ERR))
        set_saving(False)

    def open_preview(e):
        webbrowser.open(PREVIEW_BASE + store.article_url(series, article.slug))

    lang_names = {"ja": "日本語", "en": "English"}
    tab_labels = []
    tab_views = []
    for lang in article.langs:
        tab_labels.append(ft.Tab(label=lang_names.get(lang, lang)))
        tab_views.append(
            ft.Container(
                content=ft.TextField(
                    value=draft[lang],
                    multiline=True,
                    expand=True,
                    border=ft.InputBorder.NONE,
                    text_style=ft.TextStyle(
                        font_family="monospace", size=14, color=WP_TEXT
                    ),
                    on_change=lambda e, l=lang: draft.__setitem__(l, e.control.value),
                ),
                bgcolor="white",
                border=ft.Border.all(1, "#c3c4c7"),
                border_radius=3,
                padding=12,
                expand=True,
            )
        )
    # Flet 1.0 の Tabs は length + TabBar + TabBarView 構成
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

    return ft.Column(
        [
            ft.Row(
                [
                    ft.TextButton(
                        content=ft.Text("← 記事一覧に戻る", color=WP_LINK),
                        on_click=lambda _: on_back(),
                    ),
                ]
            ),
            ft.Text(
                article.title_ja or article.title_en or article.slug,
                size=22,
                color=WP_TEXT,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Text(
                f"スラッグ: {article.slug}   日付: {article.date}   "
                "本文は AsciiDoc 形式(見出し ==、強調 *太字*、リスト * …)",
                size=12,
                color="#50575e",
            ),
            tabs,
            ft.Row(
                [
                    ft.Button(
                        "更新中…" if saving else "更新",
                        bgcolor=WP_DARK_ACTIVE,
                        color="white",
                        disabled=saving,
                        on_click=save,
                        height=40,
                    ),
                    ft.OutlinedButton(
                        "プレビュー",
                        icon=ft.Icons.OPEN_IN_NEW,
                        on_click=open_preview,
                        height=40,
                    ),
                    ft.Container(expand=True),
                    ft.Text(
                        f"記事ID: {article.article_id}", size=11, color="#8c8f94"
                    ),
                ],
                spacing=12,
            ),
        ],
        spacing=10,
        expand=True,
    )


@ft.component
def App():
    first = store.list_series()[0][0]
    view, set_view = ft.use_state(
        {
            "screen": "list",
            "series": first,
            "articles": store.load_articles(first),
        }
    )
    status, set_status = ft.use_state(("", WP_OK))

    def select_series(name):
        set_view(
            {"screen": "list", "series": name, "articles": store.load_articles(name)}
        )

    def open_editor(article):
        draft = {
            lang: store.read_body(view["series"], article.article_id, lang)
            for lang in article.langs
        }
        set_view({**view, "screen": "edit", "article": article, "draft": draft})

    def back():
        set_view(
            {
                "screen": "list",
                "series": view["series"],
                "articles": store.load_articles(view["series"]),
            }
        )

    if view["screen"] == "edit":
        content = Editor(
            series=view["series"],
            article=view["article"],
            draft=view["draft"],
            on_back=back,
            set_status=set_status,
        )
    else:
        content = ArticleList(
            series=view["series"],
            articles=view["articles"],
            on_edit=open_editor,
        )

    return ft.Row(
        [
            Sidebar(current=view["series"], on_select=select_series),
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
    page.title = "aiseed.dev 記事エディタ"
    page.bgcolor = WP_BG
    page.padding = 0
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
