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
    

class TransactionRepo:
    def __init__(self, store: EncryptedStore):
        self._store = store
        self._txns = List[Transaction] = self._store.load_transactions()
        self._next_id = (max((t.id for t in self._txns), default=0) + 1) if self._txns else 1

    def add_transaction(self) -> List[Transaction]:
        return list(self._txns)
    
    def add_transaction(self, txn: Transaction) -> Transaction:
        txn.id = self._next_id
        self._next_id += 1
        self._txns.append(txn)
        self._store.save_transactions(self._txns)
        return txn
    
    def clear(self) -> None:
        self._txns = []
        self._store.save_transactions(self._txns)
        self._next_id = 1

    