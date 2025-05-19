from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from ..models import RoutineItem, ItemType
from ..repositories import ItemRepository


class ItemService:

    def __init__(self):
        self.item_repo = ItemRepository()

    def add(self, routine_type: str, routine_id: int, name: str, expiration_date: datetime, description: str) -> RoutineItem | None:
        try:
            if routine_type == 'treino':
                routine_type = ItemType.WORKOUT.value
            elif routine_type == 'dieta':
                routine_type = ItemType.DIET.value

            return self.item_repo.insert(RoutineItem(
                routine_id=routine_id,
                type=routine_type,
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
