# Lesson 12 — Functions, Namespaces, Scopes, and the Main Construct

## DRY principle
Don't Repeat Yourself. Reuse code via functions or modules.

## Functions
```python
def name(params):
    """docstring"""
    statements
    return value
```

## Comments and docstrings
- `#` for single-line comments (≤72 chars)
- Triple-quoted docstrings as first statement of module, class, function
- PEP 257 style

## Namespaces (LEGB lookup order)
- **L**ocal — current function
- **E**nclosing — outer function in nested setup
- **G**lobal — module level
- **B**uilt-in — `print`, `len`, …

## main() construct
```python
def main():
    ...

if __name__ == '__main__':
    main()
```
`__name__` is `'__main__'` when run directly, else the module name.

## Lab
See `labs/12_functions/`.