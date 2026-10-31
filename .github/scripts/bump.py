#!/usr/bin/env python3
"""
Generic Homebrew Formula Version Bumper

Supports:
1. Explicit manual bump:
   bump.py --package <name> --version <version> [--formula-path <path>]
2. Automated multi-package discovery (for cron runs):
   bump.py --auto
   - Checks every package defined in packages.json
   - Probes vendor CDN via HTTP HEAD for patch/minor/major increments
   - Skips packages with no updates and continues to the rest
   - Handles multi-platform artifacts (macOS and Linux, ARM64 and x86_64)
"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PACKAGES_FILE = REPO_ROOT / ".github" / "packages.json"


def check_url_exists(url: str) -> bool:
    """Perform HTTP HEAD request to check if artifact exists at URL."""
    req = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "Homebrew-Tap-Bumper/1.0 (prateek11rai/homebrew-tap)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False


def calculate_sha256(url: str) -> str:
    """Download artifact from URL and return its hex SHA-256 checksum."""
    print(f"--> Downloading artifact: {url}")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Homebrew-Tap-Bumper/1.0 (prateek11rai/homebrew-tap)"},
    )
    hasher = hashlib.sha256()
    with urllib.request.urlopen(req) as response:
        while chunk := response.read(65536):
            hasher.update(chunk)
    digest = hasher.hexdigest()
    print(f"    SHA-256: {digest}")
    return digest


def update_formula(
    formula_path: Path,
    new_version: str,
    darwin_arm_url: str,
    darwin_arm_sha: str,
    darwin_intel_url: str,
    darwin_intel_sha: str,
    linux_arm_url: str = "",
    linux_arm_sha: str = "",
    linux_intel_url: str = "",
    linux_intel_sha: str = "",
) -> bool:
    """Update version, URLs, and checksums in a formula Ruby file."""
    content = formula_path.read_text(encoding="utf-8")
    original = content

    content = re.sub(
        r'version\s+"[^"]+"',
        f'version "{new_version}"',
        content,
        count=1,
    )

    # Replace on_macos block
    macos_block = f"""  on_macos do
    on_arm do
      url "{darwin_arm_url}"
      sha256 "{darwin_arm_sha}"
    end
    on_intel do
      url "{darwin_intel_url}"
      sha256 "{darwin_intel_sha}"
    end
  end"""
    content = re.sub(r"  on_macos do\n.*?\n  end", macos_block, content, flags=re.DOTALL)

    # Replace on_linux block if provided
    if linux_arm_url and linux_intel_url:
        linux_block = f"""  on_linux do
    on_arm do
      url "{linux_arm_url}"
      sha256 "{linux_arm_sha}"
    end
    on_intel do
      url "{linux_intel_url}"
      sha256 "{linux_intel_sha}"
    end
  end"""
        content = re.sub(r"  on_linux do\n.*?\n  end", linux_block, content, flags=re.DOTALL)

    if content != original:
        formula_path.write_text(content, encoding="utf-8")
        print(f"✓ Updated formula: {formula_path.relative_to(REPO_ROOT)}")
        return True
    return False


def create_versioned_formula(
    base_formula: Path,
    pkg_name: str,
    minor_tag: str,
    new_version: str,
    darwin_arm_url: str,
    darwin_arm_sha: str,
    darwin_intel_url: str,
    darwin_intel_sha: str,
    linux_arm_url: str = "",
    linux_arm_sha: str = "",
    linux_intel_url: str = "",
    linux_intel_sha: str = "",
) -> Path:
    """Create a new versioned formula file (e.g. antigravity-acp@1.5.rb) with keg_only."""
    versioned_file = base_formula.parent / f"{pkg_name}@{minor_tag}.rb"
    class_suffix = minor_tag.replace(".", "")
    pascal_name = "".join(part.capitalize() for part in pkg_name.split("-"))
    class_name = f"{pascal_name}AT{class_suffix}"

    linux_section = ""
    if linux_arm_url and linux_intel_url:
        linux_section = f"""
  on_linux do
    on_arm do
      url "{linux_arm_url}"
      sha256 "{linux_arm_sha}"
    end
    on_intel do
      url "{linux_intel_url}"
      sha256 "{linux_intel_sha}"
    end
  end"""

    code = f"""class {class_name} < Formula
  desc "{pkg_name} ({minor_tag} branch)"
  homepage "https://antigravity.google"
  version "{new_version}"

  keg_only :versioned_formula

  on_macos do
    on_arm do
      url "{darwin_arm_url}"
      sha256 "{darwin_arm_sha}"
    end
    on_intel do
      url "{darwin_intel_url}"
      sha256 "{darwin_intel_sha}"
    end
  end{linux_section}

  def install
    bin.install "agy_acp_server.par"
    bin.install "localharness_external"
  end

  test do
    assert_predicate bin/"agy_acp_server.par", :exist?
    assert_predicate bin/"localharness_external", :exist?
  end
end
"""
    versioned_file.write_text(code, encoding="utf-8")
    print(f"✓ Created new versioned formula: {versioned_file.relative_to(REPO_ROOT)}")
    return versioned_file


def extract_minor(version_str: str) -> str:
    """Extract major.minor from version string (e.g. '1.4.2' -> '1.4')."""
    match = re.match(r"^(\d+\.\d+)", version_str)
    return match.group(1) if match else ""


def probe_latest_version(pkg_meta: dict) -> str | None:
    """Probe CDN for version increments (patch, minor, major)."""
    current = pkg_meta.get("current_version", "")
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)$", current)
    if not m:
        return None

    major, minor, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))
    probe_template = pkg_meta.get("version_check", {}).get("url_template", "")
    if not probe_template:
        probe_template = pkg_meta.get("artifacts", {}).get("darwin_arm64", {}).get("url_template", "")

    if not probe_template:
        return None

    latest_found = None

    # 1. Probe patch increments (e.g. 1.4.2, 1.4.3...)
    p = patch + 1
    while p <= patch + 10:
        candidate = f"{major}.{minor}.{p}"
        url = probe_template.replace("{version}", candidate)
        if check_url_exists(url):
            latest_found = candidate
            p += 1
        else:
            break

    # 2. Probe minor increments (e.g. 1.5.0, 1.6.0...)
    mi = minor + 1
    while mi <= minor + 5:
        candidate = f"{major}.{mi}.0"
        url = probe_template.replace("{version}", candidate)
        if check_url_exists(url):
            latest_found = candidate
            mi += 1
        else:
            break

    # 3. Probe major increment (e.g. 2.0.0)
    candidate_major = f"{major + 1}.0.0"
    url_major = probe_template.replace("{version}", candidate_major)
    if check_url_exists(url_major):
        latest_found = candidate_major

    return latest_found


def bump_package(pkg_meta: dict, new_version: str, formula_path_override: str = "") -> bool:
    """Execute bump for a specific package metadata object."""
    pkg_name = pkg_meta["name"]
    is_main_formula = not bool(formula_path_override)
    target_formula = (
        REPO_ROOT / formula_path_override if formula_path_override else REPO_ROOT / pkg_meta["formula_path"]
    )

    if not target_formula.is_file():
        print(f"Error: Formula file {target_formula} not found.")
        return False

    artifacts = pkg_meta.get("artifacts", {})
    darwin_arm_tmpl = artifacts.get("darwin_arm64", {}).get("url_template", "")
    darwin_intel_tmpl = artifacts.get("darwin_x86_64", {}).get("url_template", "")
    linux_arm_tmpl = artifacts.get("linux_arm64", {}).get("url_template", "")
    linux_intel_tmpl = artifacts.get("linux_x86_64", {}).get("url_template", "")

    darwin_arm_url = darwin_arm_tmpl.replace("{version}", new_version)
    darwin_intel_url = darwin_intel_tmpl.replace("{version}", new_version)
    linux_arm_url = linux_arm_tmpl.replace("{version}", new_version) if linux_arm_tmpl else ""
    linux_intel_url = linux_intel_tmpl.replace("{version}", new_version) if linux_intel_tmpl else ""

    print(f"\n==========================================")
    print(f"Bumping '{pkg_name}' to version {new_version}...")
    print(f"==========================================")
    try:
        darwin_arm_sha = calculate_sha256(darwin_arm_url)
        darwin_intel_sha = calculate_sha256(darwin_intel_url)
        linux_arm_sha = calculate_sha256(linux_arm_url) if linux_arm_url else ""
        linux_intel_sha = calculate_sha256(linux_intel_url) if linux_intel_url else ""
    except Exception as e:
        print(f"Error calculating artifact checksums for {pkg_name}: {e}")
        return False

    updated = update_formula(
        target_formula,
        new_version,
        darwin_arm_url,
        darwin_arm_sha,
        darwin_intel_url,
        darwin_intel_sha,
        linux_arm_url,
        linux_arm_sha,
        linux_intel_url,
        linux_intel_sha,
    )

    target_minor = extract_minor(new_version)
    if is_main_formula and target_minor:
        minor_formula = target_formula.parent / f"{pkg_name}@{target_minor}.rb"
        if minor_formula.is_file():
            update_formula(
                minor_formula,
                new_version,
                darwin_arm_url,
                darwin_arm_sha,
                darwin_intel_url,
                darwin_intel_sha,
                linux_arm_url,
                linux_arm_sha,
                linux_intel_url,
                linux_intel_sha,
            )
        else:
            create_versioned_formula(
                target_formula,
                pkg_name,
                target_minor,
                new_version,
                darwin_arm_url,
                darwin_arm_sha,
                darwin_intel_url,
                darwin_intel_sha,
                linux_arm_url,
                linux_arm_sha,
                linux_intel_url,
                linux_intel_sha,
            )

    if updated and is_main_formula:
        pkg_meta["current_version"] = new_version

    return updated


def main():
    parser = argparse.ArgumentParser(description="Homebrew Tap Version Bumper")
    parser.add_argument("--auto", action="store_true", help="Auto-probe CDN and bump all packages with updates")
    parser.add_argument("--package", help="Package name defined in packages.json")
    parser.add_argument("--version", help="Explicit target version string (e.g. 1.4.2)")
    parser.add_argument("--formula-path", default="", help="Optional custom formula path")
    args = parser.parse_args()

    if not PACKAGES_FILE.is_file():
        sys.exit(f"Error: {PACKAGES_FILE} not found.")

    with open(PACKAGES_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)

    packages = registry.get("packages", [])

    any_updated = False

    if args.auto or (not args.package and not args.version):
        print("==> Running automated discovery across all registered packages...")
        for pkg in packages:
            name = pkg["name"]
            curr = pkg.get("current_version", "")
            print(f"\nChecking '{name}' (current version: {curr})...")
            new_ver = probe_latest_version(pkg)
            if new_ver and new_ver != curr:
                print(f"[+] Update available for {name}: {curr} -> {new_ver}")
                if bump_package(pkg, new_ver):
                    any_updated = True
            else:
                print(f"[-] No new version found for {name}. Up to date.")

        if any_updated:
            with open(PACKAGES_FILE, "w", encoding="utf-8") as f:
                json.dump(registry, f, indent=2)
                f.write("\n")
            print("\n✓ Synchronized packages.json with new versions")

    else:
        pkg = next((p for p in packages if p["name"] == args.package), None)
        if not pkg:
            sys.exit(f"Error: Package '{args.package}' not found in packages.json")

        target_ver = args.version or probe_latest_version(pkg)
        if not target_ver:
            print(f"[-] No new version detected for {args.package}.")
            sys.exit(0)

        if bump_package(pkg, target_ver, args.formula_path):
            any_updated = True
            with open(PACKAGES_FILE, "w", encoding="utf-8") as f:
                json.dump(registry, f, indent=2)
                f.write("\n")
            print("✓ Synchronized packages.json")

    output_file = os.getenv("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"updated={'true' if any_updated else 'false'}\n")


if __name__ == "__main__":
    main()
