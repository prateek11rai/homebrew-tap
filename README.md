# Homebrew Tap (`prateek11rai/tap`)

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
