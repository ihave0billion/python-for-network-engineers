# Lab 11 — Regex on Unstructured Output

Run `python edit_cisco_config.py` to SSH into a lab router, run
`show ip int brief`, then pull a list of (interface, state) pairs
out of the raw text using two `re.findall` calls and `zip` — exactly
the recipe from Lesson 11.

When no router is reachable, pyne's lab runner falls back to the
captured `_simulated_output.txt` and labels the panel `[SIMULATED]`.

## Setup

```bash
pip install netmiko
```

Then edit the env vars or set them in `config.yaml` so the runner
injects them: `PYNE_ROUTER_HOST`, `PYNE_USERNAME`, `PYNE_PASSWORD`,
`PYNE_DEVICE_TYPE`.

## Expected output (simulated)

```
GigabitEthernet1          up
GigabitEthernet2          down
GigabitEthernet3          administratively down
```
