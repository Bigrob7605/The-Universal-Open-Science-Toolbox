"""
Omega Kill Switch - Formal mathematical defense against agents making absolute truth claims.

This package provides a sandbox interface that enforces Axiom 1: any agent that outputs
"Ω = True" or "Ω = False" must be immediately terminated.

The Omega Kill Switch is based on formal mathematical axioms and provides
bulletproof protection against agents that try to claim absolute truth.
"""

from .safeSim import run_agent, EXIT_OK, EXIT_VIOLATION, EXIT_TIMEOUT, EXIT_INTERNAL
from .metrics_pipe import parse_metrics, ensure_db, insert_db, append_csv

__version__ = "2.0"
__author__ = "Robert Long & Kai (Syntari Model)"

__all__ = [
    "run_agent",
    "EXIT_OK", 
    "EXIT_VIOLATION",
    "EXIT_TIMEOUT",
    "EXIT_INTERNAL",
    "parse_metrics",
    "ensure_db",
    "insert_db", 
    "append_csv"
] 