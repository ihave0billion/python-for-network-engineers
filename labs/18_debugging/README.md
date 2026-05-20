# Lab 18 — Debugging Basics

Run `python debug_with_print.py` to see what a typical first-pass
debugging session looks like: `print()` statements at function entry
and after a tricky cast, plus an `assert` that fails fast when an
invariant is violated. The narrative is "leave the prints in while
you're working, then delete or replace them with `logging.debug(...)`
before the script ships."

## Expected output

```
DEBUG parse_port('22')
DEBUG   -> int=22
keeping 22
---
DEBUG parse_port('443')
DEBUG   -> int=443
keeping 443
---
DEBUG parse_port('8080')
DEBUG   -> int=8080
keeping 8080
---
```
