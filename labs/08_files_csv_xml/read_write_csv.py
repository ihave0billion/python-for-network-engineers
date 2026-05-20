"""Write a small device inventory to CSV, then read it back as dicts."""
import csv
import os
import tempfile

path = os.path.join(tempfile.gettempdir(), "pyne_devices.csv")

devices = [
    ["hostname", "ip", "role"],
    ["R1", "10.0.0.1", "core"],
    ["R2", "10.0.0.2", "edge"],
    ["SW1", "10.0.0.10", "access"],
]

# Write — note `newline=""` to avoid blank lines on Windows.
with open(path, "w", newline="") as f:
    csv.writer(f).writerows(devices)

# Read back as dicts keyed by the header row.
with open(path) as f:
    for row in csv.DictReader(f):
        print(f"{row['hostname']:5s} {row['ip']:11s} {row['role']}")
