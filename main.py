from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.connection import init_db
import models.transaction  # noqa: F401
import models.user         # noqa: F401 — ambos precisam estar importados antes do init_db
from routes import health, transactions, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # cria tabelas: transactions + users
    yield


app = FastAPI(
    title="Samantha Zentrix API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(transactions.router)
