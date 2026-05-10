# Lesson 14 — Python Modules and Packages

## Standard Library
`datetime`, `calendar`, `math`, `random`, `os`, `os.path`, `filecmp`,
`logging`, `json`, `base64`, `urllib`, `ftplib`, `wave`, `imghdr`, `sys`,
`traceback`, …

## Importing
- `import module`
- `from module import name`
- `import module as alias`
- `from module import name as alias`

`sys.path` is the search list.

## pip
`pip install package`, `pip list`, `pip freeze > requirements.txt`,
`pip install -r requirements.txt`.

## Creating modules
Any `.py` file with functions/classes is a module. Add docstrings; guard
runnable code with `if __name__ == '__main__':`.

## Virtual environments
```bash
python3 -m venv ProjectB
source ProjectB/bin/activate
pip install ...
deactivate
```

## Lab
See `labs/14_modules/`.