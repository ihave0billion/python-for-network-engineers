"""Quick debugging with print() + assert — the classic first pass."""


def parse_port(raw: str) -> int:
    # Left in for the first pass. Once the bug is fixed, delete or
    # switch to `logging.debug(...)` so it doesn't ship to production.
    print(f"DEBUG parse_port({raw!r})")
    port = int(raw)
    print(f"DEBUG   -> int={port}")
    assert 1 <= port <= 65535, f"port {port} out of range"
    return port


for raw in ("22", "443", "8080"):
    keep = parse_port(raw)
    print(f"keeping {keep}")
    print("---")
