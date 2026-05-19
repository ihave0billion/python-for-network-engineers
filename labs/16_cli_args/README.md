# Lab 16 — Inputs from the Command Line

Run `python parse_cli.py` to see argparse parse with all defaults.
Then try:

```bash
python parse_cli.py --router R7 --port 2222
python parse_cli.py --help
```

The `--help` page is auto-generated from `add_argument` calls — no
extra code to maintain. `type=int` makes argparse cast for you and
emit a clean error if the user passes a non-integer.

## Expected output (no CLI args)

```
router: R1
port:   22
```
