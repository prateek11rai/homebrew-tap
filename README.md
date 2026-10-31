<p align="center">
  <img src="assets/banner.svg" alt="prateek11rai/tap Homebrew Tap" width="100%">
</p>

<p align="center">
  <a href="https://brew.sh"><img src="https://img.shields.io/badge/Homebrew-Tap-FBBF24?style=flat-square&logo=homebrew&logoColor=black" alt="Homebrew Tap"></a>
  <img src="https://img.shields.io/badge/Platform-macOS%20(arm64%20%7C%20x86__64)-0f172a?style=flat-square&logo=apple&logoColor=white" alt="macOS Supported">
  <img src="https://img.shields.io/badge/Integrity-SHA--256%20Verified-10b981?style=flat-square" alt="SHA-256 Verified">
</p>

---

Personal Homebrew tap for custom formulae, casks, and standalone binary distributions that lack official upstream packaging in `homebrew/core`.

---

## Adding the Tap

Add this tap to your local Homebrew installation:

```bash
brew tap prateek11rai/tap
```

You can also install packages directly without tapping first using the single-slash shorthand:

```bash
brew install prateek11rai/<formula>
```

---

## Available Packages

### Formulae

| Formula | Description | Version | Documentation |
| :--- | :--- | :--- | :--- |
| **`antigravity-acp`** | Antigravity Agent Client Protocol (ACP) server daemon for IDEs & editors | `1.4.1` | [Documentation](docs/formulae/antigravity-acp.md) |

### Casks

*(None currently. Future GUI applications will be placed under [`Casks/`](Casks/))*

---

## Managing in Dotfiles (`Brewfile`)

To declare packages from this tap in your machine's `Brewfile`:

```ruby
# Tap declaration
tap "prateek11rai/tap"

# Formulae
brew "antigravity-acp"
```

Apply changes on any machine with:

```bash
brew bundle
```

---

## Repository Guide

For development rules, packaging conventions, and guidelines on how to add new formulae or casks, refer to [`.agents/AGENTS.md`](.agents/AGENTS.md).
