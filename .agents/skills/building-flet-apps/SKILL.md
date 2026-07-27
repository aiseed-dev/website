---
name: building-flet-apps
description: Conventions and patterns for building Flet desktop/mobile/web apps on the **Flet 1.0 Beta (0.80.x) / 0.85.0 line** — the post-rewrite declarative API. Use this skill when adding a new Flet-based app to the repo, drafting Flet code in any chapter / example folder, or reviewing Flet code for whether it follows the 1.0 conventions instead of the legacy 0.28.x patterns. Covers the imperative / declarative split, `@ft.component` + hooks (`use_state`, `use_dialog`, `use_route_outlet`), `ft.Router` declarative navigation, version pinning, install commands for `uv` and `pip`, the most common 0.28 → 0.80 migration breakages, and the small surface of `flet-video` / `AudioRecorder` streaming that ships with 0.85.0.
---

# Building Flet apps (1.0 Beta / 0.85.0 line)

This skill captures the conventions for the **current Flet line** ── Flet 1.0 Beta, shipped as 0.80.0 on PyPI in Dec 2025, with 0.85.0 (May 2026) adding declarative `Router` and `use_dialog()`. The legacy line is 0.28.3 ── only relevant when freezing an existing 0.28 codebase.

The source of truth is the two Flet announcement posts (Dec 2025 / May 2026). Anything not stated here should be verified at <https://flet.dev/docs/>, which is regenerated from the codebase and stays in sync with the API.

## The version landscape

| Line | Status | When to use |
|---|---|---|
| **0.80.x — 1.0 Beta** (current) | API 99% stable, recommended for **all new apps** | New code in this repo |
| **0.85.x** (current minor) | Adds declarative `Router`, `use_dialog()`, better `flet-video` / `AudioRecorder` | New code that needs routing or dialogs in declarative mode |
| **0.28.x** (legacy) | Bug/security fixes only, no new features | Only when an existing 0.28 app cannot be migrated yet |

`pip install flet` (or any unpinned add) **now installs 0.80+**. This is not a drop-in upgrade ── 0.80.0 has [breaking changes](https://github.com/flet-dev/flet/issues/5238) vs 0.28.x. If an existing app must stay on the old line, pin explicitly:

```toml
# pyproject.toml or requirements.txt
flet==0.28.3
```

## Install / upgrade

### `uv`-managed project (preferred — matches the series ethos)

```bash
# New project: just add and sync
uv add 'flet[all]'

# Existing project, upgrade everything
uv sync --upgrade

# Existing project, upgrade only Flet packages
uv sync \
  --upgrade-package flet \
  --upgrade-package flet-cli \
  --upgrade-package flet-desktop \
  --upgrade-package flet-web

# Force a re-resolve when upgrading 0.28 → 0.80
rm uv.lock
uv sync
```

### `pip`-managed project

```bash
pip install 'flet[all]' --upgrade
```

> Built-in extensions (`flet-audio`, `flet-video`, `flet-audio-recorder`, etc.) are now released with the **same version number** as core `flet`. Pin and upgrade them together — don't let dependency resolution leave them on an older line.

## Two styles, one framework

Flet 1.0 supports **both**:

- **Imperative** — `page.add(...)`, `page.show_dialog(...)`, mutate controls and call `page.update()`. The 0.28.x style; still fully supported.
- **Declarative** — `@ft.component` functions return a control tree that is a pure function of state; framework diffs and applies the minimum delta. Uses hooks (`use_state`, `use_dialog`, `use_route_outlet`).

**Default to declarative for new code** unless the app is essentially a single static page with no dynamic state. Declarative scales better as the app grows ── that's the explicit goal of the 1.0 architecture.

The declarative entry point:

```python
import flet as ft

@ft.component
def App():
    return ft.Text("Hello", size=24)

ft.run(lambda page: page.render(App))
```

The imperative entry point (legacy/mixed):

```python
import flet as ft

def main(page: ft.Page):
    page.add(ft.Text("Hello", size=24))

ft.app(main)
```

Mixing is allowed — declarative components can be rendered inside an imperatively built page — but pick a primary style per top-level screen to keep the data flow clear.

## Declarative essentials: `@ft.component` + hooks

### `use_state` — local reactive state

```python
@ft.component
def Counter():
    count, set_count = ft.use_state(0)

    return ft.Column([
        ft.Text(f"Count: {count}", size=24),
        ft.Button("Increment", on_click=lambda _: set_count(count + 1)),
    ])
```

The tuple is `(value, setter)`. Calling `set_count(...)` triggers a re-render; the component re-runs and Flet diffs the returned tree against the previous one.

### `use_dialog` — declarative dialogs (0.85.0)

Dialogs are now reactive state, not imperative `page.show_dialog()` calls. Pass a `DialogControl` to show it, pass `None` to dismiss it. The hook portals the dialog into the page's dialog overlay automatically and removes it when the component unmounts.

```python
import asyncio
import flet as ft

@ft.component
def App():
    show, set_show = ft.use_state(False)
    deleting, set_deleting = ft.use_state(False)

    async def handle_delete():
        set_deleting(True)
        await asyncio.sleep(2)  # placeholder for the real delete
        set_deleting(False)
        set_show(False)

    ft.use_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete report.pdf?"),
            content=ft.Text(
                "Deleting, please wait..." if deleting else "This cannot be undone."
            ),
            actions=[
                ft.Button(
                    "Deleting..." if deleting else "Delete",
                    disabled=deleting,
                    on_click=handle_delete,
                ),
                ft.TextButton(
                    "Cancel",
                    on_click=lambda _: set_show(False),
                    disabled=deleting,
                ),
            ],
            on_dismiss=lambda _: set_show(False),
        )
        if show
        else None
    )

    return ft.Button("Delete File", icon=ft.Icons.DELETE,
                     on_click=lambda _: set_show(True))
```

Key properties:

- **Frozen-diff updates.** When the component re-renders and you pass back a new dialog instance with different field values, the hook diffs it field-by-field and emits only the actual deltas — a `TextField` inside the dialog keeps cursor, focus, and selection across re-renders even though Python is handing the framework a new control object each build. **Build dialogs normally; do not try to cache instances yourself.**
- **Multiple dialogs per component are fine.** Call `use_dialog()` more than once in the same component to manage independent dialogs (e.g. a rename dialog and a delete dialog) — each one is tracked separately.

### `use_route_outlet` — layout slots in nested routes

Inside a layout component that wraps child routes via `ft.Router`:

```python
@ft.component
def AppLayout():
    outlet = ft.use_route_outlet()
    return ft.Column([
        # ... shared chrome (app bar, nav) ...
        ft.Container(content=outlet, padding=20),  # child route renders here
    ])
```

## Routing: `ft.Router` (0.85.0)

Declarative, React Router-style. A `Router` matches the current page route against a tree of `Route` definitions and renders the matched component chain. Replaces hand-rolled `page.on_route_change` + `views` plumbing for declarative apps.

### Flat routes

```python
import flet as ft

@ft.component
def Home():    return ft.Text("Home page", size=24)

@ft.component
def About():   return ft.Text("About page", size=24)

@ft.component
def App():
    return ft.SafeArea(
        content=ft.Column([
            ft.Row([
                ft.Button("Home",
                          on_click=lambda _: ft.context.page.navigate("/")),
                ft.Button("About",
                          on_click=lambda _: ft.context.page.navigate("/about")),
            ]),
            ft.Router([
                ft.Route(index=True, component=Home),
                ft.Route(path="about", component=About),
            ]),
        ])
    )

ft.run(lambda page: page.render(App))
```

### Nested routes with a shared layout

```python
@ft.component
def App():
    return ft.Router([
        ft.Route(component=AppLayout, children=[
            ft.Route(index=True, component=Home),
            ft.Route(path="about", component=About),
        ]),
    ])
```

The parent `Route` declares the layout; `use_route_outlet()` inside `AppLayout` is where each child renders.

### Router features (use as needed)

- **Dynamic segments**: `path="users/:id"` — match `/users/42`, `/users/abc`.
- **Optional segments**: `path="posts/:id?"` — match `/posts` and `/posts/42`.
- **Splats**: `path="files/*"` — catch-all.
- **Regex constraints** on segment values.
- **Data loaders** run before a route renders (do fetches here, not inside the component).
- **Active link detection** for highlighting current-route nav items.
- **Auth guards** — block a route, redirect to login, then return.
- **`manage_views=True`** — switches Router into view-stack mode where each route returns a full `View` with its own `AppBar`. Navigating deeper pushes views onto the stack; on mobile the user can swipe back / tap the AppBar back button. Use this for mobile-feeling apps; leave the default for desktop-feeling apps.

Navigate from anywhere: `ft.context.page.navigate("/some/path")`. Pop the view stack to a specific depth (and return a result): `page.pop_views_until(...)`.

References: PR [#6406](https://github.com/flet-dev/flet/pull/6406), guide <https://flet.dev/docs/cookbook/router>, control docs <https://flet.dev/docs/controls/router>.

## Media (0.85.0)

### `flet-video`

```python
import flet_video as fv

async def handle_screenshot(e):
    image_bytes = await video.take_screenshot()
    # save / upload / display in an Image

video = fv.Video(
    playlist=[fv.VideoMedia("https://example.com/clip.mp4")],
    on_position_change=lambda e: print(f"At {e.position}s"),
    on_duration_change=lambda e: print(f"Duration: {e.duration}s"),
)
```

- Control bar is fully configurable: use built-ins, replace with your own widgets, hide entirely, or use different controls in normal vs fullscreen mode.
- `Video.take_screenshot()` captures the currently displayed frame.
- `on_position_change` fires as playback progresses (drives custom progress bars).
- `on_duration_change` fires when duration becomes known (or changes between playlist entries).

### `AudioRecorder` PCM16 streaming

For real-time use (voice activity detection, live transcription, streaming an LLM voice assistant) the recorder now emits raw PCM16 chunks via `on_stream`:

```python
import flet as ft
import flet_audio_recorder as far

def main(page: ft.Page):
    buffer = bytearray()

    def handle_stream(e: far.AudioRecorderStreamEvent):
        buffer.extend(e.chunk)
        status.value = (
            f"Streaming chunk {e.sequence}; {e.bytes_streamed} bytes."
        )

    async def start(e):
        buffer.clear()
        await recorder.start_recording(
            configuration=far.AudioRecorderConfiguration(
                encoder=far.AudioEncoder.PCM16BITS,
                sample_rate=44100,
                channels=1,
            ),
        )

    recorder = far.AudioRecorder(on_stream=handle_stream)
    page.add(ft.Button("Start", on_click=start), status := ft.Text())
```

For server-side capture without buffering through Python, point the recorder at an upload URL:

```python
upload_url = page.get_upload_url(file_name="rec.pcm", expires=600)
await recorder.start_recording(
    upload=far.AudioRecorderUploadSettings(
        upload_url=upload_url, file_name="rec.pcm",
    ),
    configuration=far.AudioRecorderConfiguration(
        encoder=far.AudioEncoder.PCM16BITS,
    ),
)
```

## Other 0.85.0 additions worth knowing

- `NavigationRail` is scrollable; `pin_leading_to_top` / `pin_trailing_to_bottom` keep header/footer pinned while the middle scrolls.
- `ResponsiveRow` supports scroll for layouts whose content exceeds available height.
- `CodeEditor.issues` shows analysis error markers in the gutter; the analysis itself runs in Python.
- `NavigationDrawerDestination.label` now accepts custom controls; theme via `NavigationDrawerTheme.icon_theme`.
- `DragTargetEvent.local_position` / `global_position` are the way to read positions; the old `x`, `y`, `offset` are deprecated.
- `Page.theme_animation_style` customizes the cross-fade between `theme` and `dark_theme`.

## Common 0.28 → 0.80 migration breakages

(Not exhaustive — see [the breaking-changes issue](https://github.com/flet-dev/flet/issues/5238) for the full list.)

Whenever Flet code in this repo shows any of these patterns, it's pre-1.0 and needs migrating:

- **`page.show_dialog(d)` / `page.close_dialog()`** in a declarative component → replace with `ft.use_dialog(d if show else None)`.
- **Hand-rolled route handling** via `page.on_route_change` + manipulating `page.views` → replace with `ft.Router` + `ft.Route` tree.
- **`DragTargetEvent.x` / `.y` / `.offset`** → use `local_position` / `global_position`.
- **`Duration(seconds=2.0)` with a float** silently decoded to `0` on some older paths; use `int` seconds or a richer literal (fixed in 0.85.0 but worth catching when reading old code).
- **`auto_scroll=True` without `scroll=...`** silently did nothing; both must be set.
- **`flet pack` desktop bundles** on Windows / Linux were missing the client archive in some 0.28 patch versions — rebuild with 0.80+ and verify the bundle layout.

## CLI: `flet debug` and friends

0.80 ships `flet debug` for stepping through an app on real devices and emulators (see `flet devices`, `flet emulators`). Use it instead of attaching ad-hoc loggers when chasing a mobile-only bug. The CLI surface is documented at <https://flet.dev/docs/cli/>.

## Conventions for code added to this repo

When code (chapter examples, blog code snippets, a future migration tool) uses Flet:

1. **Target 0.80+ unless explicitly migrating an existing 0.28 app.** Pin the Flet version in `pyproject.toml` if reproducibility matters.
2. **Default to declarative (`@ft.component` + hooks).** Use imperative only for trivially small one-screen utilities or when extending an existing 0.28 codebase.
3. **Use `ft.Router` for any app with more than one screen.** Don't hand-roll route handling.
4. **Use `ft.use_dialog()` for dialogs in declarative components.** Do not mix imperative `page.show_dialog` with declarative state — pick one model per component.
5. **Keep `flet`, `flet-video`, `flet-audio`, `flet-audio-recorder`, etc. at the same version.** They release in lockstep; mismatched versions surface as obscure missing-attribute errors at runtime.
6. **Cite the docs and PR numbers** when a behavior is non-obvious (e.g. the frozen-diff dialog detail). The Flet docs are generated from code, so a doc link is the most stable reference; PR numbers help when the doc lags.

## Sources

- Flet 1.0 Beta announcement (Dec 24, 2025) — version 0.80.0, declarative style introduced as a first-class option.
- Flet 0.85.0 announcement (May 11, 2026) — `Router`, `use_dialog()`, `flet-video` controls, `AudioRecorder` streaming.
- Flet documentation: <https://flet.dev/docs/>
- Breaking-changes tracker: <https://github.com/flet-dev/flet/issues/5238>
