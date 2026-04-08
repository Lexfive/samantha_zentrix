"""
Testes de integração para o CRUD de transações.
Roda com: pytest tests/

Os models são registrados no Base via conftest.py na raiz do projeto.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.connection import Base, get_db
from main import app

# ── Banco em memória exclusivo para testes ─────────────────────────────────────
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Fixtures ───────────────────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def client():
    """Recria o banco a cada teste — isolamento garantido."""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    """Registra e loga um usuário, retorna o header Authorization pronto."""
    client.post("/users/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "senha123",
    })
    r = client.post("/users/login", json={
        "username": "testuser",
        "password": "senha123",
    })
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ── Testes de health ───────────────────────────────────────────────────────────
def test_health(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


# ── Testes de auth ─────────────────────────────────────────────────────────────
def test_register_user(client):
    r = client.post("/users/register", json={
        "username": "lexfive",
        "email": "lex@zentrix.com",
        "password": "senha123",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["username"] == "lexfive"
    assert "password_hash" not in data  # nunca expõe hash


def test_register_duplicate_username(client):
    payload = {"username": "lex", "email": "a@b.com", "password": "senha123"}
    client.post("/users/register", json=payload)
    r = client.post("/users/register", json={**payload, "email": "outro@b.com"})
    assert r.status_code == 409


def test_login_success(client):
    client.post("/users/register", json={
        "username": "lex", "email": "a@b.com", "password": "senha123"
    })
    r = client.post("/users/login", json={"username": "lex", "password": "senha123"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password(client):
    client.post("/users/register", json={
        "username": "lex", "email": "a@b.com", "password": "senha123"
    })
    r = client.post("/users/login", json={"username": "lex", "password": "errada"})
    assert r.status_code == 401


def test_transactions_require_auth(client):
    """Sem token → 403."""
    r = client.get("/transactions")
    assert r.status_code == 403


# ── Testes de transações (autenticados) ───────────────────────────────────────
def test_create_and_list_transaction(client, auth_headers):
    payload = {"type": "income", "amount": 1000.0, "description": "Salário"}
    r = client.post("/transactions/", json=payload, headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    assert data["type"] == "income"
    assert data["amount"] == 1000.0

    r2 = client.get("/transactions/", headers=auth_headers)
    assert r2.status_code == 200
    assert len(r2.json()) == 1


def test_summary(client, auth_headers):
    client.post("/transactions/", json={"type": "income",  "amount": 2000, "description": "Salário"},  headers=auth_headers)
    client.post("/transactions/", json={"type": "expense", "amount": 500,  "description": "Mercado"}, headers=auth_headers)

    r = client.get("/transactions/summary", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert data["total_income"] == 2000
    assert data["total_expense"] == 500
    assert data["balance"] == 1500


def test_get_transaction_by_id(client, auth_headers):
    r = client.post("/transactions/", json={"type": "income", "amount": 100, "description": "Teste"}, headers=auth_headers)
    tid = r.json()["id"]
    r2 = client.get(f"/transactions/{tid}", headers=auth_headers)
    assert r2.status_code == 200
    assert r2.json()["id"] == tid


def test_get_transaction_404(client, auth_headers):
    r = client.get("/transactions/9999", headers=auth_headers)
    assert r.status_code == 404


def test_patch_transaction(client, auth_headers):
    r = client.post("/transactions/", json={"type": "income", "amount": 100, "description": "Teste"}, headers=auth_headers)
    tid = r.json()["id"]

    r2 = client.patch(f"/transactions/{tid}", json={"amount": 150, "description": "Atualizado"}, headers=auth_headers)
    assert r2.status_code == 200
    data = r2.json()
    assert data["amount"] == 150
    assert data["description"] == "Atualizado"


def test_delete_transaction(client, auth_headers):
    r = client.post("/transactions/", json={"type": "income", "amount": 100, "description": "Teste"}, headers=auth_headers)
    tid = r.json()["id"]

    r2 = client.delete(f"/transactions/{tid}", headers=auth_headers)
    assert r2.status_code == 204

    r3 = client.get(f"/transactions/{tid}", headers=auth_headers)
    assert r3.status_code == 404


def test_filter_by_type(client, auth_headers):
    client.post("/transactions/", json={"type": "income",  "amount": 100, "description": "Inc1"}, headers=auth_headers)
    client.post("/transactions/", json={"type": "income",  "amount": 200, "description": "Inc2"}, headers=auth_headers)
    client.post("/transactions/", json={"type": "expense", "amount": 50,  "description": "Exp1"}, headers=auth_headers)

    r = client.get("/transactions/?type=income", headers=auth_headers)
    assert r.status_code == 200
    assert all(t["type"] == "income" for t in r.json())

    r2 = client.get("/transactions/?type=expense", headers=auth_headers)
    assert r2.status_code == 200
    assert all(t["type"] == "expense" for t in r2.json())
