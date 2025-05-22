from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base

class ItemMeals(Base):
    __tablename__ = 'item_meals'

    id: Mapped[int] = mapped_column(Integer, ForeignKey('routine_items.id'), primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey('routine_items.id'), nullable=False)
    meal_opt_id: Mapped[int] = mapped_column(Integer, ForeignKey('meal_ops.id'), nullable=True)

    item: Mapped['RoutineItem'] = relationship('RoutineItem', back_populates='meals', foreign_keys=[item_id])
    meal_opt: Mapped['MealOpt'] = relationship('MealOpt', foreign_keys=[meal_opt_id])
