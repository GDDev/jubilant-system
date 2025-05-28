from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from ..models import RoutineItem, ItemType
from ..repositories import ItemRepository


class ItemService:

    def __init__(self):
        self.item_repo = ItemRepository()

    def add(self, routine_type: str, routine_id: int, name: str, expiration_date: datetime, description: str) -> RoutineItem | None:
        try:
             return self.item_repo.insert(RoutineItem(
                routine_id=routine_id,
                type=ItemType.WORKOUT.value if routine_type == 'workout' else ItemType.DIET.value,
                name=name,
                expiration_date=expiration_date,
                description=description
            ))
        except SQLAlchemyError as e:
            raise Exception(f'Erro ao adicionar {routine_type}') from e

    def delete(self, item_id: int) -> None:
        try:
            item = self.item_repo.find_by_id(item_id)
            if item:
                self.item_repo.delete(item)
        except SQLAlchemyError as e:
            raise Exception(f'Erro ao remover item') from e

    def find_by_id(self, item_id: int) -> RoutineItem | None:
        try:
            return self.item_repo.find_by_id(item_id)
        except SQLAlchemyError as e:
            raise Exception(f'Erro ao recuperar item') from e

    def update(self, item):
        try:
            self.item_repo.update(item)
        except SQLAlchemyError as e:
            raise Exception(f'Erro ao atualizar item') from e
