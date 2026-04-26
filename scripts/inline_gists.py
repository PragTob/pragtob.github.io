#!/usr/bin/env python3
"""Replace gist URLs in _posts with inline fenced code blocks."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory


POSTS_DIR = Path("/workspaces/pragtob.github.io/_posts")
API_BASE = "https://api.github.com/gists/"

# Markdown link to gist, capturing URL in group "url"
MARKDOWN_GIST_LINK = re.compile(r"\[[^\]]+\]\((https?://gist\.github\.com/[^\s)]+)\)")
# Bare gist URL. Negative lookbehind avoids matching the URL part of markdown links.
BARE_GIST_LINK = re.compile(r"(?<!\]\()https?://gist\.github\.com/[^\s)]+")
ANY_GIST_REFERENCE = re.compile(
    r"\[[^\]]+\]\((?P<mdurl>https?://gist\.github\.com/[^\s)]+)\)|(?P<url>(?<!\]\()https?://gist\.github\.com/[^\s)]+)"
)


LANGUAGE_MAP = {
    "elixir": "elixir",
    "erlang": "erlang",
    "ruby": "ruby",
    "python": "python",
    "shell": "bash",
    "bash": "bash",
    "zsh": "bash",
    "javascript": "javascript",
    "typescript": "typescript",
    "json": "json",
    "yaml": "yaml",
    "markdown": "markdown",
    "text": "",
}

EXTENSION_LANGUAGE_MAP = {
    ".rb": "ruby",
    ".ex": "elixir",
    ".exs": "elixir",
    ".erl": "erlang",
    ".py": "python",
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",
    ".js": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "typescript",
    ".json": "json",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".md": "markdown",
    ".txt": "",
}


@dataclass
class GistFile:
    filename: str
    language: str
    content: str


@dataclass
class GistData:
    gist_id: str
    html_url: str
    files: list[GistFile]


def normalize_gist_url(url: str) -> tuple[str, str]:
    url = url.rstrip(".,;")
    no_fragment = url.split("#", 1)[0]
    no_query = no_fragment.split("?", 1)[0]

    path = no_query.split("gist.github.com/", 1)[1].strip("/")
    parts = [part for part in path.split("/") if part]
    if not parts:
        raise ValueError(f"Could not parse gist URL: {url}")

    if len(parts) == 1:
        gist_id = parts[0]
    else:
        gist_id = parts[1]

    canonical_url = f"https://gist.github.com/{'/'.join(parts)}"
    return gist_id, canonical_url


def fetch_gist(gist_id: str) -> GistData:
    request = urllib.request.Request(
        f"{API_BASE}{gist_id}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "inline-gists-migrator",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} when fetching gist {gist_id}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error when fetching gist {gist_id}: {exc}") from exc

    files = []
    for file_data in payload.get("files", {}).values():
        files.append(
            GistFile(
                filename=file_data.get("filename", "unknown"),
                language=(file_data.get("language") or "").strip(),
                content=file_data.get("content") or "",
            )
        )

    files.sort(key=lambda file: file.filename.lower())

    return GistData(
        gist_id=gist_id,
        html_url=payload.get("html_url", f"https://gist.github.com/{gist_id}"),
        files=files,
    )


def guess_language_from_name(filename: str) -> str:
    lower_name = filename.lower()
    for extension, language in EXTENSION_LANGUAGE_MAP.items():
        if lower_name.endswith(extension):
            return language
    return ""


def fetch_gist_via_git(gist_id: str) -> GistData:
    if shutil.which("git") is None:
        raise RuntimeError("git is not installed, cannot fetch gists via clone")

    with TemporaryDirectory(prefix=f"gist-{gist_id}-") as temp_dir:
        clone_dir = Path(temp_dir) / "repo"
        command = [
            "git",
            "clone",
            "--depth",
            "1",
            f"https://gist.github.com/{gist_id}.git",
            str(clone_dir),
        ]
        try:
            subprocess.run(command, check=True, capture_output=True, text=True, timeout=60)
        except subprocess.CalledProcessError as error:
            stderr = (error.stderr or "").strip()
            raise RuntimeError(f"git clone failed for gist {gist_id}: {stderr}") from error
        except subprocess.TimeoutExpired as error:
            raise RuntimeError(f"git clone timed out for gist {gist_id}") from error

        files: list[GistFile] = []
        for path in sorted(clone_dir.rglob("*")):
            if not path.is_file():
                continue
            if ".git" in path.parts:
                continue

            relative_name = path.relative_to(clone_dir).as_posix()
            content = path.read_text(encoding="utf-8")
            files.append(
                GistFile(
                    filename=relative_name,
                    language=guess_language_from_name(relative_name),
                    content=content,
                )
            )

        return GistData(
            gist_id=gist_id,
            html_url=f"https://gist.github.com/{gist_id}",
            files=files,
        )


def to_fence_language(language_name: str) -> str:
    if not language_name:
        return ""
    lowered = language_name.strip().lower()
    return LANGUAGE_MAP.get(lowered, lowered.replace(" ", ""))


def fence_for_content(content: str) -> str:
    # Fence length must be longer than the longest run in content.
    runs = re.findall(r"`+", content)
    longest = max((len(run) for run in runs), default=0)
    return "`" * max(3, longest + 1)


def build_replacement(gist: GistData, source_url: str) -> str:
    lines: list[str] = []
    lines.append(f"Source: [{source_url}]({source_url})")
    lines.append("")

    for idx, gist_file in enumerate(gist.files):
        lines.append(f"**File: `{gist_file.filename}`**")
        language = to_fence_language(gist_file.language)
        fence = fence_for_content(gist_file.content)
        lines.append(f"{fence}{language}")
        lines.append(gist_file.content.rstrip("\n"))
        lines.append(fence)
        if idx < len(gist.files) - 1:
            lines.append("")

    return "\n".join(lines)


def replace_references(text: str, gists: dict[str, GistData]) -> tuple[str, int]:
    changes = 0
    cursor = 0
    result_parts: list[str] = []

    for match in ANY_GIST_REFERENCE.finditer(text):
        url = match.group("mdurl") or match.group("url")
        if not url:
            continue
        try:
            gist_id, canonical_url = normalize_gist_url(url)
        except ValueError:
            continue

        gist = gists.get(gist_id)
        if gist is None:
            continue

        replacement = "\n\n" + build_replacement(gist, canonical_url) + "\n\n"
        result_parts.append(text[cursor : match.start()])
        result_parts.append(replacement)
        cursor = match.end()
        changes += 1

    if changes == 0:
        return text, 0

    result_parts.append(text[cursor:])
    return "".join(result_parts), changes


def collect_urls() -> list[str]:
    urls: list[str] = []
    for post_path in sorted(POSTS_DIR.glob("*.md")):
        text = post_path.read_text(encoding="utf-8")
        urls.extend(match.group(1) for match in MARKDOWN_GIST_LINK.finditer(text))
        urls.extend(match.group(0) for match in BARE_GIST_LINK.finditer(text))
    return urls


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write changes to files")
    args = parser.parse_args()

    all_urls = collect_urls()
    unique_ids: list[str] = []
    seen_ids: set[str] = set()
    for url in all_urls:
        try:
            gist_id, _ = normalize_gist_url(url)
        except ValueError:
            continue
        if gist_id not in seen_ids:
            seen_ids.add(gist_id)
            unique_ids.append(gist_id)

    print(f"Found {len(all_urls)} gist URL occurrences across posts")
    print(f"Need to resolve {len(unique_ids)} unique gist IDs")

    gists: dict[str, GistData] = {}
    failures: list[tuple[str, str]] = []

    for gist_id in unique_ids:
        try:
            gists[gist_id] = fetch_gist(gist_id)
        except RuntimeError as error:
            api_error = str(error)
            try:
                gists[gist_id] = fetch_gist_via_git(gist_id)
            except RuntimeError as git_error:
                failures.append((gist_id, f"{api_error}; fallback failed: {git_error}"))
        time.sleep(0.05)

    print(f"Fetched {len(gists)} gists, failures: {len(failures)}")
    if failures:
        print("Failed gist IDs:")
        for gist_id, error in failures:
            print(f"  - {gist_id}: {error}")

    changed_files = 0
    total_replacements = 0

    for post_path in sorted(POSTS_DIR.glob("*.md")):
        original = post_path.read_text(encoding="utf-8")
        updated, replacements = replace_references(original, gists)
        if replacements == 0:
            continue

        changed_files += 1
        total_replacements += replacements

        if args.write:
            post_path.write_text(updated, encoding="utf-8")
        print(f"{post_path.name}: replaced {replacements} occurrence(s)")

    print(f"Changed files: {changed_files}")
    print(f"Total replacements: {total_replacements}")

    # Non-zero when there are unresolved gist IDs so user can inspect.
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
