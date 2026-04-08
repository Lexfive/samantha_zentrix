from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models.transaction import Transaction, Base
from schemas.transaction import TransactionCreate, TransactionResponse

app = FastAPI()

# Inicializa o banco
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Criar transação
@app.post("/transactions/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_trx = Transaction(**transaction.dict())
    db.add(db_trx)
    db.commit()
    db.refresh(db_trx)
    return db_trx

# Listar todas
@app.get("/transactions/", response_model=list[TransactionResponse])
def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()