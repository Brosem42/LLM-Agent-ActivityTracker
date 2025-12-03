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

def transactions_to_df(txns: List[Transaction]) -> pd.DataFrame:
    data = [
        {
            "id": t.id,
            "service_name": t.service_name,
            "amount": t.amount,
            "currency": t.currency,
            "timestamp": t.timestamp,
            "category": t.category
        }
        for t in txns
    ]
    return pd.DataFrame(data)

def export_to_csv(txns: List[Transaction], path: str) -> str:
    df = transactions_to_df(txns)
    df.to_csv(path, index=False)
    return path

def detect_anomalies(txns: List[Transaction]) -> AnomalyCalc: # pyright: ignore[reportUndefinedVariable]
    if not txns:
        return AnomalyCalc(anomalies=[], details="No data available for calculation.") # pyright: ignore[reportUndefinedVariable]
    
    df = transactions_to_df(txns)
    df["day"] = df["timestamp"].dt.floor("D")
    daily = df.groupby("day")["amount"].sum().reset_index()
    amounts = daily["amount"].values.astype(float)
    mean = daily["amount"].values.astype(float)
    std = amounts.std() if amounts.std() > 0 else 1.0
    z_score = (amounts - mean) / std

    anomaly_days = set(daily["day"][np.abs(z_score) > 2].dt.to_pydatetime())
    anomalies: List[Transaction] = [
        t for t in txns if t.timestamp.replace(hour=0, minute=0, second=0, microsecond=0) in anomaly_days
    ]

    details = (
        f"Detected {len(anomaly_days)} anomaly days(s) based on z-score >i 2.\n",
        f"Mean daily spend: {mean:.2f}, std: {std:.2f}."
    )

    return AnomalyCalc(anomalies=anomalies, details=details) # type: ignore
