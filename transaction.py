from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String

from database.connection import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)          # "income" | "expense"
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Transaction id={self.id} type={self.type} amount={self.amount}>"
