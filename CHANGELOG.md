# Changelog

All notable changes to pyne are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] — 2026-05-19

First public alpha. Every lesson is gradeable; every lesson has a runnable
lab folder.

### Added

#### App
- Textual TUI shell with a lesson list (left) and rendered markdown viewer
  (right). Progress persists at `~/.pyne/progress.json` (override with
  `PYNE_STATE_DIR`).
- Keybindings: `n` / `p` next/prev lesson, `m` mark complete, `c` open
  knowledge check, `l` open lab, `q` quit.

#### Knowledge checks (gradeable lessons)
- YAML check format under `checks/NN.yaml` with optional MCQ + optional
  code task. Code tasks run in a sandboxed subprocess with a hard timeout,
  and stdout is matched against an expected regex.
- `CheckScreen` UI with MCQ radio, inline code editor, hint, and result
  panel.
- 20 / 20 lessons have a check authored.

#### Labs runner (Cisco gear or recorded fallback)
- Picks the alphabetically-first `*.py` in `labs/NN_*/` as the lab's
  primary script and executes it in a subprocess.
- Injects `PYNE_USERNAME`, `PYNE_PASSWORD`, `PYNE_ROUTER_HOST`,
  `PYNE_ROUTER_NAME`, `PYNE_DEVICE_TYPE`, and `PYNE_PORT` from
  `config.yaml` so labs that opt into the env-var pattern stay
  credential-free.
- Falls back to `labs/NN_*/_simulated_output.txt` (labelled `[SIMULATED]`
  in the UI) when the real run errors, times out, or `force_simulated:
  true` is set.
- `LabScreen` UI with rendered README + script preview + Run button +
  output panel. Lab execution runs in a Textual worker thread so the UI
  stays responsive during a slow Netmiko attempt.

#### Lessons (20 / 20)
- 00 Why automate? · 01 Your first Python program · 02 Scripting, PEP 8,
  help · 03 Basic data types · 04 Lists / tuples / sets / dicts · 05
  Manipulating strings · 06 Conditionals and operators · 07 For and while
  loops · 08 Text and CSV files · 09 JSON files · 10 Regex intro · 11
  Regex on unstructured output · 12 Functions, namespaces, `__main__` ·
  13 Classes, methods, inheritance · 14 Modules and packages · 15 User
  input · 16 Command-line arguments · 17 Exceptions and assertions · 18
  Debugging basics · 19 Python pdb.

#### Labs (20 / 20 runnable through the lab runner)
- 17 pure-Python labs that run without any networking dependency.
- 3 Netmiko-flavored labs (`01_first_program`, `11_regex_unstructured`,
  `13_classes`) that ship a `_simulated_output.txt` fixture so the
  runner has something to show when no real router is reachable.

#### Tests
- 50 unit tests covering `pyne.checks`, `pyne.lab_runner`, `pyne.lessons`,
  `pyne.progress`, and `pyne.config`. Run with `pytest`.

### Fixed (during 0.1.0 development)

- Syntax error and truncated loop in `labs/03_basic_data_types/floats.py`
  that was preventing the file from parsing at all.
- Lab runner double-prepending `cwd` when given a relative `lab_path` —
  caught by integration testing against the pilot labs.

### Known limitations

- TUI screens (`app.py`, `check_screen.py`, `lab_screen.py`) are
  smoke-tested by hand; no unit tests yet. Textual's headless `pilot`
  framework is a candidate for v0.2.
- The Netmiko-flavored labs were not exercised against real Cisco gear in
  this release — only the simulated-fallback path was verified
  end-to-end. Live validation against a CSR1000v / Cat 9k / Nexus is on
  the v0.2 list.
- The lab runner picks only the alphabetically-first `*.py` per lab
  folder. A multi-script picker is planned for v0.2 so multi-file labs
  (e.g. `labs/03_basic_data_types/` with `strings.py`, `integers.py`,
  `floats.py`, `boolean.py`) become first-class in the UI.

[0.1.0]: https://github.com/ihave0billion/python-for-network-engineers/releases/tag/v0.1.0
