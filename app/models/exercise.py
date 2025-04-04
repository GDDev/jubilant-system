from app.utils import Base

from sqlalchemy import Integer, Float, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Exercise(Base):
    __tablename__ = 'exercises'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey('plan_items.id'))
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    min_sets: Mapped[int] = mapped_column(Integer, nullable=False)
    max_sets: Mapped[int] = mapped_column(Integer, nullable=True)
    set_duration: Mapped[int] = mapped_column(Integer, nullable=False)
    set_interval: Mapped[int] = mapped_column(Integer, nullable=False)
    min_reps: Mapped[int] = mapped_column(Integer, nullable=True)
    max_reps: Mapped[int] = mapped_column(Integer, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=False)