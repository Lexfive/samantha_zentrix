# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"  # simples pra testes

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # necessário pro SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)