# Lesson 8 — Reading and Writing Simple Text and CSV Files

## CSV format
Values separated by commas (or semicolons/tabs) — no formal standard.

## Reading text files
`with open('file.txt', 'r') as f:` — `r/w/a/x` modes. Methods: `f.read()`,
`f.readline()`, `f.readlines()`. `with open` auto-closes the file.

## Reading CSV
```python
import csv
with open('devices.csv', 'r') as f:
    devices = csv.reader(f)
    header = next(devices)
    for row in devices:
        print(row)
```
`csv.DictReader(f)` returns dicts keyed on the header row.

## Writing
- `f.write(data)` for strings; `\n` for newlines
- `f.writelines(list)` for lists of lines
- `csv.writer(f).writerow(row)` for CSV
- `print(data, file=f)` works too

## Lab
See `labs/08_files_csv_xml/`.