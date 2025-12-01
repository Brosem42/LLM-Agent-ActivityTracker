from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator  # type: ignore


class Transaction(BaseModel):
    id:int
    app_name: str = Field(..., description="Name of SaaS App or service used.")
    amount: float = Field(..., description="Amount spent on the SaaS App or service (must be positive number)")
    currency: str = Field(default="USD")
    timestamp: datetime = Field(default_factory= datetime.utcnow, description="When transaction occurred")
    category: Optional[str] = Field(default=None, description="Miscellaneous spending category--infra, marketing")

    @validator("amount")
    def amount_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError("transaction amount must be positive")
        return v
    

#request for chat message
class ChatRequest(BaseModel):
    message: str

#reponse for chat message
class ChatResponse(BaseModel):
    reply: str

class FinancialSummary(BaseModel):
    total_spend: float
    per_microservice: dict
    currency: str = "USD"

class AnomalyResultj(BaseModel):
    anomalies: List[Transaction]
    details: str

