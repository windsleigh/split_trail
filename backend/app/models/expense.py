from sqlalchemy import Column, String, DateTime, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import CHAR
from app.database import Base
from datetime import datetime, timezone
import uuid

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    group_id = Column(CHAR(36), ForeignKey("groups.id"), nullable=False)
    paid_by = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(String(255), nullable=False)
    split_type = Column(String(20), default="equal")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    group = relationship("Group", back_populates="expenses")
    paid_by_user = relationship("User", back_populates="expenses_paid")
    splits = relationship("ExpenseSplit", back_populates="expense")

class ExpenseSplit(Base):
    __tablename__ = "expense_splits"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    expense_id = Column(CHAR(36), ForeignKey("expenses.id"), nullable=False)
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    owed_amount = Column(Numeric(10, 2), nullable=False)
    is_settled = Column(Boolean, default=False)

    expense = relationship("Expense", back_populates="splits")
    user = relationship("User", back_populates="expense_splits")