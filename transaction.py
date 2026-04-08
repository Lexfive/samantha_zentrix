from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    type: Literal["income", "expense"]
    amount: float = Field(gt=0)
    description: str = Field(min_length=1)


class TransactionResponse(BaseModel):
    id: int
    type: str
    amount: float
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}  # permite criar a partir de objetos SQLAlchemy
