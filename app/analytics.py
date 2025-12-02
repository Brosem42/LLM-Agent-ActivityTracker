from __future__ import annotations
from collections import defaultdict
from typing import Dict, List, Tuple

#imports
import numpy as np #type: ignore
import pandas as pd #type: ignore

from .models import Transaction, FinancialSummary

def compute_fin_summary(txns: List[Transaction]) -> FinancialSummary:
    total = sum(t.amount for t in txns)
    per_service: Dict[str, float] = defaultdict(float)
    for t in txns:
        per_service[t.service_name] += t.amount
    currency = txns[0].currency if txns else "USD"
    return FinancialSummary(total_spend=total, per_microservice=dict(per_service), currency=currency)

def apply_6040_protocol(total_spend: float) -> Tuple[float, float]:
    operational_expenses = total_spend * 0.6 
    budget_runway = total_spend * 0.4 
    return operational_expenses, budget_runway