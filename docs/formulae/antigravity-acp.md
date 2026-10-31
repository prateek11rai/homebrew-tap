<img src="../../assets/brew-logo.svg" align="right" width="72" alt="Homebrew Logo">

# `antigravity-acp`

Google Antigravity Agent Client Protocol (ACP) headless server daemon and local execution harness.

---

## Overview

* **Formula Directory:** [`Formula/antigravity-acp/`](../../Formula/antigravity-acp/)
* **Upstream Homepage:** [https://antigravity.google](https://antigravity.google)

This package distributes the standalone headless ACP server (`agy_acp_server.par`) and companion sandbox execution harness (`localharness_external`) used by agent-aware developer editors and external orchestrators communicating via Google's Agent Client Protocol.

---

## Release Streams

This package is provided in two installation forms:

1. **Latest Stable (`antigravity-acp`):**  
   Tracks the newest stable release published by Google. Binaries are symlinked into `/opt/homebrew/bin/` and automatically available in your `$PATH`.
2. **Pinned Version Streams (`antigravity-acp@<version>`):**  
   Pinned to specific major/minor release branches. Installed as `keg_only` in `/opt/homebrew/opt/antigravity-acp@<version>/` so they never collide with the default binary.

---

## Why This Formula Exists

1. **Decoupled Extension Runtime:** Google distributes the interactive terminal CLI (`antigravity-cli` / `agy`) and desktop IDE (`antigravity`) on Homebrew, but does not provide an official formula for the standalone headless ACP daemon.
2. **Standardized ACP Interface:** External editors and agent runtimes connect via ACP stdio/IPC and require two companion binaries in the same directory:
   * `agy_acp_server.par`
   * `localharness_external`
3. **Reproducible Local Management:** This formula allows Homebrew to manage binary downloads, checksum integrity validation, and symlinks in `/opt/homebrew/bin` without manual intervention or opaque in-app background downloaders.

---

## Upstream Release Architecture

Google distributes the ACP extension runtime as platform-specific archives directly from its release CDN:

| Platform | Architecture | Archive Pattern |
| :--- | :--- | :--- |
| macOS | Apple Silicon (`arm64`) | `https://dl.google.com/agy-extensions/releases/macos/agy-acp-server-{version}-darwin-arm64.zip` |
| macOS | Intel (`x86_64`) | `https://dl.google.com/agy-extensions/releases/macos/agy-acp-server-{version}-darwin-x86_64.zip` |

Exact versions and validated SHA-256 checksums are maintained directly in the formula source files. To inspect the current version:

```bash
brew info prateek11rai/antigravity-acp
```

---

## Installed Binaries

When installed, the formula provides the following binaries:

* **`agy_acp_server.par`**: Google's hermetic Python archive executable running the ACP server daemon.
* **`localharness_external`**: Companion local harness runtime mediating tool execution and host permissions.

---

## Installation & Usage

### Install Latest Stable

```bash
brew install prateek11rai/antigravity-acp
```

### Install a Specific Pinned Branch

```bash
brew install prateek11rai/antigravity-acp@<version>
```

### Verification

Confirm the binaries are installed and executable:

```bash
which agy_acp_server.par
which localharness_external
```

### ACP Client Integration

* **Standard Detection:** Most ACP-compatible editors search your system `$PATH` and will automatically discover `/opt/homebrew/bin/agy_acp_server.par`.
* **Custom Executable Path:** If an editor or client asks for an explicit executable path, or if you are using a pinned branch formula (`antigravity-acp@<version>`), provide the exact binary path:
  ```text
  /opt/homebrew/opt/antigravity-acp@<version>/bin/agy_acp_server.par
  ```

---

## Upstream References

* [Google Antigravity Documentation](https://antigravity.google)
* [Agent Client Protocol Specification (ACP)](https://github.com/google/agent-client-protocol)
