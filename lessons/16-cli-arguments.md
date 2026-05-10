# Lesson 16 — Inputs from the Command Line

## sys.argv
`sys.argv` is a list; index 0 is the script name.

## argparse
```python
import argparse
parser = argparse.ArgumentParser(description='...')
parser.add_argument('-R', '--router', help='router name')
parser.add_argument('-IP', help='ip address')
args = parser.parse_args()
print(args.router, args.IP)
```
`--help` is generated automatically.

## Lab
See `labs/16_cli_args/`.