"""
MMH (Immutable Memory Hash) System for Kai Core

Provides immutable data storage with cryptographic verification for:
- Scientific results and test payloads
- Signed content that cannot be altered
- 100% reproducible test recreation
- Immutable science data preservation
- Single-file format for portability and bit-perfect reproduction

Author: Kai Core System
Version: 1.0.0
"""

import hashlib
import json
import time
import hmac
import base64
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
import sqlite3
import pickle
import gzip

# MMH System Components
from .mmh_core import MMHCore, MMHRecord, MMHVerifier
from .mmh_storage import MMHStorage, MMHDatabase
from .mmh_signer import MMHSigner, MMHValidator
from .mmh_reproducer import MMHReproducer
from .mmh_file_format import MMHFileFormat, MMHFileManager
from .mmh_simple_file import SimpleMMHFile

# Version and package info
__version__ = "1.0.0"
__author__ = "Kai Core System"
__description__ = "Immutable Memory Hash System for Scientific Data"

# Main exports
__all__ = [
    "MMHCore",
    "MMHRecord", 
    "MMHVerifier",
    "MMHStorage",
    "MMHDatabase",
    "MMHSigner",
    "MMHValidator",
    "MMHReproducer",
    "MMHFileFormat",
    "MMHFileManager",
    "SimpleMMHFile"
]

print(f"🔗 MMH System v{__version__} loaded")
print("Ready for immutable data storage and verification")
print("📁 Single-file format for portability and bit-perfect reproduction") 