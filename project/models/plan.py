from datetime import datetime
import uuid

from sqlalchemy import Integer, String, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base

class Plan(Base):
    __tablename__ = 'plans'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    created_for: Mapped[str] = mapped_column(String(36), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    approved_by: Mapped[str] = mapped_column(String(36), nullable=True)
    approved_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)

    plan_items: Mapped[list['PlanItem']] = relationship('PlanItem', back_populates='plan')
