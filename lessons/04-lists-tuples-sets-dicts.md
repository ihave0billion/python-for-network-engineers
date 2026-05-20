# Lesson 4 — Lists, Tuples, Sets, and Dictionaries

## Variables
Variables are named pointers to PyObjects. Names are case-sensitive, cannot
start with a digit, cannot be keywords, use snake_case. Global vs local scope.

## Lists `[]`
Ordered, mutable, indexable, allow duplicates. Operations: `append(x)`,
`insert(i, x)`, `pop()`, `pop(i)`, `remove(x)`, `count(x)`, `len(list)`.
Negative indices count from the end (`-1` = last).

## Tuples `()`
Ordered and indexable but **immutable**. Methods: `count()`, `index()`.
Use when data should not be changed.

## Sets `{}`
Unordered, unindexed, no duplicates, mutable. Useful for `union()`,
`intersection()`, dedupe via `set(my_list)`.

## Dictionaries `{key: value}`
Unordered (insertion-ordered since 3.6) key-value mapping. Keys must be
immutable. Access with `d[key]`; safe access with `d.get(key)`. Methods:
`items()`, `keys()`, `values()`, `pop(k)`, `update(d2)`, `clear()`.

## Nested data
Lists of lists, dicts of lists, etc. Navigate with chained indexing/keys:
`net[2]["device"]["interface"]`.

## Lab
See `labs/04_collections/` for `lists.py` and `tuples.py`. Set and
dict examples are introduced inline in the lesson above; standalone
lab scripts for those are planned.