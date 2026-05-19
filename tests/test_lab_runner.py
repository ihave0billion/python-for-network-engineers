"""Tests for the lab runner's decision logic and env injection."""
from __future__ import annotations

from pathlib import Path

from pyne.config import CMLConfig, Router
from pyne.lab_runner import (
    build_env,
    find_primary_script,
    load_simulated_output,
    run_lab,
)


def _config(
    *,
    force_simulated: bool = False,
    connect_timeout: int = 5,
    routers: list[Router] | None = None,
) -> CMLConfig:
    return CMLConfig(
        device_type="cisco_xe",
        username="cisco",
        password="cisco",
        port=22,
        routers=routers if routers is not None else [Router(name="R1", host="10.0.0.1")],
        connect_timeout=connect_timeout,
        force_simulated=force_simulated,
    )


def _write_script(lab: Path, name: str, body: str) -> Path:
    lab.mkdir(parents=True, exist_ok=True)
    script = lab / name
    script.write_text(body, encoding="utf-8")
    return script


# ---- find_primary_script -----------------------------------------------------


def test_find_primary_script_returns_alphabetically_first(tmp_path: Path) -> None:
    _write_script(tmp_path, "zebra.py", "print('z')\n")
    _write_script(tmp_path, "alpha.py", "print('a')\n")
    _write_script(tmp_path, "middle.py", "print('m')\n")

    assert find_primary_script(tmp_path).name == "alpha.py"


def test_find_primary_script_returns_none_for_empty(tmp_path: Path) -> None:
    assert find_primary_script(tmp_path) is None


def test_find_primary_script_returns_none_for_missing_dir(tmp_path: Path) -> None:
    assert find_primary_script(tmp_path / "does_not_exist") is None


# ---- build_env ---------------------------------------------------------------


def test_build_env_with_config_adds_pyne_vars() -> None:
    cfg = _config()
    env = build_env(cfg, {"EXISTING": "1"})

    assert env["EXISTING"] == "1"
    assert env["PYNE_USERNAME"] == "cisco"
    assert env["PYNE_PASSWORD"] == "cisco"
    assert env["PYNE_DEVICE_TYPE"] == "cisco_xe"
    assert env["PYNE_PORT"] == "22"
    assert env["PYNE_ROUTER_HOST"] == "10.0.0.1"
    assert env["PYNE_ROUTER_NAME"] == "R1"


def test_build_env_without_config_is_passthrough() -> None:
    env = build_env(None, {"EXISTING": "1"})
    assert env == {"EXISTING": "1"}


def test_build_env_with_no_routers_omits_router_keys() -> None:
    cfg = _config(routers=[])
    env = build_env(cfg, {})
    assert "PYNE_ROUTER_HOST" not in env
    assert "PYNE_USERNAME" in env  # other keys still present


# ---- run_lab: empty / missing ------------------------------------------------


def test_run_lab_reports_no_script_for_empty_folder(tmp_path: Path) -> None:
    result = run_lab(tmp_path, config=None)
    assert not result.simulated
    assert "no Python scripts" in result.output


# ---- run_lab: real-run success -----------------------------------------------


def test_run_lab_returns_real_output_on_success(tmp_path: Path) -> None:
    _write_script(tmp_path, "ok.py", "print('hello, network')\n")

    result = run_lab(tmp_path, config=None)

    assert not result.simulated
    assert result.output.strip() == "hello, network"
    assert result.real_returncode == 0


def test_run_lab_runs_without_config_for_pure_python_lab(tmp_path: Path) -> None:
    _write_script(tmp_path, "lab.py", "import os; print(os.environ.get('PYNE_USERNAME', 'unset'))\n")

    result = run_lab(tmp_path, config=None)

    assert not result.simulated
    assert result.output.strip() == "unset"


def test_run_lab_injects_pyne_env_when_config_present(tmp_path: Path) -> None:
    _write_script(
        tmp_path,
        "lab.py",
        "import os\nprint(os.environ['PYNE_ROUTER_HOST'])\n",
    )

    result = run_lab(tmp_path, config=_config())

    assert not result.simulated
    assert result.output.strip() == "10.0.0.1"


# ---- run_lab: force_simulated ------------------------------------------------


def test_run_lab_force_simulated_skips_real_run(tmp_path: Path) -> None:
    _write_script(tmp_path, "lab.py", "print('SHOULD NOT RUN')\n")
    (tmp_path / "_simulated_output.txt").write_text("RECORDED OUTPUT\n")

    result = run_lab(tmp_path, config=_config(force_simulated=True))

    assert result.simulated
    assert "RECORDED OUTPUT" in result.output
    assert "SHOULD NOT RUN" not in result.output
    assert "force_simulated" in result.reason


# ---- run_lab: failure → fallback --------------------------------------------


def test_run_lab_falls_back_to_simulated_on_nonzero_exit(tmp_path: Path) -> None:
    _write_script(tmp_path, "lab.py", "import sys; sys.stderr.write('boom\\n'); sys.exit(2)\n")
    (tmp_path / "_simulated_output.txt").write_text("FALLBACK OUTPUT\n")

    result = run_lab(tmp_path, config=None)

    assert result.simulated
    assert "FALLBACK OUTPUT" in result.output
    assert result.real_returncode == 2
    assert "boom" in result.real_stderr


def test_run_lab_reports_real_error_when_no_simulated(tmp_path: Path) -> None:
    _write_script(tmp_path, "lab.py", "raise RuntimeError('explode')\n")

    result = run_lab(tmp_path, config=None)

    assert not result.simulated
    assert "no `_simulated_output.txt`" in result.output
    assert "explode" in result.real_stderr
    assert result.real_returncode not in (0, None)


def test_run_lab_times_out_and_uses_fallback(tmp_path: Path) -> None:
    _write_script(tmp_path, "lab.py", "import time\ntime.sleep(5)\n")
    (tmp_path / "_simulated_output.txt").write_text("TIMEOUT FALLBACK\n")

    result = run_lab(tmp_path, config=None, timeout=0.5)

    assert result.simulated
    assert result.timed_out
    assert "TIMEOUT FALLBACK" in result.output


def test_run_lab_times_out_with_no_fallback_reports_error(tmp_path: Path) -> None:
    _write_script(tmp_path, "lab.py", "import time\ntime.sleep(5)\n")

    result = run_lab(tmp_path, config=None, timeout=0.5)

    assert not result.simulated
    assert result.timed_out
    assert "no `_simulated_output.txt`" in result.output


# ---- load_simulated_output ---------------------------------------------------


def test_load_simulated_output_returns_text(tmp_path: Path) -> None:
    (tmp_path / "_simulated_output.txt").write_text("recorded\n")
    assert load_simulated_output(tmp_path) == "recorded\n"


def test_load_simulated_output_returns_none_when_missing(tmp_path: Path) -> None:
    assert load_simulated_output(tmp_path) is None
