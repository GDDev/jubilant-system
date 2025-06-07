from typing import Generic, Type, TypeVar

from sqlalchemy.exc import SQLAlchemyError

from ..models import OptFoods, ItemOpts
from ..repositories import BaseRepository


T = TypeVar('T')


class MealService(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model
        self.base_repo = BaseRepository(self.model)


    def add(self, **kwargs):
        try:
            return self.base_repo.insert(self.model(**kwargs))
        except SQLAlchemyError as e:
            raise Exception('Erro ao adicionar à refeição.') from e
    #
    # def add_food(self, **kwargs):
    #     try:
    #         self.food_repo.insert(OptFoods(**kwargs))
    #     except SQLAlchemyError as e:
    #         raise Exception('Erro ao adicionar alimento à opção.') from e

    def find_by_id(self, item_id: int) -> T | None:
        try:
            return self.base_repo.find_by_id(item_id)
        except SQLAlchemyError as e:
            raise Exception('Erro ao buscar em refeição.') from e

    # def find_food_by_id(self, food_id: int) -> OptFoods | None:
    #     try:
    #         return self.food_repo.find_by_id(food_id)
    #     except SQLAlchemyError as e:
    #         raise Exception('Erro ao buscar alimento em refeição.') from e

    def delete(self, item):
        try:
            return self.base_repo.delete(item)
        except SQLAlchemyError as e:
            raise Exception('Erro ao excluir de refeição.') from e

    # def delete_food(self, food):
    #     try:
    #         return self.food_repo.delete(food)
    #     except SQLAlchemyError as e:
    #         raise Exception('Erro ao excluir refeição.') from e

    def update(self, item, **kwargs):
        try:
            for arg in kwargs:
                if arg in item.__dict__:
                    setattr(item, arg, kwargs[arg])
            self.base_repo.update(item)
        except SQLAlchemyError as e:
            raise Exception('Erro ao atualizar em refeição.') from e

    # def update_opt(self, opt, **kwargs):
    #     try:
    #         for arg in kwargs:
    #             if arg in opt.__dict__:
    #                 setattr(opt, arg, kwargs[arg])
    #         self.base_repo.update(opt)
    #     except SQLAlchemyError as e:
    #         raise Exception('Erro ao atualizar refeição.') from e

    # def update_food(self, food, **kwargs):
    #     try:
    #         for arg in kwargs:
    #             if arg in food.__dict__:
    #                 setattr(food, arg, kwargs[arg])
    #         self.food_repo.update(food)
    #     except SQLAlchemyError as e:
    #         raise Exception('Erro ao atualizar refeição.') from e

