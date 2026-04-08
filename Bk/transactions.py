from datetime import date
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.connection import get_db
from models.transaction import Transaction
from schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
    SummaryResponse,
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def get_transaction_or_404(id: int, db: Session) -> Transaction:
    transaction = db.query(Transaction).filter(Transaction.id == id).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction


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
def list_transactions(
    type: Optional[Literal["income", "expense"]] = Query(default=None),
    start: Optional[date] = Query(default=None, description="Formato: YYYY-MM-DD"),
    end: Optional[date] = Query(default=None, description="Formato: YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    query = db.query(Transaction)

    if type is not None:
        query = query.filter(Transaction.type == type)
    if start is not None:
        query = query.filter(Transaction.created_at >= start)
    if end is not None:
        query = query.filter(Transaction.created_at < end)

    return query.order_by(Transaction.created_at.desc()).all()


@router.get("/{id}", response_model=TransactionResponse)
def get_transaction(id: int, db: Session = Depends(get_db)):
    return get_transaction_or_404(id, db)


@router.patch("/{id}", response_model=TransactionResponse)
def update_transaction(id: int, payload: TransactionUpdate, db: Session = Depends(get_db)):
    transaction = get_transaction_or_404(id, db)

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)
    return transaction


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(id: int, db: Session = Depends(get_db)):
    transaction = get_transaction_or_404(id, db)
    db.delete(transaction)
    db.commit()
