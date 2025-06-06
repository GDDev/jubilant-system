from core import Base

from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship


class OptFoods(Base):
    __tablename__ = 'opt_foods'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    opt_id: Mapped[int] = mapped_column(Integer, ForeignKey('item_opts.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=True)

    opt: Mapped['ItemOpts'] = relationship('ItemOpts', back_populates='opt_foods', foreign_keys=[opt_id])
