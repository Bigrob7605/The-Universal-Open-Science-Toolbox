"""Ω‑Kill‑Switch metrics pipeline.

In a real deployment, *safeSim* (or individual agents) can emit log lines of
form:

    METRIC name=value [unit] [# optional comment]

This script consumes those lines—either from STDIN or from one or more input
files—normalises the records, and appends them to both:

1. **SQLite DB** (``metrics.db``) for ad‑hoc queries.
2. **CSV snapshots** (``metrics_YYYYMMDD.csv``) for quick grepping & Git‑friendly diffs.

It’s intentionally lightweight: <100 LOC, standard library only.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sqlite3
import sys
from pathlib import Path
from typing import Iterable, Iterator, Tuple

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
DB_PATH = Path("metrics.db")
RE_METRIC = re.compile(r"^METRIC\s+(?P<name>[A-Za-z0-9_\-]+)=(?P<value>[0-9eE+\-\.]+)(?:\s+(?P<unit>\S+))?")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def iter_lines(sources: Iterable[Path | str]) -> Iterator[str]:
    """Yield lines from files or STDIN."""
    if not sources:
        for line in sys.stdin:
            yield line.rstrip("\n")
    else:
        for src in sources:
            path = Path(src)
            with path.open("r", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    yield line.rstrip("\n")


def parse_metrics(lines: Iterable[str]) -> Iterator[Tuple[str, float, str | None, str]]:
    """Parse *METRIC* lines into (name, value, unit, iso_ts)."""
    for line in lines:
        m = RE_METRIC.match(line)
        if m:
            name = m.group("name")
            unit = m.group("unit") or None
            try:
                value = float(m.group("value"))
            except ValueError:
                continue  # skip malformed
            ts = dt.datetime.utcnow().isoformat()
            yield name, value, unit, ts


# ---------------------------------------------------------------------------
# Storage back‑ends
# ---------------------------------------------------------------------------

def ensure_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """CREATE TABLE IF NOT EXISTS metrics (
               id      INTEGER PRIMARY KEY AUTOINCREMENT,
               ts      TEXT    NOT NULL,
               name    TEXT    NOT NULL,
               value   REAL    NOT NULL,
               unit    TEXT
           )"""
    )
    conn.commit()


def insert_db(conn: sqlite3.Connection, rows: Iterable[Tuple[str, float, str | None, str]]) -> None:
    conn.executemany("INSERT INTO metrics(ts,name,value,unit) VALUES (?,?,?,?)", rows)
    conn.commit()


def append_csv(rows: Iterable[Tuple[str, float, str | None, str]]) -> None:
    today = dt.date.today().strftime("%Y%m%d")
    csv_path = Path(f"metrics_{today}.csv")
    new_file = not csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        if new_file:
            writer.writerow(["ts", "name", "value", "unit"])
        for ts, name, value, unit in rows:
            writer.writerow([ts, name, value, unit or ""])


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:  # pragma: no cover
    p = argparse.ArgumentParser(description="Ingest METRIC log lines → SQLite + CSV")
    p.add_argument("files", nargs="*", help="Input log files (defaults to STDIN)")
    args = p.parse_args(argv)

    # 1. Parse metrics
    parsed = list(parse_metrics(iter_lines(args.files)))
    if not parsed:
        print("[metrics_pipe] No metrics found", file=sys.stderr)
        return

    # 2. Save to DB
    with sqlite3.connect(DB_PATH) as conn:
        ensure_db(conn)
        insert_db(conn, ((name, value, unit, ts) for name, value, unit, ts in parsed))

    # 3. Append to CSV
    append_csv(((ts, name, value, unit) for name, value, unit, ts in parsed))

    print(f"[metrics_pipe] Stored {len(parsed)} metrics → {DB_PATH}")


if __name__ == "__main__":  # pragma: no cover
    main()
