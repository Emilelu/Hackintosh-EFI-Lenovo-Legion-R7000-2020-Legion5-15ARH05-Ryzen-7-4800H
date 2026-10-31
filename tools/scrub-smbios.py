#!/usr/bin/env python3
"""Scrub SMBIOS identity from staged EFI plists and block the burned identity.

Installed as a pre-commit hook via `git config core.hooksPath .githooks`
(see .githooks/pre-commit). Behavior on every commit:

1. Any staged *.plist under EFI/ has its PlatformInfo>Generic identity fields
   (SystemSerialNumber, MLB, SystemUUID, ROM) blanked to the repository's
   placeholder convention (<string></string> / empty <data>). Formatting and
   every other byte of the file are preserved; already-empty fields are left
   untouched, so the scrub is idempotent. Scrubbed files are re-staged.
2. Every staged file is scanned for the burned identity (the set that leaked
   into the public history before the 2026-10-31 rewrite). If any of it shows
   up anywhere - including inside plists where the field scrub already ran -
   the commit is rejected; remove it and generate a fresh identity instead.

Bypass (only if you really know better): git commit --no-verify.
"""
import os
import re
import subprocess
import sys

# Identity that was published in public git history before the 2026-10-31
# filter-repo rewrite. It must never be committed again.
BURNED = (
    "C02FHKZ8ML7H",                      # old system serial number
    "C021139024NP8PGA8",                 # old MLB
    "07083417-A5B9-443F-B65C-FB0B3E3FC82B",  # old system UUID
    "3VwKFnue",                          # old ROM (base64)
)

IDENTITY_STRING_FIELDS = ("SystemSerialNumber", "MLB", "SystemUUID")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True)


def scrub_plist(text: str) -> tuple[str, list[str]]:
    """Blank the four identity fields; return (new_text, list of scrubbed fields)."""
    changed = []
    for field in IDENTITY_STRING_FIELDS:
        pattern = r"(<key>" + field + r"</key>\s*<string>)[^<]*(</string>)"
        new_text, n = re.subn(pattern, r"\g<1>\g<2>", text)
        if n and new_text != text:
            changed.append(field)
        text = new_text
    # ROM is stored as base64 <data>; empty it to the HEAD convention
    # (<data>\n\t+...</data> keeps the whitespace shape of the closing tag).
    m = re.search(r"(<key>ROM</key>\s*<data>)(.*?)(\s*</data>)", text, re.S)
    if m and m.group(2).strip():
        text = text[:m.start()] + m.group(1) + m.group(3) + text[m.end():]
        changed.append("ROM")
    return text, changed


def main() -> int:
    top = git("rev-parse", "--show-toplevel").strip()
    staged = [s for s in git("diff", "--cached", "--name-only", "-z").split("\0") if s]

    # 1) scrub identity fields in staged EFI plists
    scrubbed = []
    for rel in staged:
        if not (rel.startswith("EFI/") and rel.endswith(".plist")):
            continue
        path = os.path.join(top, rel.replace("/", os.sep))
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8", newline="") as fh:
            text = fh.read()
        new_text, changed = scrub_plist(text)
        if changed:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(new_text)
            subprocess.check_call(["git", "add", "--", rel])
            scrubbed.append(f"{rel}: {', '.join(changed)}")

    # 2) burned identity must not enter the repository by any door
    #    (except this detector itself, which must carry the literals to match)
    blocked = []
    for rel in staged:
        if rel.replace(os.sep, "/") == "tools/scrub-smbios.py":
            continue
        path = os.path.join(top, rel.replace("/", os.sep))
        if not os.path.isfile(path):
            continue
        with open(path, "rb") as fh:
            blob = fh.read()
        for secret in BURNED:
            if secret.encode() in blob:
                blocked.append((rel, secret))

    if blocked:
        print("COMMIT BLOCKED - the burned (publicly leaked) SMBIOS identity is in the staged content:")
        for rel, secret in blocked:
            print(f"  {rel}: contains {secret}")
        print("Remove it (or generate a fresh identity); never re-commit the leaked values.")
        return 1

    if scrubbed:
        print("pre-commit SMBIOS scrub:")
        for line in scrubbed:
            print(f"  {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
