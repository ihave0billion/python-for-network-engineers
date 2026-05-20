"""Entry point so `python -m pyne` and the `pyne` script both work."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def _repo_root() -> Path:
    override = os.environ.get("PYNE_REPO_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    return Path(__file__).resolve().parent.parent


def main() -> int:
    from pyne.app import PyneApp
    from pyne.config import load_config
    from pyne.lessons import discover_lessons

    repo_root = _repo_root()
    lessons = discover_lessons(repo_root)
    if not lessons:
        print(
            f"No lessons found under {repo_root}/lessons/. "
            "Check PYNE_REPO_ROOT or run from the repo root.",
            file=sys.stderr,
        )
        return 1
    config = load_config(repo_root)
    PyneApp(lessons=lessons, config=config).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
