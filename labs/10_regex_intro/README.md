# Lab 10 — Regular Expressions Intro

Run `python regex_basics.py` to see the three workhorse `re` methods —
`search` (first match), `findall` (all matches), and `sub` (substitute)
— applied to a small chunk of Cisco config text.

## Expected output

```
first ip:  10.0.0.1
all ips:   ['10.0.0.1', '10.0.1.1']

after sub:
interface Gi1/0/0
 ip address 10.0.0.1 255.255.255.0
 no shutdown
interface Gi1/0/1
 ip address 10.0.1.1 255.255.255.0
 shutdown
```
