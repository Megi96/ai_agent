"""Remove AI agent attribution lines from git commit messages."""

from __future__ import annotations

import re
import sys
from pathlib import Path

COAUTHOR_PATTERN = re.compile(
    r"^co-authored-by:.*("
    r"cursor|cursoragent|composer|copilot|openai|anthropic|"
    r"made with cursor"
    r")",
    re.IGNORECASE,
)

MADE_WITH_PATTERN = re.compile(r"^made-with:\s*cursor\s*$", re.IGNORECASE)


def strip_lines(text: str) -> str:
    kept: list[str] = []
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if COAUTHOR_PATTERN.match(stripped):
            continue
        if MADE_WITH_PATTERN.match(stripped):
            continue
        kept.append(line)
    return "".join(kept).rstrip() + "\n" if kept else ""


def strip_file(path: Path) -> None:
    original = path.read_text(encoding="utf-8")
    cleaned = strip_lines(original)
    if cleaned != original:
        path.write_text(cleaned, encoding="utf-8")


def main() -> None:
    if len(sys.argv) > 1:
        strip_file(Path(sys.argv[1]))
        return

    sys.stdout.write(strip_lines(sys.stdin.read()))


if __name__ == "__main__":
    main()
