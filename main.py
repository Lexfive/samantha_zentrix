from fastapi import FastAPI
from routes import health

app = FastAPI(
    title="API Base",
    version="0.1.0",
)

app.include_router(health.router)
