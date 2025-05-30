from core import Base

from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Food(Base):
    __tablename__ = 'foods'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    option_id: Mapped[int] = mapped_column(Integer, ForeignKey('meal_options.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)

    option: Mapped['MealOpt'] = relationship('MealOpt', back_populates='foods', foreign_keys=[option_id])
