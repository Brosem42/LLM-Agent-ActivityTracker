from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator  # type: ignore


class Transactions(BaseModel):
    id:int
    app_name: str = Field(..., description="Name of SaaS App or service used.")
    amount: float = Field(..., description="Amount spent on the SaaS App or service (must be positive number)")
    currency: str = Field(default="USD")
    timestamp: datetime = Field(default_factory= datetime.utcnow, description="When transaction occurred")
    category: Optional[str] = Field(default=None, description="Miscellaneous spending category--infra, marketing")
    