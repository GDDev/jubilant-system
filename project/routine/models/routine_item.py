from enum import Enum

from datetime import datetime

from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class ItemType(str, Enum):
    EXERCISE_ITEM = 'exercise_item'
    MEAL_OPT_ITEM = 'meal_opt_item'


class RoutineItem(Base):
    __tablename__ = 'routine_items'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    routine_id: Mapped[int] = mapped_column(Integer, ForeignKey('routines.id'))
    type: Mapped[ItemType] = mapped_column('ItemType')
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    last_updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    expiration_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)

    __mapper_args__ = {
        'polymorphic_on': type
    }

    routine: Mapped['Routine'] = relationship('Routine', back_populates='routine_items', foreign_keys=[routine_id])
