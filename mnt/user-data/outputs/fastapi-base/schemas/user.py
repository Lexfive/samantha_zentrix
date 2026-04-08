from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Payload para registro de novo usuário."""
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)


class UserResponse(BaseModel):
    """Dados públicos do usuário — nunca expõe password_hash."""
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    """Payload para login."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Resposta do login com o JWT."""
    access_token: str
    token_type: str = "bearer"
