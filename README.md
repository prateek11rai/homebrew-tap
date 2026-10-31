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

| Formula | Description | Documentation |
| :--- | :--- | :--- |
| **`antigravity-acp`** | Google Antigravity Agent Client Protocol (ACP) server daemon | [Documentation](docs/formulae/antigravity-acp.md) |

*(Version-pinned streams like `<formula>@<version>` are available for supported packages; see individual package documentation).*

### Casks

*(None currently. Future GUI applications will be placed under [`Casks/`](Casks/))*

---

## Managing in Dotfiles (`Brewfile`)

To declare packages from this tap in your machine's `Brewfile`:

```ruby
# Tap declaration
tap "prateek11rai/tap"

# Formula
brew "antigravity-acp"
```

Apply changes on any machine with:

```bash
brew bundle
```

---

## Automated Version Bumping

This repository uses a generic version bumper and CI testing workflow ([`.github/workflows/bump-formula.yml`](.github/workflows/bump-formula.yml)) powered by [`.github/packages.json`](.github/packages.json).

When triggered:
1. Vendor artifacts are downloaded and their SHA-256 checksums are calculated.
2. The formula code files (`Formula/.../*.rb`) and package registry are updated.
3. Strict Homebrew checks (`brew audit`, `brew install --build-from-source`, and `brew test`) run on macOS runners.
4. Verified changes are automatically committed directly to `main`. Documentation remains evergreen and untouched.

---

## Repository Guide

For development rules, packaging conventions, and guidelines on how to add new formulae or casks, refer to [`.agents/AGENTS.md`](.agents/AGENTS.md).
