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
        key_len = len(self.key)
        return bytes(b ^ self.key[i % key_len] for i, b in enumerate(data))
    
    def save_transactions(self, txns: List[Transaction]) -> None:
        if not self.path.parent.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
        raw = json.dumps([txn.dict() for txn in txns], default=str).encode('utf-8')
        encrypted = self._xor_bytes(raw)
        self.path.write_bytes(encrypted)

    def load_transactions(self) -> List[Transaction]:
        if not self.path.exists():
            return []
        encrypted = self.path.read_bytes()
        raw = self._xor_bytes(encrypted)
        data = json.loads(raw.decode('utf-8'))
        return [Transaction(**item) for item in data]
    
    