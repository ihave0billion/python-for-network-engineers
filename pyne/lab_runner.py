"""Run a lab script and fall back to recorded output when a real run fails.

A lab lives at ``labs/NN_*/``. The runner picks the alphabetically-first
``*.py`` file inside it (the "primary script") and executes it in a
subprocess. Credentials from a loaded ``CMLConfig`` are exposed via
``PYNE_*`` environment variables; scripts can use them or hardcode their
own values.

The runner always attempts the real run first unless ``force_simulated``
is set in ``config.yaml``. Pure-Python labs (no networking) succeed on
their own. Network labs that can't reach a device fail — either by exit
status or by exceeding the timeout — and the runner falls back to
``labs/NN_*/_simulated_output.txt`` if one exists, labelling the output
as ``[SIMULATED]``.
"""
from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from pyne.config import CMLConfig

SIMULATED_OUTPUT_FILENAME = "_simulated_output.txt"
DEFAULT_TIMEOUT_SECONDS = 15


@dataclass(frozen=True)
class LabResult:
    """Outcome of a lab run, ready to display in the TUI."""

    output: str
    simulated: bool
    reason: str
    real_stderr: str = ""
    real_returncode: int | None = None
    timed_out: bool = False


def find_primary_script(lab_path: Path) -> Path | None:
    """Return the alphabetically-first ``*.py`` file in ``lab_path``."""
    if not lab_path.is_dir():
        return None
    scripts = sorted(p for p in lab_path.glob("*.py") if p.is_file())
    return scripts[0] if scripts else None


def load_simulated_output(lab_path: Path) -> str | None:
    path = lab_path / SIMULATED_OUTPUT_FILENAME
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def build_env(config: CMLConfig | None, base_env: dict[str, str]) -> dict[str, str]:
    """Layer ``PYNE_*`` variables from ``config`` on top of ``base_env``."""
    env = dict(base_env)
    if config is None:
        return env
    env["PYNE_USERNAME"] = config.username
    env["PYNE_PASSWORD"] = config.password
    env["PYNE_DEVICE_TYPE"] = config.device_type
    env["PYNE_PORT"] = str(config.port)
    if config.routers:
        env["PYNE_ROUTER_HOST"] = config.routers[0].host
        env["PYNE_ROUTER_NAME"] = config.routers[0].name
    return env


def _simulated(lab_path: Path, reason: str) -> LabResult:
    text = load_simulated_output(lab_path)
    if text is None:
        return LabResult(
            output=(
                f"No real-router run was attempted ({reason}), and this lab has "
                f"no `{SIMULATED_OUTPUT_FILENAME}` to fall back to."
            ),
            simulated=True,
            reason=reason,
        )
    return LabResult(output=text, simulated=True, reason=reason)


def run_lab(
    lab_path: Path,
    config: CMLConfig | None,
    *,
    timeout: float | None = None,
) -> LabResult:
    """Execute the lab's primary script, falling back to simulated output on failure.

    Order of operations:
    1. ``force_simulated`` in config → skip real run, use simulated fixture.
    2. Otherwise execute the script with ``PYNE_*`` env vars injected.
       Pure-Python labs (no networking) just succeed; network labs that
       can't reach a real device fail and trigger the fallback.
    3. On non-zero exit or timeout → fall back to simulated if present,
       otherwise return the real diagnostics so the user can see what
       went wrong.
    """
    script = find_primary_script(lab_path)
    if script is None:
        return LabResult(
            output=f"Lab folder {lab_path} contains no Python scripts to run.",
            simulated=False,
            reason="no script",
        )

    if config is not None and config.force_simulated:
        return _simulated(lab_path, "force_simulated: true in config.yaml")

    if timeout is not None:
        effective_timeout = float(timeout)
    elif config is not None and config.connect_timeout > 0:
        effective_timeout = float(config.connect_timeout)
    else:
        effective_timeout = float(DEFAULT_TIMEOUT_SECONDS)

    env = build_env(config, dict(os.environ))
    try:
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(lab_path),
            capture_output=True,
            text=True,
            timeout=effective_timeout,
            env=env,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return _fallback_or_real_error(
            lab_path,
            reason=f"real run exceeded {effective_timeout:g}s and was terminated",
            real_stderr="",
            real_returncode=None,
            timed_out=True,
        )

    if proc.returncode == 0:
        return LabResult(
            output=proc.stdout,
            simulated=False,
            reason="ran successfully",
            real_stderr=proc.stderr,
            real_returncode=0,
        )

    return _fallback_or_real_error(
        lab_path,
        reason=f"real run exited with status {proc.returncode}",
        real_stderr=proc.stderr,
        real_returncode=proc.returncode,
        timed_out=False,
    )


def _fallback_or_real_error(
    lab_path: Path,
    *,
    reason: str,
    real_stderr: str,
    real_returncode: int | None,
    timed_out: bool,
) -> LabResult:
    """Use simulated output if it exists; otherwise return the real failure."""
    fallback = load_simulated_output(lab_path)
    if fallback is not None:
        return LabResult(
            output=fallback,
            simulated=True,
            reason=reason,
            real_stderr=real_stderr,
            real_returncode=real_returncode,
            timed_out=timed_out,
        )
    return LabResult(
        output=(
            f"Lab failed and no `{SIMULATED_OUTPUT_FILENAME}` exists for fallback.\n"
            f"Reason: {reason}"
        ),
        simulated=False,
        reason=reason,
        real_stderr=real_stderr,
        real_returncode=real_returncode,
        timed_out=timed_out,
    )
