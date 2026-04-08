from models.transaction import Base
from database import engine

# Cria todas as tabelas
Base.metadata.create_all(bind=engine)