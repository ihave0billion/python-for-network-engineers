# Lesson 17 — Exceptions, Error Management, Assertions

## Error categories
- **Syntax** — caught by parser
- **Runtime / Exceptions** — raised at execution
- **Semantic** — code runs but wrong output

## Common exceptions
`AttributeError`, `IOError`, `ImportError`, `IndexError`, `KeyError`,
`KeyboardInterrupt`, `NameError`, `OSError`, `OverflowError`, `TypeError`,
`ValueError`, `ZeroDivisionError`.

## try/except/else/finally
```python
try:
    ...
except KeyError as e:
    ...
except ZeroDivisionError as e:
    ...
else:
    # ran without exception
finally:
    # always runs (cleanup)
```
Use specific exceptions, not bare `except`.

## Assertions
```python
assert condition, "error message"
```
Raises AssertionError if False — used for debugging-time invariants, not
production error handling.

## Lab
See `labs/17_exceptions/`.