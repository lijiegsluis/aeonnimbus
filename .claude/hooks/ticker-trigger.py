#!/usr/bin/env python3
"""UserPromptSubmit hook: a message that is only a ticker (e.g. "NVDA", "$iren", "BRK.B",
"deep dive MELI") routes to the equity-deep-dive skill."""
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)
prompt = (data.get("prompt") or "").strip()
m = re.fullmatch(
    r"(?:(?:deep[\s-]?dive|equity research|an[aá]lisis(?: de)?|analiza|research)\s+)?\$?([A-Za-z]{1,5}(?:[.\-][A-Za-z]{1,2})?)"
    r"(?:\s+(es|en|watching|entry=\d+(?:\.\d+)?))*",
    prompt, flags=re.I)
COMMON = {"OK", "SI", "SÍ", "NO", "YES", "HI", "HOLA", "GO", "DALE", "VALE", "THANKS", "GRACIAS", "HELP", "TEST", "STOP"}
if not m:
    sys.exit(0)
ticker = m.group(1).upper()
bare = prompt.lstrip("$").split()[0]
# A bare word must be written in capitals (or with $) to count as a ticker.
if prompt == bare and not (prompt.startswith("$") or bare.isupper()):
    sys.exit(0)
if ticker in COMMON:
    sys.exit(0)
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": (
            f"The user sent a ticker ({ticker}). Run the equity-deep-dive skill for {ticker} "
            f"(Skill tool, skill 'equity-deep-dive', args '{prompt}') end to end and deliver the PDF."
        ),
    }
}))
