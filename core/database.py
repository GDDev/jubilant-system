from abc import ABCMeta

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class DeclarativeABCMeta(ABCMeta, type(DeclarativeBase)):
    pass


class Base(DeclarativeBase, metaclass=DeclarativeABCMeta):
    __abstract__ = True


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
