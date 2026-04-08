from fastapi import FastAPI
from database.connection import init_db
from routes.transactions import router as transactions_router

app = FastAPI()

# Inicializa o DB
init_db()

# Inclui rotas
app.include_router(transactions_router, prefix="/transactions")