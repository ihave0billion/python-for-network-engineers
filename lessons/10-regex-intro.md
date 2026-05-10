# Lesson 10 — Introducing Regular Expressions

Use `import re`. Steps: import → write pattern → access data → choose method.
Patterns can be raw strings: `r'GigabitEthernet[1-4]'`.

## Metacharacters
- `[]` character class — `[a-z]`, `[0-9]`, `[^abc]`
- `.` any char (except newline)
- `^` start, `$` end
- `*` zero or more, `+` one or more, `?` zero or one
- `{n}` exactly n times
- `()` grouping
- `\` escape
- `|` alternation

## Common methods
- `re.search(pat, data)` — first match (Match object) or None
- `re.findall(pat, data)` — list of all matches
- `re.split(pat, data)` — split on pattern
- `re.sub(pat, repl, data)` — substitute

Helpful tester: <https://regexr.com/>

## Lab
See `labs/10_regex_intro/`.