import secrets

# ──────────────────────────────────────────────
# JWT
# ──────────────────────────────────────────────
# Em produção: substitua por uma string fixa e guarde em variável de ambiente
SECRET_KEY: str = secrets.token_hex(32)
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas — ajuste conforme necessário
