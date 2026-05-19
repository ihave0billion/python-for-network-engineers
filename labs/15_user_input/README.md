# Lab 15 — Gathering and Validating User Input

Run `python prompt_user.py` at a real terminal to be prompted for a
port number. The script casts to int (handling `ValueError` if the
input isn't numeric) and range-checks against the TCP/UDP space.

When pyne runs the script through its lab runner there's no tty, so
the script detects that and uses a demo value (`22`) instead of
hanging on `input()`. That `sys.stdin.isatty()` pattern is worth
remembering whenever you mix interactive and batch invocations of
the same script.

## Expected output (non-interactive)

```
(non-interactive — using demo port 22)
port 22: valid
```
