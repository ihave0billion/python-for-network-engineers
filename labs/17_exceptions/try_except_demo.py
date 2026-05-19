"""try/except/else/finally over a list of port-like strings."""

candidates = ["22", "443", "abc", "99999", "-1"]

for raw in candidates:
    # Two distinct failure modes — handle each separately.
    try:
        port = int(raw)
    except ValueError:
        print(f"{raw!r}: not a number")
        continue

    try:
        assert 1 <= port <= 65535
    except AssertionError:
        print(f"{raw!r}: out of range")
    else:
        print(f"{raw!r}: ok ({port})")
