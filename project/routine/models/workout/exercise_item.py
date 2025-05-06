from datetime import time

from sqlalchemy import Integer, ForeignKey, Float, Time
from sqlalchemy.orm import Mapped, relationship, mapped_column

from core import Base
from .. import RoutineItem


class ExerciseItem(Base, RoutineItem):
    __tablename__ = 'exercise_items'
    __mapper_args__ = {
        'polymorphic_identity': 'exercise_item',
    }
    id: Mapped[int] = mapped_column(Integer, ForeignKey('routine_items.id'), primary_key=True)
    exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey('exercises.id'), nullable=True)
    min_sets: Mapped[int] = mapped_column(Integer, nullable=False)
    max_sets: Mapped[int] = mapped_column(Integer, nullable=True)
    set_duration: Mapped[time] = mapped_column(Time, nullable=False)
    set_interval: Mapped[time] = mapped_column(Time, nullable=False)
    min_reps: Mapped[int] = mapped_column(Integer, nullable=True)
    max_reps: Mapped[int] = mapped_column(Integer, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=False)

    exercise: Mapped['Exercise'] = relationship('Exercise', foreign_keys=[exercise_id])
