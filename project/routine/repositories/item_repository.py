from utils import db
from ..models import RoutineItem


class ItemRepository:

    @staticmethod
    def insert(item: RoutineItem) -> RoutineItem:
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def update(item: RoutineItem) -> None:
        db.session.commit()

    @staticmethod
    def delete(item: RoutineItem) -> None:
        db.session.delete(item)
        db.session.commit()

    @staticmethod
    def find_by_id(item_id: int) -> RoutineItem | None:
        return db.session.get(RoutineItem, item_id)

    @staticmethod
    def find_by_routine_id(routine_id: int) -> list[RoutineItem] | None:
        return db.session.query(RoutineItem).filter_by(routine_id=routine_id).all()
