from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from models.transaction import Transaction
from schemas.transaction import TransactionCreate, TransactionRead

router = APIRouter()

# CREATE
@router.post("/", response_model=TransactionRead)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# READ ONE
@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

# READ ALL
@router.get("/", response_model=List[TransactionRead])
def list_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).offset(skip).limit(limit).all()
    return transactions

# UPDATE
@router.put("/{transaction_id}", response_model=TransactionRead)
def update_transaction(transaction_id: int, updated: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in updated.dict().items():
        setattr(db_transaction, key, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# DELETE
@router.delete("/{transaction_id}", response_model=dict)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}
    
    from sqlalchemy import func

# RELATÓRIOS
@router.get("/reports/summary", response_model=dict)
def transaction_summary(db: Session = Depends(get_db)):
    total = db.query(func.sum(Transaction.amount)).scalar() or 0
    count = db.query(func.count(Transaction.id)).scalar() or 0
    average = db.query(func.avg(Transaction.amount)).scalar() or 0
    maximum = db.query(func.max(Transaction.amount)).scalar() or 0
    minimum = db.query(func.min(Transaction.amount)).scalar() or 0

    return {
        "total_transactions": count,
        "total_amount": total,
        "average_amount": average,
        "maximum_amount": maximum,
        "minimum_amount": minimum
    }