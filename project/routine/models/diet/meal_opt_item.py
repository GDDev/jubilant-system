from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base

class MealOptItem(Base):
    __tablename__ = 'meal_opt_items'
    __mapper_args__ = {
        'polymorphic_identity': 'meal_opt_item',
    }

    id: Mapped[int] = mapped_column(Integer, ForeignKey('routine_items.id'), primary_key=True)
    meal_opt_id: Mapped[int] = mapped_column(Integer, ForeignKey('meal_ops.id'), nullable=True)

    meal_opt: Mapped['MealOpt'] = relationship('MealOpt', foreign_keys=[meal_opt_id])
