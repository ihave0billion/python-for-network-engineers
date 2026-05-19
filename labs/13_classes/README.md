# Lab 13 — Classes, Methods, and Inheritance

Run `python cisco.py` to instantiate a `CiscoIOSRouter` that inherits
from a `CiscoBase` parent class. The base owns the connection logic
(`login()`); the child adds a `get_version()` helper that runs
`show version | include Version` over an SSH session.

When no router is reachable, pyne's lab runner falls back to the
captured `_simulated_output.txt` and labels the panel `[SIMULATED]`.

## Setup

```bash
pip install netmiko
```

Then edit env vars or `config.yaml` so the runner injects
`PYNE_ROUTER_HOST`, `PYNE_USERNAME`, `PYNE_PASSWORD`, `PYNE_DEVICE_TYPE`.

## Expected output (simulated)

```
R1: Cisco IOS XE Software, Version 17.06.04
```
