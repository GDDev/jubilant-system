from core import Base

from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column


class Food(Base):
    __tablename__ = 'foods'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
