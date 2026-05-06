---
slug: claude-debian-13-dev-tools
lang: en
number: "13"
title: Chapter 13 — Building the Development Tools
subtitle: Terminal, shell, editor, Git — the toolkit of a builder
description: Lay the foundation for development on Debian. Terminal emulator, shell (bash / zsh / fish), editor (Zed / Neovim / PyCharm Community), Git, SSH keys. Together with Claude, decide on a toolkit that fits your workflow.
date: 2026.04.23
label: Claude × Debian 13
prev_slug: claude-debian-12-config-management
prev_title: Chapter 12 — Understanding and Managing Configuration
next_slug: claude-debian-14-widget-architecture
next_title: Chapter 14 — Implementing the Widget Architecture
cta_label: Learn with Claude
cta_title: Development starts from the tools.
cta_text: When the tools you use most fit your hands best, productivity has its foundation. The response speed of one keypress matters more than flashy features.
cta_btn1_text: Continue to Chapter 14
cta_btn1_link: /en/claude-debian/14-widget-architecture/
cta_btn2_text: Back to Chapter 12
cta_btn2_link: /en/claude-debian/12-config-management/
---

## Where This Part Fits

Through Part 3, we got Debian to a state where you can do daily work. Part 4 builds, on top of that environment, **the foundation for making things yourself**.

Part 4 is about development, but it isn't "for programmers." In an era when you write code together with Claude, **everyone can become a builder, a little at a time**. Even if you, reading this textbook, have never written a single line of code, that's fine. You just want the toolkit ready — so that when you need to act, you can. That is what Chapter 13 is for.

## Section 1 — Terminal Emulators

### Candidates

- **GNOME Terminal** (GNOME's standard).
- **Konsole** (KDE's standard).
- **Xfce Terminal** (Xfce's standard).
- **Alacritty.** GPU-accelerated, fast.
- **WezTerm.** Feature-rich, configured in Lua.
- **Kitty.** GPU-accelerated, with its own configuration format.

### How to Choose

The DE's standard terminal is enough at first. Use it for a while; if friction shows up, try Alacritty or WezTerm. The difference is **rendering speed and configuration flexibility**.

### Settings

- Font: a Japanese-aware monospace (Source Han Code JP, HackGen, BIZ UD Gothic).
- Font size: usually 11–13 pt; larger on tired days.
- Color scheme: a dark theme (Solarized Dark, Dracula, Gruvbox) is easier on the eyes.
- Transparency: low (5–15%) — so the background is faintly visible.

### Ask Claude ①: Terminal Choice and Theme

> I use [DE name], and my development is [coding frequency / what I mainly do].
> Recommend, with reasons, which I should pick: the standard, Alacritty, or WezTerm.
> Also propose a dark color scheme that is gentle on the eyes, sorted by monitor color temperature and time of day.

## Section 2 — Shell: bash, zsh, or fish

### Three Candidates

- **bash.** Debian's default. Works everywhere.
- **zsh.** Powerful completion and history; highly customizable.
- **fish.** Instant completion and syntax highlighting; gentle learning curve.

### What This Book Recommends

**Beginners stay on bash, then switch to zsh after a while.** fish is also an option, but it has non-POSIX-compatible writing, so be careful when using it for business scripts.

### Minimum Customization for bash

Adding the following to `~/.bashrc` changes the feel.

```bash
# More history
export HISTSIZE=50000
export HISTFILESIZE=100000
export HISTCONTROL=ignoreboth:erasedups

# Colorful ls
alias ll='ls -alFh --color=auto'
alias la='ls -A --color=auto'

# Git-aware prompt (minimal)
parse_git_branch() {
    git branch 2>/dev/null | sed -n '/\* /s///p'
}
PS1='\[\e[32m\]\u@\h\[\e[m\] \[\e[34m\]\w\[\e[m\] \[\e[33m\]$(parse_git_branch)\[\e[m\]\n$ '
```

### If You Switch to zsh

```bash
sudo apt install zsh
chsh -s $(which zsh)     # change login shell to zsh
```

`oh-my-zsh` is the famous framework, but it is heavy. `starship` (a prompt) plus a minimal set of plugins is enough.

### Ask Claude ②: Shell Choice and Minimal Setup

> My command-line experience is [describe]. Of bash, zsh, fish — which should I pick?
> Write the `.[shell]rc` for the chosen shell as a practical minimum.
> Include the main parts: history, completion, prompt, aliases.

## Section 3 — Editor

### Three Recommendations

VS Code is popular, but this book **deliberately doesn't pick it**. It's
Microsoft's, with telemetry that's hard to fully turn off, an extension
ecosystem that bloats fast, and a "kitchen-sink" weight that doesn't fit
the lean AI-native toolkit (Markdown + Python + plain text) we're after.

Instead, we recommend **three editors, chosen by temperament and use case**.

#### 1. Zed — silent, ultra-fast, modern GUI

A clean wipe of VS Code's noise and weight. **If you want to face the text
itself, nothing else**, this is it. Rust + GPU rendering give it
near-instant launch and keystroke response. LSP and Copilot/Claude
integrations are built in, so capability isn't the trade. For people
done with extension hell.

```bash
# Flatpak is the easiest install
flatpak install flathub dev.zed.Zed
```

#### 2. Neovim — terminal-only, taken to its limit

Mouse becomes optional. **Editor on the left, Claude (or `tmux` split) on
the right, every action stays under your fingers**, and SSH'd servers feel
exactly the same. Pick this if you want maximum speed via the keyboard,
and if a 10–20 year skill investment sounds good.

```bash
sudo apt install neovim
```

A minimal modern setup (LSP, treesitter, Telescope) is one minute away
via LazyVim or AstroNvim.

#### 3. PyCharm Community — robust fortress with deep code analysis

The free Community edition is enough. **For when you need to refuse
structural mistakes in AI-generated code and protect serious product
logic.** Type inference, refactoring, debugger — these dwarf both Zed
and Neovim. First choice if Python is your main work.

```bash
flatpak install flathub com.jetbrains.PyCharm-Community
```

### How to Choose

| Temperament / Use | Pick |
|------------------|------|
| Quiet, fast, beautiful UI | **Zed** |
| Keyboard-everything, same flow over SSH, long-term skill | **Neovim** |
| Large Python codebases, frequent refactors, business responsibility | **PyCharm Community** |

When in doubt, **start with Zed**. Lowest learning cost. If Vim bindings
grow on you, descend to Neovim; if Python work scales up, add PyCharm
beside it.

### Bare-Minimum Vim Is Still Required

Whichever you pick as primary, **being able to use `vim` when you SSH
into a server** is basic literacy.

```
hjkl        cursor movement
i           insert mode
Esc         back to normal mode
:w          save
:q          quit
:wq         save and quit
:q!         quit without saving
```

This much is enough for `sudo vim /etc/[whatever]` situations. If you
choose Neovim as primary, this comes for free.

### Ask Claude ③: Editor Configuration

> My current main editor is [Word / Notepad / VS Code / other], and what
> I write is mainly [Japanese documents / Python / Markdown / other].
> From the three options Zed, Neovim, and PyCharm Community, which fits
> my use? Tell me the reasoning and what to set up in the first 30 minutes.
> Also suggest what to keep beside it as secondary or emergency editor.

## Section 4 — Git

### Initial Settings

```bash
sudo apt install git

# User info
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Editor (used to open commit messages, etc.)
git config --global core.editor "zed --wait"    # for Zed
# git config --global core.editor "nvim"        # for Neovim
# git config --global core.editor "charm"       # for PyCharm (via JetBrains Toolbox)

# Default branch name
git config --global init.defaultBranch main

# Pull strategy
git config --global pull.rebase false
```

### Make an SSH Key

For secure connections to GitHub or GitLab, make an SSH key.

```bash
ssh-keygen -t ed25519 -C "you@example.com"
# set a passphrase
cat ~/.ssh/id_ed25519.pub
# copy the output and paste it into GitHub → Settings → SSH and GPG keys
```

### The First Round of Operations

```bash
mkdir ~/my-project
cd ~/my-project
git init
echo "# My Project" > README.md
git add README.md
git commit -m "initial commit"
```

Create a repository on GitHub, then add the remote.

```bash
git remote add origin git@github.com:[you]/my-project.git
git push -u origin main
```

### Ask Claude ④: A Personal Git Cheatsheet

> I'm a Git beginner. Make me a one-page cheatsheet of daily operations, sorted into:
> (1) Start (init, clone).
> (2) Record (add, commit, log).
> (3) Send / receive (push, pull, fetch).
> (4) Branches (branch, checkout, merge).
> (5) Undo mistakes (reset, restore, stash, revert).
> (6) Collaboration (the basic pull-request flow).
>
> For each command, add a minimal example and "use this when …".

## Section 5 — System Adjustments for Developers

### Important Directories

```
~/Projects/           # where projects live
~/bin/                # personal scripts (added to PATH)
~/.local/bin/         # pipx and cargo often install here
```

Add this to `~/.bashrc` to put them on PATH.

```bash
export PATH="$HOME/bin:$HOME/.local/bin:$PATH"
```

### Basic Development Packages

```bash
sudo apt install build-essential curl wget jq ripgrep fd-find tree htop
```

- `build-essential`: gcc and friends. Required to build many things.
- `jq`: JSON formatting.
- `ripgrep` (command: `rg`): a fast grep.
- `fd-find` (`fd`): a fast find.
- `htop`: process monitor.

### Ask Claude ⑤: My Developer Setup

> My use case is [web frontend / data analysis / scripting / other].
> List, in priority order, the common packages I should install for development on Debian, and whether each should come from apt, pipx, npm, or cargo.
> Add a one-line purpose for each package.

## Section 6 — Setting Up Claude Code

Claude Code is the tool for reading and writing code in dialogue with Claude in the terminal. It is the core of Part 4 of this textbook.

```bash
# Node.js and npm are required
sudo apt install nodejs npm

# Install Claude Code (ask Claude for the latest steps)
npm install -g @anthropic-ai/claude-code
```

On first launch, you'll be asked to log in via the browser. Sign in with an Anthropic account.

```bash
cd ~/Projects/my-project
claude
```

That starts the dialogue.

### Knack of Claude Code

- **Launch from the project directory.** It can read files under that directory.
- **Be explicit in instructions.** "Rewrite this function," "add this feature," and so on.
- **Confirm changes.** Claude Code asks before making changes. Always look at the content before approving.

### Ask Claude ⑥: Principles for Operating Claude Code

> Tell me five principles a beginner should keep in mind when using Claude Code:
> (1) How to start (project layout).
> (2) How to phrase instructions.
> (3) How to judge whether to approve a change.
> (4) What to do when things go wrong.
> (5) When not to use it.

## Summary

What you did in this chapter:

1. Picked a terminal emulator and tuned the font and color scheme.
2. Decided on a shell (bash or zsh) and tuned `.bashrc` / `.zshrc`.
3. Built up the editor (Zed / Neovim / PyCharm Community plus minimum Vim).
4. Configured Git, made an SSH key, and connected to GitHub.
5. Installed the basic developer packages.
6. Installed Claude Code.

Where you are now:
- A terminal and shell that fit your hands.
- An editor environment with Git wired in.
- An environment where you can dialogue with Claude through code.

In Chapter 14, we move into a concrete example: writing code with Claude while exploring **the Widget architecture** — the practice of building simple, reusable UI components. The subject is a small GUI app, but the way of thinking transfers to other domains.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
