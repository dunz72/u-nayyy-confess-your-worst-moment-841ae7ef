#!/usr/bin/env python3
"""Confess Your Worst Moment — entry writer (stdlib only).

Copies the single-line confession from entry.txt (shipped beside this
script) to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt),
then validates the output the same way the sealed gate does: UTF-8,
1-200 characters, not only whitespace.
"""

import os
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.txt")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dest = os.path.join(out_dir, "entry.txt")

    with open(source, "rb") as f:
        raw = f.read()

    text = raw.decode("utf-8")  # raises UnicodeDecodeError if not UTF-8
    if not (1 <= len(text) <= 200):
        raise SystemExit(f"entry must be 1-200 characters, got {len(text)}")
    if not text.strip():
        raise SystemExit("entry must not be only whitespace")
    if "\n" in text.rstrip("\n") or "\r" in text:
        raise SystemExit("entry must be a single line")

    os.makedirs(out_dir, exist_ok=True)
    with open(dest, "wb") as f:
        f.write(raw)

    # Re-read what was written and confirm it is byte-identical.
    with open(dest, "rb") as f:
        written = f.read()
    if written != raw:
        raise SystemExit("output differs from entry.txt")
    print(f"wrote {dest} ({len(text)} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
