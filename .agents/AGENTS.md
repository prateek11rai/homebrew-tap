# AGENTS.md — Repository Operating Guide

System instructions and conventions for AI agents and maintainers working in this repository (`prateek11rai/homebrew-tap`).

---

## 1. Repository Purpose

This repository is a personal GitHub-hosted **Homebrew Tap** (`prateek11rai/tap`).  
Its primary purpose is to package, distribute, and maintain custom formulae, casks, and standalone binary releases that:
1. Lack official upstream packaging in `homebrew/core` or `homebrew/cask`.
2. Require direct binary downloads from vendor CDNs while preserving system integrity (checksum validation, automated PATH management, clean uninstalls).
3. Support local developer environments and workflows (such as T3 Code, agent runtimes, and developer tooling).

---

## 2. Directory Layout & Architecture

Agents must adhere strictly to Homebrew's canonical directory structure:

```text
homebrew-tap/
├── .agents/
│   └── AGENTS.md                    # Agent instructions and repository conventions (this file)
├── .github/
│   └── workflows/                   # Future GitHub Actions (CI / brew test-bot / linting)
├── Formula/                         # Command-line tools, headless daemons, and standalone binaries
│   └── <formula-name>.rb
├── Casks/                           # GUI macOS applications (.app bundles, DMGs, PKGs)
│   └── <cask-name>.rb               # (Reserved for future casks)
├── docs/                            # In-depth package documentation
│   ├── formulae/
│   │   └── <formula-name>.md        # Technical doc, upstream URLs, checksums, and client setup
│   └── casks/
│       └── <cask-name>.md           # (Reserved for future cask docs)
├── .gitignore                       # Standard Homebrew tap ignores
└── README.md                        # Lean public entrypoint: tap instructions, package list, dotfiles setup
```

### Rules on Directory Placement:
* **`Formula/`**: Put Ruby formula files (`.rb`) here. **Do not** put markdown or other asset files inside `Formula/`, as Homebrew's tap loader scans all files in this directory.
* **`Casks/`**: Put GUI app definitions (`.rb`) here.
* **`docs/formulae/` & `docs/casks/`**: All detailed package descriptions, upstream sources, checksum tables, and client integration guides go here.
* **`README.md`**: Must remain lean and generic. It lists packages in a high-level table and links to the relevant document under `docs/`.

---

## 3. Workflow: Adding a New Package

When tasked with adding a new package, agents must follow this sequential protocol:

### Step 1: Classification (Formula vs. Cask)
* Use a **Formula** (`Formula/<name>.rb`) for:
  - Command-line interfaces (CLIs).
  - Headless daemons or protocol servers (e.g. `antigravity-acp`).
  - Pre-compiled binaries requiring symlinks into `/opt/homebrew/bin`.
* Use a **Cask** (`Casks/<name>.rb`) for:
  - macOS `.app` bundles placed in `/Applications`.
  - Packages distributed as `.dmg`, `.pkg`, or `.zip` containing a GUI application.

### Step 2: Source Integrity & Multi-Architecture Support
* Always compute and verify official SHA256 checksums from the vendor's release artifacts. Never omit checksums.
* Support both Apple Silicon (`arm64`) and Intel (`x86_64`) whenever upstream binaries exist:
  ```ruby
  on_macos do
    on_arm do
      url "https://vendor.example/release-arm64.zip"
      sha256 "<checksum-arm64>"
    end
    on_intel do
      url "https://vendor.example/release-x86_64.zip"
      sha256 "<checksum-intel>"
    end
  end
  ```

### Step 3: Local Validation Commands
Before presenting or committing any formula changes, run:
1. **Ruby Syntax Validation:**
   ```bash
   ruby -c Formula/<name>.rb
   ```
2. **Formula Audit (Homebrew DSL compliance):**
   ```bash
   brew audit --strict Formula/<name>.rb
   ```
3. **Local Dry-Run Installation & Test:**
   ```bash
   brew install --build-from-source Formula/<name>.rb
   brew test Formula/<name>.rb
   ```

### Step 4: Documentation Protocol
Every new formula or cask **must** have:
1. A corresponding documentation file: `docs/formulae/<name>.md` or `docs/casks/<name>.md`.
2. An entry added to the package index table in `README.md`.

---

## 4. Git Commit & Versioning Conventions

Homebrew repository conventions dictate clean, predictable commit messages:

| Action | Commit Format | Example |
| :--- | :--- | :--- |
| **New Formula** | `<formula>: add formula` | `antigravity-acp: add formula` |
| **New Cask** | `<cask>: add cask` | `my-app: add cask` |
| **Version Bump** | `<formula> <new_version>` | `antigravity-acp 1.4.2` |
| **Fix/Update** | `<formula>: <summary of change>` | `antigravity-acp: update download URLs` |
| **Docs Update** | `docs: <summary>` | `docs: update T3 Code setup instructions` |

---

## 5. Future Extensions & Automation

* **GitHub Actions (`.github/workflows/tests.yml`):**  
  In the future, this repository can be wired to Homebrew's official CI runner (`Homebrew/actions/setup-homebrew` and `brew test-bot`) to automatically audit and test pull requests on both macOS ARM and Intel runners.
* **Dependabot / Version Bumpers:**  
  Periodic GitHub Actions can be added to poll vendor CDN endpoints or GitHub release feeds and submit automated version bump PRs.

---

## 6. Safety & Human Review

* **Never commit or push directly without explicit user consent.** Prepare changes as untracked files or working tree changes and present them for review.
* Ensure all external download URLs originate strictly from verified vendor domains.
