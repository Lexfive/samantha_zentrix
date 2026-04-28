from datetime import date
from decimal import Decimal
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from auth.jwt import get_current_user
from database.connection import get_db
from models.category import Category
from models.transaction import Transaction
from models.user import User
from schemas.transaction import (
    BalanceResponse,
    SummaryResponse,
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def _get_or_404(transaction_id: int, user: User, db: Session) -> Transaction:
    """Busca a transação garantindo que pertence ao usuário autenticado."""
    tx = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id, Transaction.user_id == user.id)
        .first()
    )
    if not tx:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Transação não encontrada")
    return tx


def _base_query(user: User, db: Session):
    """Query base sempre filtrada pelo user_id — nunca vaza dados."""
    return db.query(Transaction).filter(Transaction.user_id == user.id)


# ── CREATE ─────────────────────────────────────────────────────────────────────

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Transaction:
    if payload.category_id is not None:
        cat = (
            db.query(Category)
            .filter(Category.id == payload.category_id, Category.user_id == current_user.id)
            .first()
        )
        if not cat:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Categoria não encontrada")

    tx = Transaction(
        **payload.model_dump(),
        user_id=current_user.id,  # SEMPRE do JWT, nunca do payload
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


# ── LIST ───────────────────────────────────────────────────────────────────────

@router.get("/", response_model=list[TransactionResponse])
def list_transactions(
    type:        Optional[Literal["income", "expense"]] = Query(default=None),
    category_id: Optional[int]  = Query(default=None),
    start:       Optional[date] = Query(default=None, description="YYYY-MM-DD"),
    end:         Optional[date] = Query(default=None, description="YYYY-MM-DD"),
    limit:       int = Query(default=50, ge=1, le=200),
    offset:      int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Transaction]:
    q = _base_query(current_user, db)

    if type is not None:
        q = q.filter(Transaction.type == type)
    if category_id is not None:
        q = q.filter(Transaction.category_id == category_id)
    if start is not None:
        q = q.filter(Transaction.created_at >= start)
    if end is not None:
        q = q.filter(Transaction.created_at < end)

    return q.order_by(Transaction.created_at.desc()).offset(offset).limit(limit).all()


# ── BALANCE ────────────────────────────────────────────────────────────────────

@router.get("/balance", response_model=BalanceResponse)
def get_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BalanceResponse:
    """Calcula o saldo do usuário autenticado no backend — nunca confia no frontend."""

    def _sum(type_: str) -> Decimal:
        result = (
            db.query(func.coalesce(func.sum(Transaction.amount), 0))
            .filter(Transaction.user_id == current_user.id, Transaction.type == type_)
            .scalar()
        )
        return Decimal(str(result))

    income  = _sum("income")
    expense = _sum("expense")

    return BalanceResponse(
        total_income=income,
        total_expense=expense,
        balance=income - expense,
    )


# ── SUMMARY POR CATEGORIA ──────────────────────────────────────────────────────

@router.get("/summary", response_model=SummaryResponse)
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SummaryResponse:
    def _sum(type_: str) -> Decimal:
        result = (
            db.query(func.coalesce(func.sum(Transaction.amount), 0))
            .filter(Transaction.user_id == current_user.id, Transaction.type == type_)
            .scalar()
        )
        return Decimal(str(result))

    income  = _sum("income")
    expense = _sum("expense")

    by_category_rows = (
        db.query(
            Category.name,
            func.coalesce(func.sum(Transaction.amount), 0).label("total"),
        )
        .join(Transaction, Transaction.category_id == Category.id, isouter=True)
        .filter(Category.user_id == current_user.id)
        .group_by(Category.id, Category.name)
        .all()
    )

    return SummaryResponse(
        total_income=income,
        total_expense=expense,
        balance=income - expense,
        by_category=[
            {"category_name": row.name, "total": Decimal(str(row.total))}
            for row in by_category_rows
        ],
    )


# ── GET ONE ────────────────────────────────────────────────────────────────────

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Transaction:
    return _get_or_404(transaction_id, current_user, db)


# ── UPDATE ─────────────────────────────────────────────────────────────────────

@router.patch("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    payload: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Transaction:
    tx = _get_or_404(transaction_id, current_user, db)

    if payload.category_id is not None:
        cat = (
            db.query(Category)
            .filter(Category.id == payload.category_id, Category.user_id == current_user.id)
            .first()
        )
        if not cat:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Categoria não encontrada")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(tx, field, value)

    db.commit()
    db.refresh(tx)
    return tx


# ── DELETE ─────────────────────────────────────────────────────────────────────

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    tx = _get_or_404(transaction_id, current_user, db)
    db.delete(tx)
    db.commit()
