"""Standard-library modules a network engineer reaches for daily."""
import json
import os
import sys
from pathlib import Path

print(f"python:      {sys.version_info.major}.{sys.version_info.minor}")
print(f"script:      {os.path.basename(__file__)}")

device = {"name": "R1", "loopback": "10.0.0.1"}
print(f"device json: {json.dumps(device)}")

# pathlib joins paths in a cross-platform way (no '/' vs '\\' guessing).
config_dir = Path("/var/log") / "cisco" / "R1"
print(f"config dir:  {config_dir}")
