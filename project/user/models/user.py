from utils import Base
from sqlalchemy import Integer, String # type: ignore
from sqlalchemy.orm import Mapped, mapped_column, relationship # type: ignore

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    profile: Mapped['UserProfile'] = relationship('UserProfile', uselist=False, back_populates='user', cascade='all, delete-orphan', single_parent=True)
