from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.connection import Base


class Category(Base):
    __tablename__ = "categories"

    id      = Column(Integer, primary_key=True, autoincrement=True)
    name    = Column(String(100), nullable=False)
    color   = Column(String(7), nullable=False, default="#6366f1")  # hex
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    user         = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name!r} user_id={self.user_id}>"
