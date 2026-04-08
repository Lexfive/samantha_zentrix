from fastapi import APIRouter, Depends, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.connection import get_db
from models.transaction import Transaction
from schemas.transaction import TransactionCreate, TransactionResponse, SummaryResponse

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)):
    transaction = Transaction(**payload.model_dump())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.get("/summary", response_model=SummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    def sum_by_type(type_: str) -> float:
        result = (
            db.query(func.coalesce(func.sum(Transaction.amount), 0.0))
            .filter(Transaction.type == type_)
            .scalar()
        )
        return float(result)

    total_income = sum_by_type("income")
    total_expense = sum_by_type("expense")

    return SummaryResponse(
        total_income=total_income,
        total_expense=total_expense,
        balance=round(total_income - total_expense, 2),
    )


@router.get("/", response_model=list[TransactionResponse])
def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).order_by(Transaction.created_at.desc()).all()
