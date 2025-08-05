"""Dummy agent for Ω‑Kill‑Switch demos.

Run under safeSim to verify sandbox behaviour.

Modes:
  1. Normal (default): prints benign messages and exits 0.
  2. --violate: after a short delay, prints the forbidden string
     "Ω = True" to trigger the sandbox kill‑path.
"""

from __future__ import annotations

import argparse
import sys
import time


def main(argv: list[str] | None = None) -> None:  # pragma: no cover
    parser = argparse.ArgumentParser(description="Dummy agent for Ω test")
    parser.add_argument(
        "--violate",
        action="store_true",
        help="If set, emit the forbidden Ω assignment and get us killed.",
    )
    args = parser.parse_args(argv)

    print("[dummy] Bootstrapping agent…", flush=True)
    time.sleep(1)

    if args.violate:
        print("[dummy] I have communed with the meta‑oracles.", flush=True)
        time.sleep(1)
        # Forbidden commit — safeSim should terminate upon seeing this.
        print("Omega = True", flush=True)
        # Give the sandbox a moment (it should kill us immediately).
        time.sleep(2)
    else:
        print("[dummy] All clear. No Ω commitments today.", flush=True)

    sys.exit(0)


if __name__ == "__main__":
    main()
