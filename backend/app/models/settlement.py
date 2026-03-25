from sqlalchemy import Column, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from app.database import Base
from datetime import datetime, timezone
import uuid

class Settlement(Base):
    __tablename__ = "settlements"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    group_id = Column(CHAR(36), ForeignKey("groups.id"), nullable=False)
    payer_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    payee_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    settled_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))