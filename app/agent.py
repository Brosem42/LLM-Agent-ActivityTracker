from __future__ import annotations
from typing import List
import re
from datetime import datetime

from .analytics import (
    apply_6040_protocol,
    compute_fin_summary,
    detect_anomalies,
    export_to_csv,
    plot_daily_spend_chart
    
)

from .datastore import TransactionRepo
from .models import ChatResponse, Transaction
from .sandbox import run_untrusted_llm, run_untrusted_slm

class FinAgent:
    def __init__(self, repo: TransactionRepo):
        self.repo = repo
    def handle_message(self, message: str) -> ChatResponse:
        text = message.strip().lower()

        if text.startswith("add transaction"):
            reply = self._handle_add_transaction(message)
        elif "total spend" in text:
            reply = self._handle_total_spend()
        elif "spend per app" in text or "per app" in text:
            reply = self._handle_spend_per_app()
        elif "6040 protocol" in text or "60-40" in text:
            reply = self._handle_apply_6040_protocol()
        elif "export" in text and "csv" in text:
            reply = self._handle_export_to_csv()
        elif "anomaly" in text or "anomalies" in text:
            reply = self._handle_detect_anomalies()
        elif "chart" in text or "plot" in text:
            reply = self._handle_plot_daily_spend_chart()
        elif "analysis" in text or "report" in text:
            reply = self._handle_llm_analysis() 
        else:
            reply = (
                "I can help you with:\n"
                "- `Add transaction: <amount>, for <app> on <YYYY-MM-DD>`\n"
                "- `show total spend`\n"
                "- `show spend per service`\n"
                "- `apply 60-40 protocol`\n"
                "- `export in csv`\n"
                "-`run financial anomaly analysis`\n"
                "-`show live chart of trends`\n"
                "- `give analsyis report of money spent`"
            )
        return ChatResponse(reply=reply)
    
#intent handlers
    def _handle_add_transaction(self, message: str) -> str:
        pattern = (
            r"add transaction:?\s*([0-9]+(\.[0-9]+)?)\s+for\s+([a-zA-Z0-9_\-\s]+?)"
            r"(?:\s+on\s+([0-9\-]+))?$"
        )

        match = re.search(pattern, message, flags=re.IGNORECASE)
        if not match:
            return (
                "I could not parse the that transaction. Try e.g.:\n"
                "`add transaction: 29.99 for Slack on 2025-10-05`"
            )
        
        amount_str = match.group(1)
        service_name = match.group(3).strip()
        date_str = match.group(4)

        amount = float(amount_str)
        if date_str:
            try:
                timestamp = datetime.fromisoformat(date_str)
            except ValueError:
                timestamp = datetime.now()
            else:
                timestamp = datetime.now()

            txn = Transaction(
                id=0,
                service_name=service_name,
                amount=amount,
                timestamp=timestamp,
                currency="USD"
            )

            saved = self.repo.add_transaction(txn)
            return (
                f"Recorded transaction #{saved.id}: {saved.amount:.2f} {saved.currency}"
                f" for {saved.service_name} at {saved.timestamp.isoformat()}."

            )
    def _handle_total_spend(self) -> str:
        summary = compute_fin_summary(self.repo.transactions)
        return (
            f"Total spend: {summary.total_spend:.2f} {summary.currency}"
            f"across {len(self.repo.transactions)} transactions."
        )
    
    def _handle_spend_per_app(self) -> str:
        summary = compute_fin_summary(self.repo.transactions)
        if not summary.per_service:
            return "No transactions yet."
        lines = [
            f"- {app}: {amount:.2f} {summary.currency}" #type:ignore
            for app, amount in sorted(
                summary.per_service.items(), key=lambda kv: kv[1], reverse=True
            )
        ]
        return "Spend per service:\n" + "\n".join(lines)
    
    def _handle_apply_6040_protocol(self) -> str:
        summary = compute_fin_summary(self.repo.transactions)
        spend, save = apply_6040_protocol(summary.total_spend)
        return(
            f"Total spend is {summary.total_spend:.2f} {summary.currency}.\n"
            f"Applying a 60/40 rule:\n"
            f"- 60% operational: {spend:.2f} {summary.currency}\n"
            f"- 40% saving / efficiency target: {save:.2f} {summary.currency}"
        )

    def _handle_export_to_csv(self) -> str:
        path = export_to_csv(self.repo.transactions, "transactions_export.csv")
        return f"Exported {len(self.repo.transactions)} transactions to `{path}`."

    def _handle_plot_daily_spend_chart(self) -> str:
        path = plot_daily_spend_chart(self.repo.transactions, "daily_spend.png")
        if not path:
            return "No data available to plot trends."
        return (
            f"Generated a daily spend trend chart at `{path}`.\n"
            "You can open the PNG to visually inspect trends and anomalies."
        )

    def _handle_detect_anomalies(self) -> str:
        base_result = detect_anomalies(self.repo.transactions)
        if not base_result.anomalies:
            return base_result.details
        
        #slm action--> refine anomaly scores
        run_untrusted_slm ="""
    scores = [abs(t.amount) for t in transactions]
    threshold = max(scores) * 0.8 if scores else 0
    flags = [s >= threshold for s in scores]
    result = {'scores': scores, 'flags': flags}
    """

        context = {"transactions": base_result.anomalies}
        slm_locals = run_untrusted_slm()