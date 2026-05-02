---
slug: claude-debian-10-japanese-input
lang: en
number: "10"
title: Chapter 10 — Setting Up Japanese Input
subtitle: Polish Fcitx5 + Mozc into something you can use every day
description: Don't compromise on Japanese input — you use it hundreds of times a day. Together with Claude, finish off the basic Fcitx5 + Mozc configuration, the user dictionary, key bindings, app-specific behavior, emoji and symbol input, and predictive-conversion tuning.
date: 2026.04.23
label: Claude × Debian 10
prev_slug: claude-debian-09-desktop-environment
prev_title: Chapter 9 — Tuning the Desktop Environment
next_slug: claude-debian-11-application-selection
next_title: Chapter 11 — Choosing Applications
cta_label: Learn with Claude
cta_title: Input adds up over the day.
cta_text: Add up all the typing in a single day and it comes to thousands or tens of thousands of characters. Speeding up each conversion by 0.3 seconds saves minutes a day. So don't compromise on Japanese input.
cta_btn1_text: Continue to Chapter 11
cta_btn1_link: /en/claude-debian/11-application-selection/
cta_btn2_text: Back to Chapter 9
cta_btn2_link: /en/claude-debian/09-desktop-environment/
---

## Why Devote a Whole Chapter to Japanese Input

Browser, mail, documents, chat — in the end, all of it comes down to typing Japanese. **The comfort of Japanese input is one of the biggest factors in whether you can keep using Debian.**

Hands trained on Windows MS-IME or the macOS Kotoeri family feel real friction when conversion behavior is even slightly different. This chapter polishes Fcitx5 + Mozc until you can use it every day "without noticing it."

## Section 1 — Install and Activate

If you didn't finish this in Chapter 7, start here.

```bash
sudo apt install fcitx5 fcitx5-mozc fcitx5-config-qt fcitx5-configtool im-config

# Set fcitx5 as the input method
im-config -n fcitx5

# Log out and back in, or reboot
```

On GNOME, input methods are passed through differently between Wayland and X11. **GNOME on Debian 12 defaults to Wayland.** Fcitx5's Wayland support has progressed, but problems may remain in older apps.

### Setting Environment Variables

Place the following in `~/.pam_environment` or under `~/.config/environment.d/` (whether they're needed varies by DE and login manager).

```
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
SDL_IM_MODULE=fcitx
GLFW_IM_MODULE=ibus
```

The last line, `GLFW_IM_MODULE=ibus`, is a trap to know about. GLFW-based apps (some games and certain editors) recognize Fcitx5 even when this is set to `ibus`, so leaving it in covers more cases.

### Ask Claude ①: Confirm Environment Variables

> On my Debian 12 [DE name], I want to verify the Japanese-input environment variables.
> I'm pasting the output of:
> ```
> $ env | grep -iE '(xim|im_module|modifiers)'
> [output]
> ```
>
> Please judge whether this configuration enables Japanese input across all of: browser, terminal, GTK apps, Qt apps, VSCode, and Electron apps.
> If anything is missing or unnecessary, give me the steps to fix it.

## Section 2 — Basic Key Bindings

### Choosing the Toggle Key

The default is `Ctrl + Space` to switch between Japanese and alphanumeric. If you use a Japanese keyboard, **bind it to the Hankaku/Zenkaku key or the Katakana/Hiragana key** so it matches the action your hands already know.

- Launch the Fcitx5 settings tool (`fcitx5-config-qt`).
- "Global Options" → change "Trigger Input Method."

### Mozc Internal Key Bindings

For Mozc's conversion behavior, you can pick from MS-IME and ATOK styles.

- Fcitx5 settings → Input Method → Mozc → Configure.
- Key configuration: MS-IME / ATOK / Kotoeri.

Pick the one your hands are used to. If unsure, MS-IME.

### Useful Key Operations (MS-IME Mode)

- `F6`: convert to hiragana.
- `F7`: full-width katakana.
- `F8`: half-width katakana.
- `F9`: full-width alphanumeric.
- `F10`: half-width alphanumeric.
- `Ctrl + Backspace`: revert to before conversion.
- `Shift + Space`: cycle through conversion candidates in reverse.

## Section 3 — Cultivating the User Dictionary

Register the vocabulary you use every day in the dictionary. Six months from now, the difference between doing this and not doing this is large.

### How to Register

A word converted once in Mozc stays in internal history, but for frequent words, register them explicitly.

- Gear icon on the input bar → Dictionary Tool.
- Add to "User dictionary": reading, word, part of speech.

### Examples of Words Worth Registering

- Proper nouns: company names, family members' names, place names, project names.
- Technical terms: commands and tool names that come up at work.
- Set phrases: "よろしくお願いいたします" → convert from `よ`.
- Email signatures, addresses, phone numbers.

### Ask Claude ②: Candidate Words for Registration

> I am [your industry / role]. Of the Japanese I type every day, please list 20 words in each of the following categories that, if registered in the dictionary, would speed me up:
> (1) Proper nouns and technical terms specific to my work.
> (2) Set phrases for email and chat.
> (3) Kanji you guess I find slow to enter (educated guess).
>
> Add the "reading" and "part of speech" for each word.

Cherry-pick from what comes back and register it yourself.

### Export and Import

The user dictionary can be exported as a text file. Carry it across to another PC or a reinstall.

- Dictionary Tool → Tool → Import / Export from text file.

**This dictionary file is worth managing under Git as `my-mozc-dict.txt`.** A dictionary you've grown over years is your asset.

## Section 4 — Tune Conversion Behavior

### Predictive Conversion On / Off

Predictive conversion (suggestions appearing as you type) divides people.

- For: faster — candidates appear before you've finished thinking.
- Against: distracting; mistypes go up.

Fcitx5 settings → Mozc → Properties → Input assistance: turn predictive input on / off.

### Half-Width vs. Full-Width Symbols

If you want to enter symbols like `!`, `?`, `(` in half-width form, Mozc supports fine-grained control like "Japanese punctuation, but half-width alphanumerics."

### Reset Learning

Use it for a while and conversion learning can drift, putting weird candidates first.

- Dictionary Tool → Tool → Clear learning history.

Doing this once every six months brings things back into shape.

## Section 5 — App-Specific Behavior

### Browsers (Firefox / Chromium)

These work without much trouble. If candidates don't appear or you can't reconvert, restart the browser.

### VSCode

VSCode is Electron-based, and older versions had Japanese-input issues. The latest versions (2024+) are much better.

```bash
# The apt or Microsoft official repository is preferred over Flatpak.
# Ask Claude for the current installation method.
```

### JetBrains Family (IntelliJ, PyCharm, etc.)

Compatibility with the JDK can shift the input cursor position.

### Ask Claude ③: App-Specific Behavior Check

> The apps I use Japanese input in are [list]. Does Fcitx5 + Mozc work properly in each?
> List the issues that have been reported in the past, with workarounds.

## Section 6 — Key Repeat and Input Speed

The faster you type, the more key-repeat settings matter.

- GNOME: Settings → Accessibility → Keyboard → Repeat delay / speed.
- KDE: System Settings → Input Devices → Keyboard → Advanced.

Shortening the delay and increasing the speed makes selection-extension and arrow-key navigation faster.

## Section 7 — AI-Assisted Japanese Input

Claude isn't a replacement for Japanese input, but it is an aid.

- Write a long passage colloquially, then have Claude rewrite it in formal or casual register.
- Have Claude translate context-aware between English and Japanese.
- Have Claude draft an email and edit it yourself.

If you drop the assumption that "I have to type every word myself," Japanese input takes a different place in your day. That said, **always re-read important text yourself**. Claude can miss honorifics or industry conventions in Japanese.

### Ask Claude ④: How to Use Claude as a Japanese Drafting Aid

> I am in [industry], and I write [emails / meeting minutes / reports] N each per day. Tell me five practices for letting Claude draft Japanese text:
> (1) The shape of the instruction (what / to whom / how polite).
> (2) How to teach Claude my own writing style.
> (3) Self-check points after the draft.
> (4) Kinds of writing I should not delegate to Claude.
> (5) The balance between efficiency and responsibility.

## Summary

What you did in this chapter:

1. Installed Fcitx5 + Mozc and set up the environment variables.
2. Chose the toggle key and conversion style (MS-IME / ATOK).
3. Started cultivating a user dictionary (exported as `my-mozc-dict.txt`).
4. Learned how to tune predictive conversion and clear learning history.
5. Checked app-specific behavior.
6. Acquired the practice of using Claude as a Japanese drafting aid.

Where you are now:
- A Debian where Japanese input feels seamless.
- Your own user dictionary (backed up).
- Faster typing, physically, every day.

In Chapter 11, "Choosing Applications," we work through, with Claude, what to replace each Windows app with on Debian. Browser, mail, office, image / video, communication tools, file sync, password management — sorted out one at a time.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
