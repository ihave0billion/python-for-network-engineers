# Lab 17 — Exceptions, Error Management, Assertions

Run `python try_except_demo.py` to walk a list of port-like strings
through two distinct failure modes: `ValueError` from `int()` when
the string isn't numeric, and `AssertionError` from a range check.
Notice each `except` names the **specific** exception — never a bare
`except:` — and notice how `else:` only runs when no exception fired.

## Expected output

```
'22': ok (22)
'443': ok (443)
'abc': not a number
'99999': out of range
'-1': out of range
```
