from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import CHAR
from app.database import Base
from datetime import datetime, timezone
import uuid

class Group(Base):
    __tablename__ = "groups"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    currency = Column(String(10), default="USD")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    members = relationship("GroupMember", back_populates="group")
    expenses = relationship("Expense", back_populates="group")

class GroupMember(Base):
    __tablename__ = "group_members"

    group_id = Column(CHAR(36), ForeignKey("groups.id"), primary_key=True)
    user_id = Column(CHAR(36), ForeignKey("users.id"), primary_key=True)
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    group = relationship("Group", back_populates="members")
    user = relationship("User", back_populates="group_memberships")