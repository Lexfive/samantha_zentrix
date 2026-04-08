from fastapi import APIRouter
from database.connection import SessionLocal
from models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def list_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users