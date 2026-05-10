# Lesson 7 — For and While Loops

## for loops
Iterate any iterable: string, list, dict, tuple, set.
```python
for ip in ip_list:
    print(ip)
```

## while loops
Run while expression is True.
```python
i = 4
while i > 0:
    print(i)
    i -= 1
```

## Iterating dicts
`for k in d:`, `for v in d.values():`, `for k, v in d.items():`.

## range()
`range(start, stop, step)` — stop is exclusive.

## break and continue
`break` exits the loop. `continue` skips the rest of this iteration.

## Lab
See `labs/07_loops/`.