from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# ========================
# Base model para criar
# ========================
class TransactionBase(BaseModel):
    amount: float
    description: str
    type: str  # "income" ou "expense"

# ========================
# Para criação de transações
# ========================
class TransactionCreate(TransactionBase):
    pass

# ========================
# Para atualizar transações
# ========================
class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    type: Optional[str] = None

# ========================
# Para resposta de cada transação
# ========================
class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# ========================
# Resumo de transações
# ========================
class SummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    balance: float