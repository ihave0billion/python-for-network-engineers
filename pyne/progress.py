"""Persisted user progress at ~/.pyne/progress.json."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_STATE_DIR = Path.home() / ".pyne"
PROGRESS_FILENAME = "progress.json"


def state_dir() -> Path:
    override = os.environ.get("PYNE_STATE_DIR")
    return Path(override).expanduser() if override else DEFAULT_STATE_DIR


@dataclass
class Progress:
    completed: set[int] = field(default_factory=set)
    passed_checks: set[int] = field(default_factory=set)
    last_lesson_number: int | None = None


def load_progress() -> Progress:
    path = state_dir() / PROGRESS_FILENAME
    if not path.exists():
        return Progress()
    data = json.loads(path.read_text(encoding="utf-8"))
    return Progress(
        completed=set(data.get("completed", [])),
        passed_checks=set(data.get("passed_checks", [])),
        last_lesson_number=data.get("last_lesson_number"),
    )


def save_progress(progress: Progress) -> None:
    directory = state_dir()
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / PROGRESS_FILENAME
    payload = {
        "completed": sorted(progress.completed),
        "passed_checks": sorted(progress.passed_checks),
        "last_lesson_number": progress.last_lesson_number,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
