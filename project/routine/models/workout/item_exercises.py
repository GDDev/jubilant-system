from datetime import time

from sqlalchemy import Integer, ForeignKey, Float, Time
from sqlalchemy.orm import Mapped, relationship, mapped_column

from core import Base

class ItemExercises(Base):
    __tablename__ = 'item_exercises'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey('routine_items.id'), nullable=False)
    exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey('exercises.id'), nullable=True)
    min_sets: Mapped[int] = mapped_column(Integer, nullable=False)
    max_sets: Mapped[int] = mapped_column(Integer, nullable=True)
    set_duration: Mapped[time] = mapped_column(Time, nullable=True)
    set_interval: Mapped[time] = mapped_column(Time, nullable=True)
    min_reps: Mapped[int] = mapped_column(Integer, nullable=False)
    max_reps: Mapped[int] = mapped_column(Integer, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=True)

    item: Mapped['RoutineItem'] = relationship('RoutineItem', back_populates='exercises', foreign_keys=[item_id])
    exercise: Mapped['Exercise'] = relationship('Exercise', foreign_keys=[exercise_id])
