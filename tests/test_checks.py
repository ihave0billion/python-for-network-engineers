"""Tests for the knowledge-check loader and code-task runner."""
from __future__ import annotations

from pathlib import Path

import pytest

from pyne.checks import (
    CheckError,
    load_check,
    run_code_task,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_load_existing_check_yaml() -> None:
    check = load_check(REPO_ROOT / "checks" / "00.yaml")
    assert check.mcq is not None
    assert check.code_task is not None
    assert check.mcq.answer == 3
    assert len(check.mcq.options) == 4
    assert check.code_task.expected_stdout_regex.startswith("^R1")


def test_load_check_rejects_out_of_range_answer(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        "title: t\n"
        "mcq:\n"
        "  question: q\n"
        "  options: [a, b]\n"
        "  answer: 5\n"
        "  explain: e\n",
        encoding="utf-8",
    )
    with pytest.raises(CheckError):
        load_check(bad)


def test_load_check_rejects_bad_regex(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        "title: t\n"
        "code_task:\n"
        "  prompt: p\n"
        "  starter: ''\n"
        "  expected_stdout_regex: '[unclosed'\n"
        "  hint: h\n",
        encoding="utf-8",
    )
    with pytest.raises(CheckError):
        load_check(bad)


def test_load_check_rejects_empty_check(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("title: t\n", encoding="utf-8")
    with pytest.raises(CheckError):
        load_check(bad)


def test_run_code_task_passes_on_matching_stdout() -> None:
    code = 'for r in ["R1", "R2", "R3"]:\n    print(r)\n'
    result = run_code_task(code, r"^R1\nR2\nR3\n?$")
    assert result.passed
    assert result.stdout == "R1\nR2\nR3\n"
    assert result.returncode == 0


def test_run_code_task_fails_on_wrong_stdout() -> None:
    code = 'print("oops")\n'
    result = run_code_task(code, r"^R1\nR2\nR3\n?$")
    assert not result.passed
    assert result.stdout == "oops\n"
    assert not result.timed_out


def test_run_code_task_fails_on_runtime_error() -> None:
    code = 'raise RuntimeError("boom")\n'
    result = run_code_task(code, r".*")
    assert not result.passed
    assert result.returncode not in (0, None)
    assert "RuntimeError" in result.stderr


def test_run_code_task_times_out() -> None:
    code = "while True:\n    pass\n"
    result = run_code_task(code, r".*", timeout=0.5)
    assert not result.passed
    assert result.timed_out
