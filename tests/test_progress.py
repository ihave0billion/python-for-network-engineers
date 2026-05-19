"""Tests for progress persistence."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyne.progress import Progress, load_progress, save_progress, state_dir


def test_state_dir_defaults_to_home_pyne(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PYNE_STATE_DIR", raising=False)
    assert state_dir() == Path.home() / ".pyne"


def test_state_dir_respects_env_override(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("PYNE_STATE_DIR", str(tmp_path / "custom"))
    assert state_dir() == tmp_path / "custom"


def test_load_progress_returns_empty_when_file_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("PYNE_STATE_DIR", str(tmp_path))

    progress = load_progress()

    assert progress.completed == set()
    assert progress.passed_checks == set()
    assert progress.last_lesson_number is None


def test_save_and_load_round_trip(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("PYNE_STATE_DIR", str(tmp_path))
    original = Progress(
        completed={1, 3, 5}, passed_checks={1, 5}, last_lesson_number=3
    )

    save_progress(original)
    loaded = load_progress()

    assert loaded.completed == {1, 3, 5}
    assert loaded.passed_checks == {1, 5}
    assert loaded.last_lesson_number == 3


def test_save_serializes_sets_as_sorted_lists(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("PYNE_STATE_DIR", str(tmp_path))
    progress = Progress(
        completed={5, 3, 1}, passed_checks={4, 2}, last_lesson_number=5
    )

    save_progress(progress)

    data = json.loads((tmp_path / "progress.json").read_text(encoding="utf-8"))
    assert data["completed"] == [1, 3, 5]
    assert data["passed_checks"] == [2, 4]
    assert data["last_lesson_number"] == 5


def test_save_creates_state_directory_if_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    state = tmp_path / "fresh" / "nested"
    monkeypatch.setenv("PYNE_STATE_DIR", str(state))

    save_progress(Progress(completed={2}, passed_checks=set(), last_lesson_number=2))

    assert (state / "progress.json").exists()


def test_load_progress_tolerates_missing_keys(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("PYNE_STATE_DIR", str(tmp_path))
    # Older progress files may not have `passed_checks` — should default to empty.
    (tmp_path / "progress.json").write_text(
        json.dumps({"completed": [1, 2], "last_lesson_number": 2}), encoding="utf-8"
    )

    progress = load_progress()

    assert progress.completed == {1, 2}
    assert progress.passed_checks == set()
    assert progress.last_lesson_number == 2
