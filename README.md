# pyne — Python for Network Engineers

An interactive terminal app that teaches Python to Cisco network engineers,
one short lesson at a time. Built on the *Programming for Network Engineers
(PRNE 2.0)* learning path with a CLI-to-data-oriented mindset.

> **Status:** v0.1.0 alpha. Every lesson is gradeable and every lesson has a
> runnable lab. See [CHANGELOG.md](CHANGELOG.md) for what's in this release
> and what's slated for v0.2.

## What's inside

| Path | Contents |
|---|---|
| `lessons/` | Short markdown lessons (one concept each) — modules 1–8 |
| `labs/` | Runnable Python lab files paired with each lesson |
| `checks/` | Per-lesson knowledge-check definitions (MCQ + code task) |
| `pyne/` | Textual TUI app source |
| `tests/` | Pytest suite for the app internals |
| `teach-me-python.md` | Course design philosophy / meta-prompt |
| `Python for Network Engineer notes.pdf` | Source reference notes |
| `GITHUB_SETUP.md` | First-time GitHub publishing guide |
| `CHANGELOG.md` | Release notes — see for what's in v0.1.0 |

## Course modules

1. Intro to Python — lessons 01–02
2. Data Types — lessons 03–05
3. Conditionals and Loops — lessons 06–07
4. Reading and Writing Data to a File — lessons 08–09
5. Regular Expressions — lessons 10–11
6. Code Reuse — lessons 12–14
7. User Input — lessons 15–16
8. Troubleshooting — lessons 17–19

A new opening lesson on the CLI-to-data mindset shift will precede module 1.

## Requirements

- Python 3.10+
- A terminal that supports modern ANSI (Terminal.app, iTerm2, Windows Terminal, etc.)
- For labs: Cisco IOS-XE / IOS / NX-OS routers reachable via SSH. If you don't
  have access, labs fall back to recorded simulated output automatically.

## Quickstart

```bash
# 1. Clone
git clone https://github.com/<your-username>/python-for-network-engineers.git
cd python-for-network-engineers

# 2. Create a virtualenv and install
python3 -m venv .venv
source .venv/bin/activate
pip install -e .              # once pyproject.toml lands

# 3. Configure your lab environment
cp config.example.yaml config.yaml
$EDITOR config.yaml           # fill in your router IPs, username, password

# 4. Run the app
python -m pyne
```

## App keybindings

| Key | Action |
|---|---|
| `n` / `p` | Next / previous lesson |
| `m` | Toggle lesson complete |
| `c` | Open the knowledge check (if the lesson has one) |
| `l` | Open the lab (if the lesson has one) |
| `q` | Quit |

Inside a knowledge check:

| Key | Action |
|---|---|
| `Ctrl+S` | Submit the MCQ + run the code task |
| `Ctrl+H` | Show the hint |
| `Esc` | Back to the lesson list (passes persist on exit) |

Inside a lab:

| Key | Action |
|---|---|
| `Ctrl+R` | Run the lab's primary script |
| `Esc` | Back to the lesson list |

## Running the test suite

```bash
pip install -e ".[dev]"
pytest -q
```

50 tests across `pyne.checks`, `pyne.lab_runner`, `pyne.lessons`,
`pyne.progress`, and `pyne.config`. TUI screens are currently
smoke-tested by hand.

## Lab environment

Lab connection details (router IPs, credentials, device type) live in
`config.yaml`, which is gitignored. The template in `config.example.yaml`
shows the expected shape. If routers are unreachable when a lab runs, the
lab runner falls back to recorded output stored in
`labs/<n>/_simulated_output.txt` and labels it `[SIMULATED]`.

**Never commit real IPs or credentials.** A clean repo means
`grep -RIn '10\.' . | grep -v node_modules` returns nothing surprising.

## Packages used in labs

`netmiko`, `requests`, `pandas`, `beautifulsoup4`, `lxml`, `privy`,
`textfsm`, `ntc_templates`.

## Contributing

This project is single-author today. Once it matures, contribution guidelines
will appear in `CONTRIBUTING.md`.

## License

MIT — see [LICENSE](LICENSE).
