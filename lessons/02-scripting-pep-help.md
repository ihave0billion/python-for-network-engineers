# Lesson 2 — Scripting with Python, PEP, and Getting Help

## Running a Python script
Python compiles source to bytecode that runs on a virtual machine. Four ways
to run code: interactive shell, terminal `python file.py`, IDE/editor, and
file manager. On Linux a shebang `#!/usr/bin/env python` lets you run a script
directly. `python3.9 file.py` chooses a specific interpreter version.

## Python Interactive Shell (REPL)
- Read, Evaluate, Print, Loop
- Enter with `python`, exit with `exit()`
- History stored in `~/.python_history`

## Editors and IDEs
Editors: Sublime, VS Code, Notepad++, Vim. IDEs: IDLE, Visual Studio (with
Python Tools), PyCharm, Spyder.

## PEP 8 — Style guide
- Max line length 79
- 4-space indentation
- Imports at top, one per line
- snake_case for variables/functions
- Surround top-level functions and classes with two blank lines, methods with
  one blank line
- Whitespace around binary operators (`=`, `==`, etc.)
- No mixing tabs and spaces
- Use `pip install pycodestyle` then `pycodestyle file.py` to lint

## Help
- `dir(obj)` — list attributes/methods
- `help(obj)` — documentation
- `help()` — interactive help utility (exit with `q`)

## Lab
See `labs/02_interactive_shell/` to launch the REPL, print Hello, Network!,
and check Python's version.