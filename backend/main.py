from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connection import init_db

import models.user         # noqa: F401
import models.category     # noqa: F401
import models.transaction  # noqa: F401

from routes import auth, categories, transactions


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Zentrix API",
    version="2.0.0",
    lifespan=lifespan,
)

# 🔥 CORS corrigido (isso aqui estava quebrado)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # pode deixar assim em dev/prod inicial
        "https://samantha-zentrix.vercel.app",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)


# Health check raiz
@app.get("/", tags=["Health"])
def health() -> dict:
    return {
        "status": "ok",
        "version": app.version
    }


# Endpoint opcional mais explícito
@app.get("/health", tags=["Health"])
def health_check() -> dict:
    return {
        "status": "ok",
        "version": app.version
    }
