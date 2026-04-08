from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from models.transaction import Transaction
from schemas.transaction import TransactionCreate, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)):
    transaction = Transaction(**payload.model_dump())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.get("/", response_model=list[TransactionResponse])
def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).order_by(Transaction.created_at.desc()).all()
