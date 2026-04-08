from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.connection import init_db
import models.transaction  # noqa: F401 — garante que o model é registrado no Base antes do init_db
from routes import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # cria as tabelas ao iniciar
    yield


app = FastAPI(
    title="API Base",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router)
