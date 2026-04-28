from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.connection import Base


class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    username      = Column(String(50), unique=True, nullable=False, index=True)
    email         = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    transactions  = relationship("Transaction", back_populates="user", lazy="dynamic")
    categories    = relationship("Category", back_populates="user", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"
