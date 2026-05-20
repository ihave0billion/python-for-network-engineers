# Lab 19 — Python pdb

Two ways to use this lab:

**Non-interactive** — `python cisco_restconf.py` (or the pyne lab
runner) runs the parser straight through and prints the uptime.

**Interactive** — uncomment the `breakpoint()` line inside
`extract_uptime_days(...)`, then run `python cisco_restconf.py`.
You'll land in pdb at that line. From there:

| Command | Action |
| --- | --- |
| `l` | List source |
| `n` | Step over (next line, don't enter calls) |
| `s` | Step into the next call |
| `p match` | Print the value of `match` |
| `c` | Continue to the next breakpoint (or end) |
| `q` | Quit pdb |

## Expected output (non-interactive)

```
R1 has been up for 12 day(s)
```
