# Lab 7 — For and While Loops

Run `python loops.py` to see a basic `for` over a list, a `range`-based
loop building loopback IPs, dict iteration with `.items()`, and a
`while True` that uses `break` + `continue` to skip a router that's
in maintenance.

## Expected output

```
polling R1...
polling R2...
polling R3...
polling R4...

loopbacks via range:
  192.168.1.1
  192.168.1.2
  192.168.1.3
  192.168.1.4

mgmt IPs:
  R1 -> 10.0.0.1
  R2 -> 10.0.0.2
  R3 -> 10.0.0.3

scanning interfaces:
  scanning R1
  scanning R2
  skip R3 (in maintenance)
  scanning R4
```
