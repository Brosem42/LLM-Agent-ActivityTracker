from __future__ import annotations
import json 
from pathlib import Path

from typing import List

from .models import Transaction

class EncryptedStore:
    def __init__(self, path: Path, key: bytes= b"Agent-Actvitiy tracker-key"):
        self.path = path
        self.key = key

    def _xor_bytes(self, data: bytes) -> bytes: