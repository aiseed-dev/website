---
slug: apps
number: "08"
lang: en
title: "Building Apps — CLI Tools, Flet Apps, Flutter Apps"
subtitle: "A three-layer structure that scales up gradually"
description: To build an app, you don't need Flutter from the start. Write a CLI tool first and run it. If a screen is needed, put a GUI on top with Flet — still in Python. If serious cross-platform delivery is needed, move to Flutter. Climb the three layers in stages — small risk, AI-friendly.
date: 2026.05.02
label: AI Native 08
title_html: Start apps from <span class="accent">CLI</span>,<br>extend through <span class="accent">Flet</span> and <span class="accent">Flutter</span>.
prev_slug: web
prev_title: "Building for the Web — Back to HTML+CSS+JavaScript"
next_slug: embedded
next_title: "Building Embedded — Think in Python, Have Claude Translate"
---

# Building Apps — CLI Tools, Flet Apps, Flutter Apps

When building an app, don't start with Flutter, React Native, or Swift.

**Start with CLI.** Get it running. If a screen is needed, layer a GUI on top with Flet. If that is not enough, move to Flutter. Climb three layers in stages. This is the AI-native way to build.

## Three layers

Think of app-building tools in three stages.

| Layer | Tool | Purpose |
|-------|------|---------|
| Layer 1 | CLI tool (Python) | Write the core processing, run it, validate it |
| Layer 2 | Flet app (Python) | When a screen is needed, layer a GUI in Python |
| Layer 3 | Flutter app (Dart) | Serious cross-platform app |

A new app starts at Layer 1. Move to Layer 2 only after the CLI works. Move to Layer 3 only when Flet is not enough.

**Less rework, less code.**

## Layer 1: start with a CLI tool

The essence of an app is: take input, process, produce output.

The first thing to write is a command-line tool.

```python
import sys

def main(args):
    input_file = args[0]
    # processing here
    print("done")

if __name__ == "__main__":
    main(sys.argv[1:])
```

That gives you an app where "running a command makes something happen." No GUI. Easy to test. Easy to debug. Easy for Claude to write.

Once the CLI tool works, you can ship it. Mac/Linux/Windows, all OSes (with Python). You don't even need to host it on the web. `pip install` distributes it.

**Many apps need only the CLI.** Processing data, converting files, hitting APIs — these don't need a GUI.

## Layer 2: put a GUI on with Flet

When CLI is not enough — non-technical users, visual feedback needed, multiple input fields — a screen is needed.

Before learning Flutter, try Flet.

Flet is a Python GUI framework. It uses Flutter's rendering engine internally, but you write Python. The Layer 1 CLI code can ride on top of the GUI almost unchanged.

```python
import flet as ft

def main(page: ft.Page):
    name = ft.TextField(label="Name")
    result = ft.Text()

    def greet(e):
        result.value = f"Hello, {name.value}"
        page.update()

    page.add(name, ft.ElevatedButton("Greet", on_click=greet), result)

ft.app(main)
```

That gives you a GUI app with a text field, a button, and an output area. It runs on Mac, Windows, Linux, the web browser, and mobile (iOS/Android). **You write only Python.**

Flet is new (released 2022). But it is already usable for production. Claude can write it.

## Layer 3: Flutter

When Flet is not enough — advanced animation, native API access, distribution channels (App Store, Play Store) — only then consider Flutter.

Flutter is written in Dart. Dart is a statically typed language similar to Java or C#. New to learn, but Claude can write it. **You don't need to write Dart yourself.** Have Claude write it; you read and judge.

After validating logic in Python at Layers 1–2, port to Flutter. **Correctness is already verified in Python**, so the Dart side can focus on UI and OS integration only.

That removes half the complexity of a Flutter project.

## Why not Swift / Kotlin?

iOS-only or Android-only apps can be written in Swift or Kotlin. But not as a first choice.

Two reasons.

One: cross-platform cost. To build the same app for both iOS and Android, Flutter is dramatically cheaper. Writing in Swift and Kotlin separately doubles the code volume and doubles the maintenance burden.

Two: AI-writability. Claude can write Swift and Kotlin too. But the output quality is more stable for Python and Dart. Latest `SwiftUI` or `Jetpack Compose` specifications change quickly, and AI training data sometimes lags.

If there is a clear iOS-only reason (Apple Watch integration, Vision Pro exclusive), pick Swift. Otherwise, Flutter is fine.

## Not React Native either

The thinking "I can write in React, so React Native" — as covered in the web chapter — is no longer something we actively recommend.

Flutter has higher rendering quality, fewer dependencies, and Dart is easier for AI to write than JavaScript. **Stepping away from the React ecosystem** is a Mythos-era safety strategy.

## How to distribute

CLI tool: PyPI (`pip install`), GitHub releases, your own website.

Flet app: distributable as a Flet package (build to OS-specific executables). The web build is just hosted on a website.

Flutter app: App Store, Play Store, web, desktop apps — all possible.

**The higher the layer, the more distribution channels, but also the more friction.** You don't need to aim for the highest layer. CLI is often enough.

## Example: a personal photo organizer

An example. You want an app that "groups camera photos into folders by capture date."

Write at Layer 1 (CLI):

```python
# python organize.py /path/to/photos
import sys, shutil, os
from PIL import Image
from PIL.ExifTags import TAGS

def main(folder):
    for f in os.listdir(folder):
        if not f.lower().endswith(('.jpg', '.jpeg')):
            continue
        path = os.path.join(folder, f)
        img = Image.open(path)
        exif = img._getexif() or {}
        date = next((v for t, v in exif.items() if TAGS.get(t) == 'DateTimeOriginal'), None)
        if date:
            ymd = date[:10].replace(':', '-')
            target = os.path.join(folder, ymd)
            os.makedirs(target, exist_ok=True)
            shutil.move(path, os.path.join(target, f))

if __name__ == "__main__":
    main(sys.argv[1])
```

Ask Claude "write Python that groups photos into folders by capture date" and this comes out in 30 seconds. Run it, it works.

Distributable now (if it's just for you, you're done).

If family or friends should use it too, move to Layer 2. Wrap a Flet GUI around it. Now there's a "select folder" button and "run" button.

If you want to sell it on the App Store (really?), move to Layer 3. Rewrite in Flutter. Have Claude convert the Python logic to Dart.

**In most cases, you stop at Layer 1.** That is fine.

## In numbers

A photo-organizing app (sort by capture date):

- CLI version: 30 lines of Python, **30 minutes** to develop, distributed by pushing to GitHub
- iOS app: 200 lines of Swift, 50 GB of Xcode environment, 1-week App Store review, $99/year membership

Development environment disk usage:

- Flutter: Android Studio + Flutter SDK + Xcode = **~50 GB**
- Flet: Python alone = **~100 MB** (Flutter distribution unpacked only when needed)
- CLI tool: **20 MB**

CLI tool creation and distribution: 1 hour to write, `pip install` instantly distributes worldwide to Python users. Distributing the same as an "app" requires reviews from 3 App Stores and 2 SDKs. **A 2+ week gap.**

Adding a Flet GUI to existing CLI logic: install Flet, add tens of lines of code, **1 hour**. Rewriting in Flutter: 1 month.

## In summary

Apps start at the CLI.

Build a working CLI, validate it. Add a GUI with Flet if needed. Move to Flutter for cross-platform distribution if needed.

**Each step up still uses the processing code from the CLI.** Start where AI writes most easily; expand only as needed. This is AI-native app development.

The next chapter moves to embedded — "Think in Python, have Claude translate to C." Hardware meets AI.

---

## Related

- [Chapter 07: Building for the Web — Back to HTML+CSS+JavaScript](/en/ai-native-ways/web/)
- [Chapter 04: Writing Logic — Have AI Write Python For You](/en/ai-native-ways/python/)
- [Structural Analysis 15: Security Design for the Mythos Era](/en/insights/security-design/)
