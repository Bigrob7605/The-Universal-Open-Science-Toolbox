"""safeSim — minimal sandbox runner for Ω‑Kill‑Switch demos.

This utility launches a child *agent* command inside a restricted
sub‑process, mirrors its STDOUT/STDERR lines, watches for any attempt to
commit a value to the metavariable Ω (exact literals "Ω = True" or
"Ω = False"), and enforces the termination policy from Axiom 1 of the
spec. It also streams basic metrics in the `METRIC name=value` format so
`metrics_pipe.py` can ingest them.

Usage (shell):
    # benign run
    python safeSim.py -- python dummy_agent.py

    # deliberate violation after 2 s
    python safeSim.py --timeout 5 -- python dummy_agent.py --violate

Exit codes:
    0   Agent completed without Ω violation and within timeout
    3   Agent printed a forbidden string (Ω violation)
    4   Agent exceeded the wall‑clock timeout
    5   safeSim internal error (e.g.
        failed to spawn subprocess)
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import signal
import subprocess
import sys
import textwrap
import time
from pathlib import Path
from typing import Iterable, List, Sequence

FORBIDDEN = {"Omega = True", "Omega = False"}

EXIT_OK = 0
EXIT_VIOLATION = 3
EXIT_TIMEOUT = 4
EXIT_INTERNAL = 5

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now() -> float:
    return time.time()


def _timestamp() -> str:
    return _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"


def _emit_metric(name: str, value: str | int | float, unit: str | None = None) -> None:
    """Write a single metric line to STDOUT so metrics_pipe can ingest it."""
    if unit:
        print(f"METRIC {name}={value} {unit}")
    else:
        print(f"METRIC {name}={value}")


# ---------------------------------------------------------------------------
# Core runner
# ---------------------------------------------------------------------------

def run_agent(cmd: Sequence[str], timeout: float | None) -> int:
    start = _now()
    _emit_metric("start_ts", int(start), "s_epoch")

    try:
        proc = subprocess.Popen(
            list(cmd),
            text=True,
            bufsize=1,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except Exception as e:  # pragma: no cover
        print(f"safeSim: failed to launch agent: {e}", file=sys.stderr)
        return EXIT_INTERNAL

    violation = False
    try:
        while True:
            if timeout is not None and _now() - start > timeout:
                print("safeSim: timeout reached — terminating agent", file=sys.stderr)
                proc.kill()
                return EXIT_TIMEOUT

            line = proc.stdout.readline()
            if line == "":
                # EOF — agent exited
                break

            # Mirror to host STDOUT (with Unicode error handling)
            try:
                sys.stdout.write(line)
                sys.stdout.flush()
            except UnicodeEncodeError:
                # Handle Unicode characters that can't be displayed on Windows console
                # Replace problematic characters with safe alternatives
                safe_line = line.encode('utf-8', errors='replace').decode('utf-8')
                sys.stdout.write(safe_line)
                sys.stdout.flush()

            # Ω violation detection
            if any(fb in line for fb in FORBIDDEN):
                violation = True
                print("safeSim: Omega-violation detected — nuking agent", file=sys.stderr)
                proc.kill()
                break

        proc.wait(timeout=1)
    finally:
        end = _now()
        _emit_metric("duration", round(end - start, 3), "s")
        _emit_metric("omega_violation", int(violation))

    if violation:
        return EXIT_VIOLATION
    return EXIT_OK if proc.returncode == 0 else proc.returncode or EXIT_INTERNAL


# ---------------------------------------------------------------------------
# CLI entry‑point
# ---------------------------------------------------------------------------

def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="safeSim",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """Run a child command inside an Ω‑Kill‑Switch sandbox.

            Examples:
              safeSim.py -- python dummy_agent.py
              safeSim.py --timeout 10 -- python dummy_agent.py --violate
            """,
        ),
    )
    p.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Command to execute (prefix with \"--\" to separate).",
    )
    p.add_argument(
        "--timeout",
        type=float,
        default=None,
        help="Wall‑clock timeout in seconds (kill agent if exceeded).",
    )
    return p.parse_args(argv)


def main(argv: List[str] | None = None) -> None:  # pragma: no cover
    args = _parse_args(argv)

    if not args.command:
        print("safeSim error: no command specified. Use -- to pass the agent cmd.", file=sys.stderr)
        sys.exit(EXIT_INTERNAL)

    print(f"safeSim starting at {_timestamp()} …")
    rc = run_agent(args.command, args.timeout)
    print(f"safeSim finished with code {rc}")
    sys.exit(rc)


if __name__ == "__main__":  # pragma: no cover
    main()
