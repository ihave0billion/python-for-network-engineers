# Lesson 3 — Examining Basic Data Types

## Strings (`str`)
Sequences of characters delimited by `'`, `"`, or `'''`/`"""` (multi-line).
Use the alternate quote style to embed quotes, or escape with `\`.
`type("text")` returns `<class 'str'>`.

## Integers (`int`)
Whole numbers — no decimals, no commas. Use `_` for readability:
`25_000_000`. Convert with `int()`. `int(4.55)` → `4`. `int("4.55")` raises
ValueError; `int("4")` works.

## Floats (`float`)
Decimal or exponential numbers. `float(4)` → `4.0`. Numbers exceeding system
limits show as `inf`. Beware floating-point precision:
`0.1 + 0.1 + 0.1` is `0.30000000000000004` — use `round()` to fix.

## Booleans (`bool`)
`True` / `False` (capitalized, reserved). `bool(0)` is False; any non-zero
number is True. Empty string evaluates False; non-empty string True. Useful
for validating user input.

## type() Function
Python is loosely typed. `type(obj)` returns the class of the object — useful
for runtime checks and debugging.

## Lab
See `labs/03_basic_data_types/` for `strings.py`, `integers.py`, `floats.py`,
`booleans.py`.