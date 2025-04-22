from core import Base

from sqlalchemy import Integer, String, ForeignKey, Time
from sqlalchemy.orm import Mapped, mapped_column

from datetime import time

class MealOpt(Base):
    __tablename__ = 'meal_options'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey('plan_items.id'))
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    meal_time: Mapped[time] = mapped_column(Time, nullable=False)