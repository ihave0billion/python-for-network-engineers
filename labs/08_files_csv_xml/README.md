# Lab 8 — Reading and Writing Text/CSV Files

Run `python read_write_csv.py` to write a small device inventory to a
CSV in the OS temp directory, then read it back using `csv.DictReader`
and print one row per device.

Demonstrates the `with open(...) as f:` context manager, `csv.writer`
+ `writerows`, and dict-style access to columns by header name.

## Expected output

```
R1    10.0.0.1    core
R2    10.0.0.2    edge
SW1   10.0.0.10   access
```
