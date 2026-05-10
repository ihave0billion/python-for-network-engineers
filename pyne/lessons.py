"""Discover and load lessons from the repo.

A lesson is a markdown file named `NN-slug.md`, where `NN` is two digits.
Lessons live in `lessons/`; for backwards compatibility, numbered markdown
files at the repo root are also accepted (lessons/ takes precedence on
duplicate numbers).

Each lesson may have:
- a knowledge check at `checks/NN.yaml`
- a lab folder at `labs/NN_*/`
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_LESSON_FILENAME = re.compile(r"^(\d{2})-(.+)\.md$")
_TITLE_PREFIX = re.compile(r"^Lesson \d+\s*[—–-]\s*")


@dataclass(frozen=True)
class Lesson:
    number: int
    slug: str
    title: str
    markdown_path: Path
    check_path: Path | None
    lab_path: Path | None

    @property
    def display_title(self) -> str:
        return self.title


def _extract_title(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    for line in text.splitlines():
        if line.startswith("# "):
            return _TITLE_PREFIX.sub("", line[2:].strip())
    return None


def _candidate_paths(repo_root: Path) -> list[Path]:
    paths: list[Path] = []
    lessons_dir = repo_root / "lessons"
    if lessons_dir.is_dir():
        paths.extend(sorted(lessons_dir.glob("*.md")))
    paths.extend(
        sorted(p for p in repo_root.glob("*.md") if _LESSON_FILENAME.match(p.name))
    )
    return paths


def discover_lessons(repo_root: Path) -> list[Lesson]:
    checks_dir = repo_root / "checks"
    labs_dir = repo_root / "labs"

    seen: set[int] = set()
    lessons: list[Lesson] = []
    for path in _candidate_paths(repo_root):
        match = _LESSON_FILENAME.match(path.name)
        if not match:
            continue
        number = int(match.group(1))
        if number in seen:
            continue
        seen.add(number)

        slug = match.group(2)
        title = _extract_title(path) or slug.replace("-", " ").title()
        check_path = checks_dir / f"{number:02d}.yaml"
        lab_path = next(iter(labs_dir.glob(f"{number:02d}_*")), None)

        lessons.append(
            Lesson(
                number=number,
                slug=slug,
                title=title,
                markdown_path=path,
                check_path=check_path if check_path.exists() else None,
                lab_path=lab_path,
            )
        )

    lessons.sort(key=lambda lesson: lesson.number)
    return lessons
