# schemas/user.py
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String
from database.connection import Base


# =====================
# SQLALCHEMY MODEL
# =====================
class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}  # evita erro de tabela duplicada
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"


# =====================
# Pydantic SCHEMAS
# =====================

# Request para login
class LoginRequest(BaseModel):
    username: str
    password: str

    model_config = {
        "from_attributes": True
    }


# Resposta do token
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = {
        "from_attributes": True
    }


# Criação de usuário
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    model_config = {
        "from_attributes": True
    }


# Retorno de usuário
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }