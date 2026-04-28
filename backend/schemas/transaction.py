from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    type:        Literal["income", "expense"]
    amount:      Decimal = Field(gt=0, decimal_places=2)
    description: str     = Field(min_length=1, max_length=255)
    category_id: Optional[int] = None
    # user_id NUNCA vem do frontend — sempre extraído do JWT


class TransactionUpdate(BaseModel):
    type:        Optional[Literal["income", "expense"]] = None
    amount:      Optional[Decimal] = Field(default=None, gt=0, decimal_places=2)
    description: Optional[str]    = Field(default=None, min_length=1, max_length=255)
    category_id: Optional[int]    = None


class TransactionResponse(BaseModel):
    id:          int
    user_id:     int
    type:        str
    amount:      Decimal
    description: str
    category_id: Optional[int]
    created_at:  datetime

    model_config = {"from_attributes": True}


class BalanceResponse(BaseModel):
    total_income:  Decimal
    total_expense: Decimal
    balance:       Decimal


class SummaryResponse(BaseModel):
    total_income:  Decimal
    total_expense: Decimal
    balance:       Decimal
    by_category:   list[dict]  # [{category_name, total}]
