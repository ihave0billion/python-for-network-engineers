"""argparse with --router and --port (default values keep the script runnable)."""
import argparse


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Demo: what argparse parsed.")
    p.add_argument("--router", default="R1", help="router name (default: R1)")
    p.add_argument("--port", type=int, default=22, help="TCP port (default: 22)")
    return p


args = build_parser().parse_args()
print(f"router: {args.router}")
print(f"port:   {args.port}")
