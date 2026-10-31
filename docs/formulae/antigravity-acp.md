# `antigravity-acp`

Google Antigravity Agent Client Protocol (ACP) headless server daemon and local execution harness.

---

## Overview

* **Formula file:** [`Formula/antigravity-acp.rb`](../../Formula/antigravity-acp.rb)
* **Upstream Homepage:** [https://antigravity.google](https://antigravity.google)
* **Latest Version:** `1.4.1`

This package distributes the standalone headless ACP server (`agy_acp_server.par`) and companion sandbox execution harness (`localharness_external`) used by agent-aware developer editors such as **T3 Code**, **Zed**, and **VS Code**.

---

## Why This Formula Exists

1. **Missing Upstream Formula:** Google distributes the interactive terminal CLI (`antigravity-cli` / `agy`) and GUI app (`antigravity`) on Homebrew, but does not provide an official formula for the standalone ACP protocol daemon.
2. **T3 Code Integration:** T3 Code communicates strictly over the Agent Client Protocol. It scans `$PATH` for two binaries located in the same directory:
   * `agy_acp_server.par`
   * `localharness_external`
3. **Controlled Local Installation:** This formula allows Homebrew to manage binary downloading, checksum integrity verification, and symlinking into `/opt/homebrew/bin` without relying on ad-hoc manual scripts or opaque in-app background downloaders.

---

## Upstream Release Sources

Google distributes the ACP extension runtime directly from its release CDN:

| Platform | Architecture | Archive URL | SHA256 Checksum |
| :--- | :--- | :--- | :--- |
| macOS | Apple Silicon (`arm64`) | `https://dl.google.com/agy-extensions/releases/macos/agy-acp-server-1.4.1-darwin-arm64.zip` | `f9bdd68291ae78c38d2141e63bc86b84e6cc7b9f60f71652c68435a7943deb17` |
| macOS | Intel (`x86_64`) | `https://dl.google.com/agy-extensions/releases/macos/agy-acp-server-1.4.1-darwin-x86_64.zip` | `27e31f096874704f14167b07ef9e84cc77134615ee41d024f7b1c957add85307` |

---

## Installed Binaries

When installed, the formula links the following binaries into your Homebrew `bin` path (`/opt/homebrew/bin`):

* **`agy_acp_server.par`**: Google's hermetic Python archive executable running the ACP server daemon.
* **`localharness_external`**: Companion local harness runtime mediating process permissions and tool execution.

---

## Installation & Verification

### Install

```bash
brew install prateek11rai/antigravity-acp
```

### Verify

Confirm both binaries are executable and resolvable in `$PATH`:

```bash
which agy_acp_server.par
which localharness_external
```

### T3 Code Setup

1. Open **T3 Code**.
2. Navigate to **Settings > Providers > Antigravity-Atlan**.
3. T3 Code will automatically detect `agy_acp_server.par` from `$PATH` and mark the provider status as active.
4. If running a custom path, specify `/opt/homebrew/bin/agy_acp_server.par` in the **Binary path** field.

---

## Upstream References

* [Google Antigravity Documentation](https://antigravity.google)
* [Agent Client Protocol Specification (ACP)](https://github.com/google/agent-client-protocol)
* [T3 Code](https://t3.chat)
