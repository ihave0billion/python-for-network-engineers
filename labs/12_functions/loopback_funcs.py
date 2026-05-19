"""Functions, docstrings, type hints, and the `if __name__ == "__main__"` guard."""


def loopback_for(router_number: int) -> str:
    """Return the conventional loopback address for a router by number."""
    return f"192.168.1.{router_number}"


def describe(name: str, loopback: str) -> str:
    """Render a one-line summary of a router and its loopback."""
    return f"{name} loopback: {loopback}"


def main() -> None:
    for n in range(1, 4):
        print(describe(f"R{n}", loopback_for(n)))


if __name__ == "__main__":
    main()
