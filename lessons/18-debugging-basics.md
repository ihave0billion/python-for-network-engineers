# Lesson 18 — Debugging Basics

## Process
1. Identify the error (compare expected vs actual output).
2. Identify the source (read trace bottom-up).
3. Identify the cause.
4. Fix and validate (one change at a time).

## Simple techniques
- `print()` — quick value inspection
- `assert` — fail fast on invariants
- `break` — exit a loop early
- `sys.exit()` — terminate the program
- `logging` module — leveled persistent logs (DEBUG/INFO/WARNING/ERROR)

## Debuggers
VS Code's integrated debugger supports breakpoints, step-through, watch and
call-stack panes.

## Lab
See `labs/18_debugging/debug_with_print.py`.