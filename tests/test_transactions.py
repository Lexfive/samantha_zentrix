import pytest
from fastapi.testclient import TestClient
from main import app
from database.connection import Base, engine, get_db
from sqlalchemy.orm import sessionmaker

# Cria session para testes
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Fixture para limpar DB antes de cada teste
@pytest.fixture(scope="function")
def client():
    # Cria tabelas fresh
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c

def test_health(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_and_list_transaction(client):
    payload = {"type": "income", "amount": 1000.0, "description": "Salário"}
    r = client.post("/transactions", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["type"] == "income"
    assert data["amount"] == 1000.0
    assert data["description"] == "Salário"

    r2 = client.get("/transactions")
    assert r2.status_code == 200
    assert len(r2.json()) == 1

def test_summary(client):
    client.post("/transactions", json={"type": "income", "amount": 2000, "description": "Salário"})
    client.post("/transactions", json={"type": "expense", "amount": 500, "description": "Mercado"})
    r = client.get("/transactions/summary")
    assert r.status_code == 200
    data = r.json()
    assert data["total_income"] == 2000
    assert data["total_expense"] == 500
    assert data["balance"] == 1500

def test_get_transaction_by_id(client):
    r = client.post("/transactions", json={"type": "income", "amount": 100, "description": "Teste"})
    tid = r.json()["id"]
    r2 = client.get(f"/transactions/{tid}")
    assert r2.status_code == 200
    assert r2.json()["id"] == tid

def test_get_transaction_404(client):
    r = client.get("/transactions/9999")
    assert r.status_code == 404

def test_patch_transaction(client):
    r = client.post("/transactions", json={"type": "income", "amount": 100, "description": "Teste"})
    tid = r.json()["id"]
    patch_payload = {"amount": 150, "description": "Atualizado"}
    r2 = client.patch(f"/transactions/{tid}", json=patch_payload)
    assert r2.status_code == 200
    data = r2.json()
    assert data["amount"] == 150
    assert data["description"] == "Atualizado"

def test_delete_transaction(client):
    r = client.post("/transactions", json={"type": "income", "amount": 100, "description": "Teste"})
    tid = r.json()["id"]
    r2 = client.delete(f"/transactions/{tid}")
    assert r2.status_code == 204
    r3 = client.get(f"/transactions/{tid}")
    assert r3.status_code == 404

def test_filters(client):
    # cria transações
    client.post("/transactions", json={"type": "income", "amount": 100, "description": "Inc1"})
    client.post("/transactions", json={"type": "income", "amount": 200, "description": "Inc2"})
    client.post("/transactions", json={"type": "expense", "amount": 50, "description": "Exp1"})

    # filtro type=income
    r = client.get("/transactions?type=income")
    assert r.status_code == 200
    data = r.json()
    assert all(t["type"] == "income" for t in data)

    # filtro type=expense
    r2 = client.get("/transactions?type=expense")
    assert r2.status_code == 200
    data = r2.json()
    assert all(t["type"] == "expense" for t in data)
