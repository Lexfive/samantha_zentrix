from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    type: Literal["income", "expense"]
    amount: float = Field(gt=0)
    description: str = Field(min_length=1)


class TransactionUpdate(BaseModel):
    type: Optional[Literal["income", "expense"]] = None
    amount: Optional[float] = Field(default=None, gt=0)
    description: Optional[str] = Field(default=None, min_length=1)


class SummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    balance: float


class TransactionResponse(BaseModel):
    id: int
    type: str
    amount: float
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}
