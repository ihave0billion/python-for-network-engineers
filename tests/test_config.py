"""Tests for config.yaml discovery and parsing."""
from __future__ import annotations

from pathlib import Path

import pytest

from pyne.config import find_config_path, load_config


_FULL_CONFIG = """\
cml:
  device_type: cisco_xe
  username: alice
  password: secret
  port: 2222
  routers:
    - name: R1
      host: 10.1.1.1
    - name: R2
      host: 10.1.1.2
    - name: TEMPLATE
      host: REPLACE_ME
    - name: NO_HOST
      host: ""
labs:
  connect_timeout: 30
  force_simulated: true
"""


# ---- find_config_path -------------------------------------------------------


def test_find_config_path_returns_none_when_missing(tmp_path: Path) -> None:
    assert find_config_path(tmp_path) is None


def test_find_config_path_finds_repo_config(tmp_path: Path) -> None:
    (tmp_path / "config.yaml").write_text("cml: {}\n", encoding="utf-8")
    assert find_config_path(tmp_path) == tmp_path / "config.yaml"


def test_find_config_path_respects_env_override(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    elsewhere = tmp_path / "elsewhere.yaml"
    elsewhere.write_text("cml: {}\n", encoding="utf-8")
    monkeypatch.setenv("PYNE_CONFIG_PATH", str(elsewhere))

    # Even with a different file in the repo root, the env override wins.
    (tmp_path / "config.yaml").write_text("cml: {}\n", encoding="utf-8")

    assert find_config_path(tmp_path) == elsewhere


def test_find_config_path_returns_none_when_env_points_to_missing_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PYNE_CONFIG_PATH", str(tmp_path / "does_not_exist.yaml"))
    assert find_config_path(tmp_path) is None


# ---- load_config ------------------------------------------------------------


def test_load_config_returns_none_when_no_config(tmp_path: Path) -> None:
    assert load_config(tmp_path) is None


def test_load_config_parses_full_config(tmp_path: Path) -> None:
    (tmp_path / "config.yaml").write_text(_FULL_CONFIG, encoding="utf-8")

    cfg = load_config(tmp_path)

    assert cfg is not None
    assert cfg.device_type == "cisco_xe"
    assert cfg.username == "alice"
    assert cfg.password == "secret"
    assert cfg.port == 2222
    assert cfg.connect_timeout == 30
    assert cfg.force_simulated is True


def test_load_config_filters_out_replace_me_and_empty_hosts(tmp_path: Path) -> None:
    (tmp_path / "config.yaml").write_text(_FULL_CONFIG, encoding="utf-8")

    cfg = load_config(tmp_path)

    assert cfg is not None
    assert [(r.name, r.host) for r in cfg.routers] == [
        ("R1", "10.1.1.1"),
        ("R2", "10.1.1.2"),
    ]


def test_load_config_applies_defaults_for_missing_keys(tmp_path: Path) -> None:
    # Bare-minimum config — exercise every default in load_config.
    (tmp_path / "config.yaml").write_text("cml: {}\n", encoding="utf-8")

    cfg = load_config(tmp_path)

    assert cfg is not None
    assert cfg.device_type == "cisco_ios"
    assert cfg.username == ""
    assert cfg.password == ""
    assert cfg.port == 22
    assert cfg.routers == []
    assert cfg.connect_timeout == 10
    assert cfg.force_simulated is False
