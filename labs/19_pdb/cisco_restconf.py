"""Walk through a small parser. Drop a breakpoint() to step into it with pdb.

To debug interactively, uncomment the `breakpoint()` line below and run:

    python cisco_restconf.py

You'll land in pdb at that line. From there try `l` (list source),
`n` (next), `s` (step), `p var` (print a variable), `c` (continue),
`q` (quit). The pyne lab runner is non-interactive — it just runs
the script straight through and prints the final result.
"""
import re


def extract_uptime_days(version_output: str) -> int:
    # breakpoint()   # <-- uncomment to drop into pdb here
    match = re.search(r"uptime is (\d+) days", version_output)
    if match is None:
        return 0
    return int(match.group(1))


sample = "Router R1 uptime is 12 days, 4 hours, 35 minutes"
days = extract_uptime_days(sample)
print(f"R1 has been up for {days} day(s)")
