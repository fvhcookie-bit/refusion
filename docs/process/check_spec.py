#!/usr/bin/env python3
"""Automatic contamination check for the clean-room specification.

Usage:  python docs/process/check_spec.py [SPEC_DIR ...]

Scans each SPEC_DIR (default: docs/spec and docs/ru/spec) for things that must not
appear in a clean-room spec: memory/code addresses, decompiler labels, original internal
identifiers, references to reverse-engineering materials. If the dirty-room notes
(notes/) are present, identifiers from them are also searched for in the spec.

Exit code 0 = clean, 1 = findings. It catches the obvious only; the manual checklist
(process/review_checklist.md) is still required.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SPECS = [Path(a) for a in sys.argv[1:]] or [ROOT / "docs" / "spec", ROOT / "docs" / "ru" / "spec"]
NOTES = ROOT / "docs" / "notes"
ALLOWED_FILE = Path(__file__).resolve().parent / "allowed_names.txt"

# (pattern, reason)
PATTERNS = [
    (r"0x[0-9A-Fa-f]{5,}", "long hex number: looks like a memory/code address"),
    (r"\b(FUN|DAT|LAB|PTR|SUB|UNK)_[0-9A-Fa-f]{4,}", "decompiler label"),
    (r"\b\w+_Q\b", "hypothesis-name suffix _Q from the reverse-engineering notes"),
    (r"\bg_[A-Za-z]\w*", "global-variable name"),
    (r"\b\w+\.(cpp|h|c|java|py|ps1)\b", "source / tool file name"),
    (r"(?i)\b(ghidra|decomp\w*|disasm\w*|дизасм\w*|декомпил\w*|sstate|savestate\w*|telemetry|сейвстейт\w*|телеметр\w*)\b",
     "reference to reverse-engineering tooling"),
    (r"\bnotes/|\.\./notes", "link to the dirty-room materials"),
    (r"(?i)\b\w+\s*\+\s*0x[0-9A-Fa-f]{2,}", "in-memory structure offset"),
    (r"\$gp|\bjal\b|\bMIPS\b|\bR5900\b|\bCOP[12]\b|\bVU[01]\b", "machine-level detail"),
    (r"\b[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)*_[A-Z][A-Za-z0-9]+(?:_[A-Za-z0-9]+)*\b",
     "CamelCase_With_Underscore identifier (function-name style)"),
]

# Code-shaped identifiers harvested from the notes: mixedCase or CamelCase, optionally with _.
IDENT_IN_BACKTICKS = re.compile(r"`([^`\n]+)`")
CODE_SHAPED = re.compile(r"^(?:[a-z]+[A-Z]\w*|[A-Z][a-z0-9]+[A-Z]\w*|\w+_Q|g_\w+)$")


def load_allowed():
    allowed = set()
    if ALLOWED_FILE.exists():
        for line in ALLOWED_FILE.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                allowed.add(line)
    return allowed


def dirty_identifiers(allowed):
    names = set()
    if not NOTES.is_dir():
        return names
    for path in NOTES.rglob("*.md"):
        for chunk in IDENT_IN_BACKTICKS.findall(path.read_text(encoding="utf-8")):
            for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", chunk):
                if len(token) >= 5 and CODE_SHAPED.match(token) and token not in allowed:
                    names.add(token)
    return names


def is_allowed(match_text, allowed):
    return match_text in allowed or any(match_text.startswith(a) for a in allowed if a.endswith("_"))


def main():
    missing = [d for d in SPECS if not d.is_dir()]
    if missing:
        print(f"spec directory not found: {missing[0]}")
        return 2
    allowed = load_allowed()
    dirty = dirty_identifiers(allowed)
    dirty_re = re.compile(r"\b(" + "|".join(map(re.escape, sorted(dirty, key=len, reverse=True))) + r")\b") if dirty else None
    compiled = [(re.compile(p), why) for p, why in PATTERNS]

    findings = 0
    for path in sorted(p for d in SPECS for p in d.rglob("*.md")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for rx, why in compiled:
                for m in rx.finditer(line):
                    if is_allowed(m.group(0), allowed):
                        continue
                    findings += 1
                    print(f"{path.relative_to(ROOT)}:{lineno}: {why}: {m.group(0)!r}")
            if dirty_re:
                for m in dirty_re.finditer(line):
                    findings += 1
                    print(f"{path.relative_to(ROOT)}:{lineno}: identifier from the notes: {m.group(0)!r}")

    note = "" if NOTES.is_dir() else " (notes/ not found: identifier cross-check skipped)"
    if findings:
        print(f"\n{findings} finding(s){note}. Fix them or, if a name really comes from game data or the screen,"
              f" add it to {ALLOWED_FILE.name} with a comment saying where it comes from.")
        return 1
    print(f"spec is clean{note}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
