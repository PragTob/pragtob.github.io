#!/usr/bin/env python3
"""Convert legacy WordPress [code] blocks to fenced Markdown code blocks."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


POSTS_DIR = Path("/workspaces/pragtob.github.io/_posts")

CODE_BLOCK_RE = re.compile(
    r"\[code(?P<attrs>[^\]]*)\](?P<body>.*?)\[/code\]", re.IGNORECASE | re.DOTALL
)

LANGUAGE_ATTR_RE = re.compile(
    r"""(?:lang|language)\s*=\s*["']?(?P<lang>[A-Za-z0-9_#+.-]+)""", re.IGNORECASE
)

GIST_SOURCE_LINE_RE = re.compile(r"Source:\s+\[https?://gist\.github\.com/")


@dataclass
class FencedBlock:
    start: int
    end: int
    code: str
    has_nearby_gist_source: bool


def normalize_language(attrs: str) -> str:
    match = LANGUAGE_ATTR_RE.search(attrs or "")
    if not match:
        return ""

    lang = match.group("lang").strip().lower()
    aliases = {
        "shell": "bash",
        "sh": "bash",
    }
    return aliases.get(lang, lang)


def normalize_code_for_compare(code: str) -> str:
    normalized_lines = [line.rstrip() for line in code.replace("\r\n", "\n").split("\n")]
    return "\n".join(normalized_lines).strip()


def fence_for_content(content: str) -> str:
    backtick_runs = re.findall(r"`+", content)
    longest = max((len(run) for run in backtick_runs), default=0)
    return "`" * max(3, longest + 1)


def convert_code_tags(content: str) -> tuple[str, int]:
    replacements = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal replacements
        replacements += 1

        attrs = match.group("attrs") or ""
        body = match.group("body") or ""
        language = normalize_language(attrs)
        code = body.strip("\n")
        fence = fence_for_content(code)

        return f"\n\n{fence}{language}\n{code}\n{fence}\n\n"

    return CODE_BLOCK_RE.sub(repl, content), replacements


def parse_fenced_blocks(text: str) -> list[FencedBlock]:
    blocks: list[FencedBlock] = []
    lines = text.splitlines(keepends=True)
    offsets = []
    current = 0
    for line in lines:
        offsets.append(current)
        current += len(line)

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip("\n")
        fence_match = re.match(r"^(`{3,})([^`]*)$", stripped)
        if not fence_match:
            i += 1
            continue

        opening = fence_match.group(1)
        start_line = i
        j = i + 1
        while j < len(lines):
            if lines[j].rstrip("\n") == opening:
                break
            j += 1
        if j >= len(lines):
            i += 1
            continue

        code = "".join(lines[i + 1 : j])
        start = offsets[start_line]
        end = offsets[j] + len(lines[j])

        context_start = max(0, start - 600)
        context = text[context_start:start]
        has_source = bool(GIST_SOURCE_LINE_RE.search(context))

        blocks.append(
            FencedBlock(
                start=start,
                end=end,
                code=normalize_code_for_compare(code),
                has_nearby_gist_source=has_source,
            )
        )
        i = j + 1

    return blocks


def is_small_intervening(text_between: str) -> bool:
    if len(text_between) > 500:
        return False
    cleaned = text_between.strip()
    if not cleaned:
        return True

    allowed_parts = []
    for line in cleaned.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("Source: [https://gist.github.com/"):
            allowed_parts.append(stripped)
            continue
        if stripped.startswith("**File: `") and stripped.endswith("`**"):
            allowed_parts.append(stripped)
            continue
        return False
    return True


def dedupe_nearby_identical_blocks(text: str) -> tuple[str, int]:
    blocks = parse_fenced_blocks(text)
    if len(blocks) < 2:
        return text, 0

    remove_ranges: list[tuple[int, int]] = []
    for first, second in zip(blocks, blocks[1:]):
        if not first.code or not second.code:
            continue
        if first.code != second.code:
            continue
        between = text[first.end : second.start]
        if not is_small_intervening(between):
            continue

        # Prefer gist-linked block when only one has a nearby source line.
        if first.has_nearby_gist_source and not second.has_nearby_gist_source:
            remove_ranges.append((second.start, second.end))
        elif second.has_nearby_gist_source and not first.has_nearby_gist_source:
            remove_ranges.append((first.start, first.end))
        else:
            remove_ranges.append((second.start, second.end))

    if not remove_ranges:
        return text, 0

    # Merge overlapping ranges.
    remove_ranges.sort()
    merged = [list(remove_ranges[0])]
    for start, end in remove_ranges[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    out = []
    cursor = 0
    for start, end in merged:
        out.append(text[cursor:start])
        cursor = end
    out.append(text[cursor:])

    return "".join(out), len(merged)


def process_file(path: Path, write: bool) -> tuple[int, int]:
    original = path.read_text(encoding="utf-8")
    converted, replacements = convert_code_tags(original)
    deduped, dedupes = dedupe_nearby_identical_blocks(converted)

    if write and deduped != original:
        path.write_text(deduped, encoding="utf-8")

    return replacements, dedupes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write changes to files")
    args = parser.parse_args()

    total_replacements = 0
    total_dedupes = 0
    changed_files = 0

    for post in sorted(POSTS_DIR.glob("*.md")):
        replacements, dedupes = process_file(post, args.write)
        if replacements or dedupes:
            changed_files += 1
            total_replacements += replacements
            total_dedupes += dedupes
            print(f"{post.name}: converted {replacements}, deduped {dedupes}")

    print(f"Changed files: {changed_files}")
    print(f"Converted [code] blocks: {total_replacements}")
    print(f"Removed near duplicates: {total_dedupes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
