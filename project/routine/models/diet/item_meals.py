from sqlalchemy import Integer, ForeignKey, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base

class ItemMeals(Base):
    __tablename__ = 'item_meals'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey('routine_items.id'), nullable=False)
    total_calories: Mapped[float] = mapped_column(Float, nullable=True)
    total_protein: Mapped[float] = mapped_column(Float, nullable=True)
    total_fat: Mapped[float] = mapped_column(Float, nullable=True)
    total_carbs: Mapped[float] = mapped_column(Float, nullable=True)
    goal: Mapped[str] = mapped_column(String(100), nullable=True)

    item: Mapped['RoutineItem'] = relationship('RoutineItem', back_populates='meals', foreign_keys=[item_id])
    meal_options: Mapped[list['MealOpt']] = relationship('MealOpt', back_populates='item_meal', foreign_keys='[MealOpt.item_id]', cascade='all, delete-orphan')
