# Lesson 5 — Manipulating Strings

## Manipulation methods
`capitalize()`, `title()`, `upper()`, `lower()`, `swapcase()`. Strings are
immutable — these return new strings.

## split()
`str.split(separator, maxsplit)` divides into list. No args splits on
whitespace. `"1.2.3.4".split(".", 1)` → `['1', '2.3.4']`.

## Slicing
`s[i]`, `s[start:stop:step]`. Negative indices count backwards. `s[-3:]`
returns last 3 chars.

## Concatenation
`+` joins strings. Cannot mix str + int — convert with `str(n)`.

## Whitespace stripping
`strip()`, `lstrip()`, `rstrip()`.

## Formatting
- `.format()`: `"{0:^20s}".format(x)` — center, width 20, string
- f-strings (3.6+): `f"hello {name}"`
- `Template` class for safer substitution

## Escape characters
`\n` newline, `\t` tab, `\'` literal quote, `\\` literal backslash.

## Methods
`count(sub, start, end)`, `find(sub, start, end)`, `startswith(prefix)`.

## Lab
See `labs/05_string_operations/string_operations.py`.