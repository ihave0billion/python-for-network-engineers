"""Knowledge check loading and code-task execution.

A check lives at `checks/NN.yaml` and may contain an `mcq` block, a
`code_task` block, or both. The code task is executed in a subprocess
with a hard timeout, and its stdout is matched against a regex.
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import yaml

DEFAULT_TIMEOUT_SECONDS = 5


class CheckError(Exception):
    """Raised when a check YAML file is malformed."""


@dataclass(frozen=True)
class MCQ:
    question: str
    options: list[str]
    answer: int  # 1-based index into options
    explain: str


@dataclass(frozen=True)
class CodeTask:
    prompt: str
    starter: str
    expected_stdout_regex: str
    hint: str


@dataclass(frozen=True)
class Check:
    title: str
    mcq: MCQ | None
    code_task: CodeTask | None


@dataclass(frozen=True)
class CodeResult:
    passed: bool
    stdout: str
    stderr: str
    timed_out: bool
    returncode: int | None


def load_check(path: Path) -> Check:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    title = str(raw.get("title") or path.stem)

    mcq_raw = raw.get("mcq")
    mcq: MCQ | None = None
    if mcq_raw is not None:
        options = mcq_raw.get("options") or []
        if not isinstance(options, list) or not options:
            raise CheckError(f"{path}: mcq.options must be a non-empty list")
        answer = mcq_raw.get("answer")
        if not isinstance(answer, int) or not (1 <= answer <= len(options)):
            raise CheckError(
                f"{path}: mcq.answer must be a 1-based index into options"
            )
        mcq = MCQ(
            question=str(mcq_raw.get("question", "")).strip(),
            options=[str(o) for o in options],
            answer=answer,
            explain=str(mcq_raw.get("explain", "")).strip(),
        )

    task_raw = raw.get("code_task")
    code_task: CodeTask | None = None
    if task_raw is not None:
        regex = task_raw.get("expected_stdout_regex")
        if not isinstance(regex, str) or not regex:
            raise CheckError(
                f"{path}: code_task.expected_stdout_regex must be a non-empty string"
            )
        try:
            re.compile(regex)
        except re.error as exc:
            raise CheckError(f"{path}: invalid regex: {exc}") from exc
        code_task = CodeTask(
            prompt=str(task_raw.get("prompt", "")).strip(),
            starter=str(task_raw.get("starter", "")),
            expected_stdout_regex=regex,
            hint=str(task_raw.get("hint", "")).strip(),
        )

    if mcq is None and code_task is None:
        raise CheckError(f"{path}: must define at least one of mcq, code_task")

    return Check(title=title, mcq=mcq, code_task=code_task)


def run_code_task(
    code: str,
    expected_stdout_regex: str,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> CodeResult:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as fh:
        fh.write(code)
        script_path = Path(fh.name)
    try:
        try:
            proc = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            return CodeResult(
                passed=False,
                stdout=exc.stdout or "" if isinstance(exc.stdout, str) else "",
                stderr=(
                    f"Execution exceeded {timeout:g}s and was terminated."
                ),
                timed_out=True,
                returncode=None,
            )
    finally:
        script_path.unlink(missing_ok=True)

    if proc.returncode != 0:
        return CodeResult(
            passed=False,
            stdout=proc.stdout,
            stderr=proc.stderr,
            timed_out=False,
            returncode=proc.returncode,
        )

    passed = re.fullmatch(expected_stdout_regex, proc.stdout, re.DOTALL) is not None
    return CodeResult(
        passed=passed,
        stdout=proc.stdout,
        stderr=proc.stderr,
        timed_out=False,
        returncode=proc.returncode,
    )
