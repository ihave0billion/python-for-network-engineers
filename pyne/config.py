"""Load `config.yaml` + `.env`. Returns None if config is absent (offline mode)."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml
from dotenv import load_dotenv


@dataclass(frozen=True)
class Router:
    name: str
    host: str


@dataclass(frozen=True)
class CMLConfig:
    device_type: str
    username: str
    password: str
    port: int
    routers: list[Router]
    connect_timeout: int
    force_simulated: bool


def find_config_path(repo_root: Path) -> Path | None:
    override = os.environ.get("PYNE_CONFIG_PATH")
    if override:
        path = Path(override).expanduser()
        return path if path.exists() else None
    candidate = repo_root / "config.yaml"
    return candidate if candidate.exists() else None


def load_config(repo_root: Path) -> CMLConfig | None:
    load_dotenv(repo_root / ".env", override=False)
    path = find_config_path(repo_root)
    if path is None:
        return None

    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    cml = raw.get("cml", {})
    labs = raw.get("labs", {})
    routers = [
        Router(name=str(r["name"]), host=str(r["host"]))
        for r in cml.get("routers", [])
        if r.get("host") and r["host"] != "REPLACE_ME"
    ]
    return CMLConfig(
        device_type=cml.get("device_type", "cisco_ios"),
        username=cml.get("username", ""),
        password=cml.get("password", ""),
        port=int(cml.get("port", 22)),
        routers=routers,
        connect_timeout=int(labs.get("connect_timeout", 10)),
        force_simulated=bool(labs.get("force_simulated", False)),
    )
