#!/usr/bin/env python3
"""Convert a UTF-8 transcript from Traditional Chinese to Simplified Chinese."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import tempfile

from opencc import OpenCC


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert a UTF-8 transcript to Simplified Chinese")
    parser.add_argument("input", help="Source Markdown or text file")
    parser.add_argument("output", nargs="?", help="Destination; omit only with --in-place")
    parser.add_argument("--in-place", action="store_true", help="Atomically replace the input file")
    args = parser.parse_args()

    source = Path(args.input).expanduser().resolve()
    if not source.is_file():
        parser.error("input must be an existing file")
    if args.in_place == bool(args.output):
        parser.error("choose exactly one: output path or --in-place")

    destination = source if args.in_place else Path(args.output).expanduser().resolve()
    text = source.read_text(encoding="utf-8")
    converted = OpenCC("t2s").convert(text)

    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=".simplified-", suffix=destination.suffix, dir=destination.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(converted)
        os.replace(temporary_name, destination)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise

    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
