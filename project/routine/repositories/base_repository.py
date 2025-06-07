from typing import Generic, TypeVar, Type

from core import db


T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    @staticmethod
    def insert(item: T) -> T:
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def update(item: T):
        db.session.commit()

    @staticmethod
    def delete(item: T):
        db.session.delete(item)
        db.session.commit()

    def find_by_id(self, item_id: int) -> T:
        return db.session.get(self.model, item_id)

    def all(self) -> list[T]:
        return db.session.query(self.model).all()

    def filter_by(self, **kwargs) -> list[T]:
        return db.session.query(self.model).filter_by(**kwargs).all()

