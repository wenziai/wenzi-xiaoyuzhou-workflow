#!/usr/bin/env python3
"""Build a deterministic readable draft from a timestamped verification transcript."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from opencc import OpenCC


LINE = re.compile(r"^\[\s*([0-9.]+)s\s*->\s*[0-9.]+s\]\s*(.*)$")


def load_json(path: str | None, default):
    if not path:
        return default
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a simplified, untimestamped readable transcript draft")
    parser.add_argument("input", help="Timestamped verification Markdown")
    parser.add_argument("output", help="Readable Markdown destination")
    parser.add_argument("--title", required=True)
    parser.add_argument("--podcast", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--host")
    parser.add_argument("--chapters", help='JSON file: [{"start": 0, "title": "..."}]')
    parser.add_argument("--replacements", help="JSON object of deterministic replacements")
    parser.add_argument("--paragraph-chars", type=int, default=220)
    args = parser.parse_args()

    chapters = sorted(load_json(args.chapters, []), key=lambda item: float(item["start"]))
    replacements = load_json(args.replacements, {})
    source_text = Path(args.input).read_text(encoding="utf-8")
    segments = []
    for line in source_text.splitlines():
        match = LINE.match(line)
        if match and match.group(2).strip():
            segments.append((float(match.group(1)), match.group(2).strip()))
    if not segments:
        raise SystemExit("No timestamped segments found")

    header = [f"# {args.title}", "", f"- 播客：{args.podcast}"]
    if args.host:
        header.append(f"- 主播：{args.host}")
    header.extend([f"- 来源：{args.source}", ""])
    output = header
    chapter_index = 0
    paragraph: list[str] = []
    paragraph_chars = 0
    sentence_segments = 0

    def flush() -> None:
        nonlocal paragraph, paragraph_chars, sentence_segments
        if not paragraph:
            return
        text = "".join(paragraph).rstrip("，")
        if text and text[-1] not in "。？！…”’：；":
            text += "。"
        output.extend([text, ""])
        paragraph = []
        paragraph_chars = 0
        sentence_segments = 0

    for start, raw in segments:
        while chapter_index < len(chapters) and start >= float(chapters[chapter_index]["start"]):
            flush()
            output.extend([f"## {chapters[chapter_index]['title']}", ""])
            chapter_index += 1
        text = raw.replace(",", "，").replace("?", "？").replace("!", "！")
        for old, new in replacements.items():
            text = text.replace(old, new)
        text = re.sub(r"\s+", " ", text).strip()
        sentence_segments += 1
        if text[-1] in "。？！…”’：；":
            paragraph.append(text)
            sentence_segments = 0
        elif sentence_segments >= 4:
            paragraph.append(text + "。")
            sentence_segments = 0
        else:
            paragraph.append(text + "，")
        paragraph_chars += len(text)
        if paragraph_chars >= args.paragraph_chars:
            flush()
    flush()

    destination = Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(OpenCC("t2s").convert("\n".join(output).rstrip() + "\n"), encoding="utf-8")
    print(destination.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
