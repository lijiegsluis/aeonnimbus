#!/usr/bin/env python3
"""Checks a deep-dive research note (markdown) or page source (html) against the master prompt.

  python3 lint_note.py research/FN/2026-10-02/FN_Fabrinet_Deep_Dive_2026-10-02.md [more files]

Fails (exit 1) on banned phrases or a missing mandatory element; warns on weak sourcing.
"""
import re
import sys

BANNED = [
    "compelling", "robust", "positioned to", "leverages", "leveraging", "unlock", "demonstrates", "underscores",
    "seamlessly", "it is worth noting", "going forward", "transformative", "innovative", "cutting-edge",
    "game-changer", "game changer", "paradigm", "synergy", "synergies", "value-add", "noteworthy",
    "it is important to note", "delve", "poised to", "significant potential", "in conclusion",
    "furthermore", "additionally", "moreover",
]
SOFT = ["landscape", "trajectory", "momentum"]  # allowed only with a concrete meaning
REQUIRED_MD = {
    "standfirst / verdict (Entry, Target, Stop, Size)": r"Entry.*\n?.*Target|Target.*Stop",
    "scenario table (Bear/Base/Bull)": r"Bear.*Base.*Bull|### Bear",
    "probability-weighted value": r"[Pp]robability-weighted",
    "cost of capital": r"(WACC|[Cc]ost of capital)",
    "sensitivity grid": r"[Ss]ensitivity",
    "weighted valuation blend": r"[Bb]lend",
    "reverse DCF": r"[Rr]everse DCF",
    "variant views": r"[Vv]ariant view",
    "payoff / Kelly": r"Kelly",
    "risks": r"## Risks",
    "catalysts": r"## Catalysts",
    "position statement": r"We took a position in|We are watching",
    "track-record line": r"including the losses",
    "references": r"## (Sources|References)",
    "disclaimer": r"[Nn]ot investment advice",
}


def lint(path):
    text = open(path, encoding="utf-8").read()
    body = re.sub(r"<[^>]+>", " ", text) if path.endswith(".html") else text
    low = body.lower()
    errors, warns = [], []
    for p in BANNED:
        for m in re.finditer(r"\b" + re.escape(p) + r"\b", low):
            line = low.count("\n", 0, m.start()) + 1
            errors.append(f"banned phrase '{p}' (line {line})")
    for p in SOFT:
        n = len(re.findall(r"\b" + p + r"\b", low))
        if n:
            warns.append(f"'{p}' used {n}x: keep only where it has a concrete meaning")
    if path.endswith(".md"):
        for name, rx in REQUIRED_MD.items():
            if not re.search(rx, body):
                errors.append(f"missing: {name}")
        refs = re.findall(r"^\s*\d+\.\s", body.split("## Sources")[-1] if "## Sources" in body else "", re.M)
        if len(refs) < 10:
            warns.append(f"only {len(refs)} numbered references (master prompt asks for 10+)")
        if "We believe" not in body and "We note" not in body:
            warns.append("no 'We believe / We note' voice found")
    return errors, warns


def main():
    bad = False
    for path in sys.argv[1:]:
        e, w = lint(path)
        print(f"== {path}: {len(e)} errors, {len(w)} warnings")
        for x in e:
            print("  ERROR", x)
        for x in w:
            print("  warn ", x)
        bad |= bool(e)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
