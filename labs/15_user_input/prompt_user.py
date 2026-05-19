"""input() + validation. Falls back to a demo value when stdin isn't a tty."""
import sys

if sys.stdin.isatty():
    raw = input("Enter a TCP port (1-65535): ")
else:
    print("(non-interactive — using demo port 22)")
    raw = "22"

try:
    port = int(raw)
except ValueError:
    print(f"not a number: {raw!r}")
    sys.exit(1)

if 1 <= port <= 65535:
    print(f"port {port}: valid")
else:
    print(f"port {port}: out of range")
