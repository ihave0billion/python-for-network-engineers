# Lesson 15 — Gathering and Validating User Input

## input()
`value = input("prompt: ")` — returns a string. Cast with `int()`/`float()`.

## getpass
```python
import getpass
pw = getpass.getpass("Password: ")
```
Hides keystrokes.

## Validation
- Type — convert and catch ValueError
- Length — `if len(s) >= 5:`
- Range — `if 0 <= x <= 100:`

## Lab
See `labs/15_user_input/prompt_user.py`.