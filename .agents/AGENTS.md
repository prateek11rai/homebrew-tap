# AGENTS.md — Repository Operating Guide

System instructions and conventions for AI agents and maintainers working in this repository (`prateek11rai/homebrew-tap`).

---

## 1. Repository Purpose & Scope

This repository is a personal, public GitHub-hosted **Homebrew Tap** (`prateek11rai/tap`).  
Its primary purpose is to package, distribute, and maintain custom formulae, casks, and standalone binary releases that:
1. Lack official upstream packaging in `homebrew/core` or `homebrew/cask`.
2. Require direct binary downloads from vendor CDNs while preserving system integrity (checksum validation, automated PATH management, clean uninstalls).
3. Support local developer environments and workflows across agent runtimes and modern developer tooling.

---

## 2. Directory Layout & Architecture

Agents must adhere strictly to Homebrew's directory structure:

```text
homebrew-tap/
├── .agents/
│   └── AGENTS.md                    # Agent instructions and repository conventions (this file)
├── .github/
│   ├── packages.json                # Package registry & artifact template metadata
│   ├── scripts/
│   │   └── bump.py                  # Generic Python script for SHA-256 calculation & formula updating
│   └── workflows/
│       └── bump-formula.yml         # GitHub Actions workflow: audit, build, test & direct push to main
├── assets/                          # Repository visuals (banner.svg, brew-logo.svg)
├── Formula/                         # Command-line tools, headless daemons, and standalone binaries
│   └── <package-name>/              # Grouped package folder
│       ├── <package-name>.rb        # Default / latest stable formula (symlinked to bin)
│       └── <package-name>@<ver>.rb  # Pinned minor versioned formula (marked keg_only)
├── Casks/                           # GUI macOS applications (.app bundles, DMGs, PKGs)
│   └── <cask-name>.rb               # (Reserved for future casks)
├── docs/                            # In-depth package documentation
│   ├── formulae/
│   │   └── <package-name>.md        # Architecture, upstream CDN patterns, verification, client setup
│   └── casks/
│       └── <cask-name>.md           # (Reserved for future cask docs)
├── .gitignore                       # Standard Homebrew tap ignores
└── README.md                        # Lean public entrypoint: tap instructions, package list, dotfiles setup
```

---

## 3. Evergreen Documentation Standard (Zero Documentation Maintenance on Bumps)

To maintain simplicity, eliminate documentation staleness, and prevent fragile regex automation:

1. **Only Primary Packages in `README.md`:**  
   The `README.md` package table only indexes the **main package identifier** (e.g. `antigravity-acp`). It does **not** list individual version variants (`@1.4`, `@1.5`).
2. **Generic Formula Documentation:**  
   Individual package docs in `docs/formulae/<package>.md` document the tool's architecture, upstream CDN patterns, installation commands, and client integration. They do not hardcode transient patch versions or version tables.
3. **No Markdown Updates During Version Bumps:**  
   The automated version bump script (`bump.py`) and workflow (`bump-formula.yml`) **never edit markdown files**. They strictly modify:
   * The formula Ruby code files (`Formula/<package>/*.rb`)
   * The metadata manifest (`.github/packages.json`)
4. **Inspecting Live Versions:**  
   Users inspect current installed and available versions using standard Homebrew commands:
   ```bash
   brew info prateek11rai/<formula>
   ```

---

## 4. Formula Organization & Versioning Standards

### Grouping in `Formula/<package-name>/`
Formulas are organized into package subdirectories under `Formula/`. Homebrew scans `Formula/**/*.rb` recursively.

### Default vs. Versioned Formulas
* **Default formula (`Formula/<package>/<package>.rb`):**  
  * Tracks the newest stable release.  
  * Class name: standard CamelCase (e.g. `class AntigravityAcp < Formula`).  
  * Symlinked into `/opt/homebrew/bin/`.
* **Versioned formula (`Formula/<package>/<package>@<ver>.rb`):**  
  * Pinned to a major or minor branch (e.g. `@1.4`).  
  * Class name: Homebrew converts `@` to `AT` (e.g. `class AntigravityAcpAT14 < Formula`).  
  * **Must include `keg_only :versioned_formula`** to prevent binary filename collisions.

### Minor Version Lifecycle:
* **Patch releases (e.g. `1.4.1` → `1.4.2`):** Updates the active minor branch (`@1.4`) in place alongside the default formula.
* **New Minor releases (e.g. `1.5.0`):** The previous minor branch (`@1.4`) is preserved permanently in the repo. A new formula (`@1.5`) is generated automatically, and the default formula is bumped to the new version.

---

## 5. Automated Version Bumping & Testing Workflow

This repo includes a fully automated version bumper framework:

### Registry: `.github/packages.json`
Every package managed by the bumper has an entry defining its artifact URL templates:
```json
{
  "name": "antigravity-acp",
  "formula_path": "Formula/antigravity-acp/antigravity-acp.rb",
  "current_version": "1.4.1",
  "artifacts": {
    "arm64": { "url_template": "...{version}..." },
    "x86_64": { "url_template": "...{version}..." }
  }
}
```

### Script: `.github/scripts/bump.py`
* Downloads the vendor archives for `arm64` and `x86_64`.
* Computes official `sha256` checksums.
* Updates the target `.rb` formula with the new version, URLs, and checksums.
* Auto-creates new `@minor` branches if a new minor release is detected.
* Updates `current_version` in `.github/packages.json`.

### GitHub Actions: `.github/workflows/bump-formula.yml`
Runs on a macOS GitHub Actions runner:
1. Executes `.github/scripts/bump.py` with given inputs.
2. Validates strict Homebrew standards and runs test suites:
   ```bash
   brew audit --strict "$FORMULA_PATH"
   brew install --build-from-source "$FORMULA_PATH"
   brew test "$FORMULA_PATH"
   brew uninstall "$FORMULA_PATH"
   ```
3. **Direct Push to `main`:** If and only if all tests pass, the action auto-commits with `<package>: update to <version>` and pushes directly to `main` using GitHub Actions bot credentials.

---

## 6. Confidentiality & Public Repository Boundary

> [!IMPORTANT]
> This is a **public open-source repository**.  
> **Never include internal company project names, proprietary tool references, internal hostnames, or private credentials** in public documentation, commit messages, or formulas.  
> Always use generic, standard terminology such as:
> * *"ACP client editors and developer tools"*
> * *"External agent runtimes and orchestrators"*
> * *"Language and agent server protocol daemons"*

---

## 7. Protocol for Adding a New Package

When adding a new package to the tap:
1. Create `Formula/<package-name>/<package-name>.rb`.
2. Add the package definition to `.github/packages.json`.
3. Add the package name to `.github/workflows/bump-formula.yml` input dropdown.
4. Verify local syntax: `ruby -c Formula/<package-name>/<package-name>.rb`.
5. Create `docs/formulae/<package-name>.md` (without hardcoding version numbers).
6. Add single package row to the index table in `README.md`.
7. Verify with `brew audit --strict Formula/<package-name>/<package-name>.rb`.
