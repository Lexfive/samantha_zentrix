from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"  # troca pro seu DB real se precisar

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # só para SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    import models.transaction  # importa todos os models antes de criar as tabelas
    Base.metadata.create_all(bind=engine)