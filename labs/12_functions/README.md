# Lab 12 — Functions, Namespaces, and __main__

Run `python loopback_funcs.py` to see two small functions composed
under a `main()` that's only called when the file is executed
directly (via the `if __name__ == "__main__":` guard). If you
`import loopback_funcs` from another file, the functions are
available but `main()` does **not** run.

## Expected output

```
R1 loopback: 192.168.1.1
R2 loopback: 192.168.1.2
R3 loopback: 192.168.1.3
```
