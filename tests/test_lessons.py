"""Tests for lesson discovery."""
from __future__ import annotations

from pathlib import Path

from pyne.lessons import discover_lessons


_VALID_CHECK_YAML = (
    "title: t\n"
    "mcq:\n"
    "  question: q\n"
    "  options: [a, b]\n"
    "  answer: 1\n"
    "  explain: e\n"
)


def _make_lesson(repo: Path, name: str, body: str) -> None:
    lessons_dir = repo / "lessons"
    lessons_dir.mkdir(exist_ok=True)
    (lessons_dir / name).write_text(body, encoding="utf-8")


def test_discover_lessons_empty_when_no_lessons(tmp_path: Path) -> None:
    assert discover_lessons(tmp_path) == []


def test_discover_lessons_finds_files_in_lessons_dir(tmp_path: Path) -> None:
    _make_lesson(tmp_path, "00-intro.md", "# Lesson 0 — Intro\n")
    _make_lesson(tmp_path, "01-first.md", "# Lesson 1 — First\n")

    lessons = discover_lessons(tmp_path)

    assert [l.number for l in lessons] == [0, 1]
    assert [l.title for l in lessons] == ["Intro", "First"]


def test_discover_lessons_sorts_by_number(tmp_path: Path) -> None:
    _make_lesson(tmp_path, "05-five.md", "# Lesson 5 — Five\n")
    _make_lesson(tmp_path, "02-two.md", "# Lesson 2 — Two\n")
    _make_lesson(tmp_path, "00-zero.md", "# Lesson 0 — Zero\n")

    lessons = discover_lessons(tmp_path)

    assert [l.number for l in lessons] == [0, 2, 5]


def test_discover_lessons_strips_lesson_prefix_from_h1(tmp_path: Path) -> None:
    _make_lesson(tmp_path, "00-intro.md", "# Lesson 0 — Why Automate?\n\nBody.\n")

    lessons = discover_lessons(tmp_path)

    assert lessons[0].title == "Why Automate?"


def test_discover_lessons_falls_back_to_slug_title(tmp_path: Path) -> None:
    _make_lesson(tmp_path, "00-no-heading.md", "No top-level heading here.\n")

    lessons = discover_lessons(tmp_path)

    assert lessons[0].title == "No Heading"


def test_discover_lessons_wires_check_and_lab_paths(tmp_path: Path) -> None:
    _make_lesson(tmp_path, "00-intro.md", "# Lesson 0 — Intro\n")
    (tmp_path / "checks").mkdir()
    (tmp_path / "checks" / "00.yaml").write_text(_VALID_CHECK_YAML, encoding="utf-8")
    (tmp_path / "labs").mkdir()
    (tmp_path / "labs" / "00_demo").mkdir()

    lessons = discover_lessons(tmp_path)

    assert lessons[0].check_path is not None
    assert lessons[0].check_path.name == "00.yaml"
    assert lessons[0].lab_path is not None
    assert lessons[0].lab_path.name == "00_demo"


def test_discover_lessons_returns_none_for_missing_check_and_lab(tmp_path: Path) -> None:
    _make_lesson(tmp_path, "00-intro.md", "# Lesson 0 — Intro\n")

    lessons = discover_lessons(tmp_path)

    assert lessons[0].check_path is None
    assert lessons[0].lab_path is None


def test_discover_lessons_dir_takes_precedence_over_repo_root(tmp_path: Path) -> None:
    _make_lesson(tmp_path, "00-canonical.md", "# Lesson 0 — Canonical\n")
    # A duplicate at the repo root should be ignored in favor of lessons/.
    (tmp_path / "00-root.md").write_text("# Lesson 0 — Root duplicate\n", encoding="utf-8")

    lessons = discover_lessons(tmp_path)

    assert len(lessons) == 1
    assert lessons[0].title == "Canonical"


def test_discover_lessons_ignores_non_lesson_markdown(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Not a lesson\n", encoding="utf-8")
    _make_lesson(tmp_path, "00-intro.md", "# Lesson 0 — Intro\n")

    lessons = discover_lessons(tmp_path)

    assert [l.number for l in lessons] == [0]
