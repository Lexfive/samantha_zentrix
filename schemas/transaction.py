from pydantic import BaseModel

class TransactionBase(BaseModel):
    description: str
    amount: float

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic V2