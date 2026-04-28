"""
Testes de integração — isolamento de dados por usuário.
Roda com: SECRET_KEY=test pytest tests/
"""
import os
os.environ.setdefault("SECRET_KEY", "test-secret-key-only-for-tests-32chars!!")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# imports de models ANTES do main para registrá-los no Base
import models.user       # noqa: F401
import models.category   # noqa: F401
import models.transaction  # noqa: F401

from database.connection import Base, get_db
from main import app

TEST_DB = "sqlite:///:memory:"
test_engine = create_engine(TEST_DB, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    Base.metadata.create_all(bind=test_engine)
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=False)
def client():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()


def _register_and_login(client, username: str, email: str) -> dict:
    client.post("/auth/register", json={"username": username, "email": email, "password": "senha123"})
    r = client.post("/auth/login", json={"username": username, "password": "senha123"})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ── Health ─────────────────────────────────────────────────────────────────────

def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


# ── Auth ───────────────────────────────────────────────────────────────────────

def test_register_success(client):
    r = client.post("/auth/register", json={"username": "lex", "email": "lex@z.com", "password": "senha123"})
    assert r.status_code == 201
    assert "password_hash" not in r.json()


def test_register_duplicate(client):
    payload = {"username": "lex", "email": "lex@z.com", "password": "senha123"}
    client.post("/auth/register", json=payload)
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 409


def test_login_success(client):
    client.post("/auth/register", json={"username": "lex", "email": "a@b.com", "password": "senha123"})
    r = client.post("/auth/login", json={"username": "lex", "password": "senha123"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"username": "lex", "email": "a@b.com", "password": "senha123"})
    r = client.post("/auth/login", json={"username": "lex", "password": "errada"})
    assert r.status_code == 401


# ── Transactions ───────────────────────────────────────────────────────────────

def test_create_and_list(client):
    headers = _register_and_login(client, "user1", "u1@z.com")
    r = client.post("/transactions/", json={"type": "income", "amount": "1500.00", "description": "Salário"}, headers=headers)
    assert r.status_code == 201
    data = r.json()
    assert data["amount"] == "1500.00"
    assert "user_id" in data

    r2 = client.get("/transactions/", headers=headers)
    assert len(r2.json()) == 1


def test_isolation_between_users(client):
    """CRÍTICO: Usuário B não pode ver transações do Usuário A."""
    h1 = _register_and_login(client, "user1", "u1@z.com")
    h2 = _register_and_login(client, "user2", "u2@z.com")

    client.post("/transactions/", json={"type": "income", "amount": "5000", "description": "Salário A"}, headers=h1)
    client.post("/transactions/", json={"type": "expense", "amount": "200", "description": "Compra A"}, headers=h1)

    r_user2 = client.get("/transactions/", headers=h2)
    assert r_user2.json() == [], "Usuário B não deve ver dados do Usuário A"


def test_cannot_access_other_users_transaction(client):
    """Usuário B não pode acessar transação específica do Usuário A via ID."""
    h1 = _register_and_login(client, "user1", "u1@z.com")
    h2 = _register_and_login(client, "user2", "u2@z.com")

    r = client.post("/transactions/", json={"type": "income", "amount": "100", "description": "Privado"}, headers=h1)
    tx_id = r.json()["id"]

    r_b = client.get(f"/transactions/{tx_id}", headers=h2)
    assert r_b.status_code == 404, "Usuário B deve receber 404, não os dados do Usuário A"


def test_cannot_delete_other_users_transaction(client):
    h1 = _register_and_login(client, "user1", "u1@z.com")
    h2 = _register_and_login(client, "user2", "u2@z.com")

    r = client.post("/transactions/", json={"type": "income", "amount": "100", "description": "Privado"}, headers=h1)
    tx_id = r.json()["id"]

    r_del = client.delete(f"/transactions/{tx_id}", headers=h2)
    assert r_del.status_code == 404

    r_check = client.get(f"/transactions/{tx_id}", headers=h1)
    assert r_check.status_code == 200, "Transação deve ainda existir para o dono"


# ── Balance ────────────────────────────────────────────────────────────────────

def test_balance_correct(client):
    headers = _register_and_login(client, "user1", "u1@z.com")
    client.post("/transactions/", json={"type": "income",  "amount": "3000", "description": "Salário"}, headers=headers)
    client.post("/transactions/", json={"type": "expense", "amount": "800",  "description": "Aluguel"}, headers=headers)
    client.post("/transactions/", json={"type": "expense", "amount": "200",  "description": "Mercado"}, headers=headers)

    r = client.get("/transactions/balance", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["total_income"]  == "3000.00"
    assert data["total_expense"] == "1000.00"
    assert data["balance"]       == "2000.00"


def test_balance_isolated(client):
    """Saldo de cada usuário é calculado independentemente."""
    h1 = _register_and_login(client, "user1", "u1@z.com")
    h2 = _register_and_login(client, "user2", "u2@z.com")

    client.post("/transactions/", json={"type": "income", "amount": "9999", "description": "Renda"}, headers=h1)

    r2 = client.get("/transactions/balance", headers=h2)
    assert r2.json()["balance"] == "0.00", "Saldo do Usuário B não deve ser afetado por dados do Usuário A"


# ── Categorias ─────────────────────────────────────────────────────────────────

def test_category_isolation(client):
    h1 = _register_and_login(client, "user1", "u1@z.com")
    h2 = _register_and_login(client, "user2", "u2@z.com")

    client.post("/categories/", json={"name": "Lazer", "color": "#ff0000"}, headers=h1)
    r2 = client.get("/categories/", headers=h2)
    assert r2.json() == [], "Usuário B não deve ver categorias do Usuário A"


def test_transaction_with_category(client):
    headers = _register_and_login(client, "user1", "u1@z.com")
    r_cat = client.post("/categories/", json={"name": "Alimentação", "color": "#00ff00"}, headers=headers)
    cat_id = r_cat.json()["id"]

    r_tx = client.post("/transactions/", json={
        "type": "expense", "amount": "150", "description": "Supermercado", "category_id": cat_id
    }, headers=headers)
    assert r_tx.status_code == 201
    assert r_tx.json()["category_id"] == cat_id


def test_cannot_use_other_users_category(client):
    """Usuário B não pode criar transação usando categoria do Usuário A."""
    h1 = _register_and_login(client, "user1", "u1@z.com")
    h2 = _register_and_login(client, "user2", "u2@z.com")

    r_cat = client.post("/categories/", json={"name": "Privada", "color": "#0000ff"}, headers=h1)
    cat_id = r_cat.json()["id"]

    r_tx = client.post("/transactions/", json={
        "type": "expense", "amount": "100", "description": "Tentativa", "category_id": cat_id
    }, headers=h2)
    assert r_tx.status_code == 404, "Não deve aceitar categoria de outro usuário"


# ── Filtros + paginação ────────────────────────────────────────────────────────

def test_filter_by_type(client):
    headers = _register_and_login(client, "user1", "u1@z.com")
    client.post("/transactions/", json={"type": "income",  "amount": "100", "description": "A"}, headers=headers)
    client.post("/transactions/", json={"type": "expense", "amount": "50",  "description": "B"}, headers=headers)

    r = client.get("/transactions/?type=income", headers=headers)
    assert all(t["type"] == "income" for t in r.json())


def test_pagination(client):
    headers = _register_and_login(client, "user1", "u1@z.com")
    for i in range(5):
        client.post("/transactions/", json={"type": "income", "amount": "10", "description": f"Tx{i}"}, headers=headers)

    r = client.get("/transactions/?limit=2&offset=0", headers=headers)
    assert len(r.json()) == 2

    r2 = client.get("/transactions/?limit=2&offset=2", headers=headers)
    assert len(r2.json()) == 2


# ── Sem token ──────────────────────────────────────────────────────────────────

def test_requires_auth(client):
    # HTTPBearer sem header retorna 403 (no credentials) ou 401 (credencial inválida)
    r1 = client.get("/transactions/")
    assert r1.status_code in (401, 403)
    r2 = client.get("/transactions/balance")
    assert r2.status_code in (401, 403)
    r3 = client.get("/categories/")
    assert r3.status_code in (401, 403)
