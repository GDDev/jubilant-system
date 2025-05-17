from enum import Enum

from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class RoutineEnum(str, Enum):
    WORKOUT = "workout"
    DIETARY = "dietary"


class RoutineStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Routine(Base):
    __tablename__ = 'routines'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_by: Mapped[str] = mapped_column(String(36), ForeignKey('profiles.id'), nullable=False)
    status: Mapped[RoutineStatus] = mapped_column('RoutineStatus', nullable=False, default=RoutineStatus.PENDING)
    created_for: Mapped[str] = mapped_column(String(36), ForeignKey('profiles.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    approved_by: Mapped[str] = mapped_column(String(36), nullable=True)
    approved_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    type: Mapped[RoutineEnum] = mapped_column('RoutineEnum', nullable=False)


    creator: Mapped['UserProfile'] = relationship('UserProfile', back_populates='created_routines', foreign_keys=[created_by])
    receiver: Mapped['UserProfile'] = relationship('UserProfile', back_populates='routines', foreign_keys=[created_for])
    routine_items: Mapped[list['RoutineItem']] = relationship('RoutineItem', back_populates='routine', cascade='all, delete-orphan')
