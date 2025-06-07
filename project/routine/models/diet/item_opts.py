from datetime import time

from sqlalchemy import Integer, ForeignKey, Float, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base

class ItemOpts(Base):
    __tablename__ = 'item_opts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey('routine_items.id'), nullable=False)
    ref_time: Mapped[time] = mapped_column(Time, nullable=False)
    goal: Mapped[str] = mapped_column(String(100), nullable=True)
    total_calories: Mapped[float] = mapped_column(Float, nullable=True)
    total_protein: Mapped[float] = mapped_column(Float, nullable=True)
    total_fat: Mapped[float] = mapped_column(Float, nullable=True)
    total_carbs: Mapped[float] = mapped_column(Float, nullable=True)

    item: Mapped['RoutineItem'] = relationship(
        'RoutineItem', back_populates='opts', foreign_keys=[item_id]
    )
    opt_foods: Mapped[list['OptFoods']] = relationship(
        'OptFoods', back_populates='opt', foreign_keys='[OptFoods.opt_id]', cascade='all, delete-orphan'
    )
