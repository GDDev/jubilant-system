from sqlalchemy.exc import SQLAlchemyError

from ..models import ItemMeals, MealOpt, Food
from ..repositories import FoodRepository, MealOptRepository, ItemMealsRepository


class MealService:
    def __init__(self):
        self.food_repo = FoodRepository()
        self.opt_repo = MealOptRepository()
        self.meals_repo = ItemMealsRepository()


    def add(self, **kwargs):
        try:
            return self.meals_repo.insert(ItemMeals(**kwargs))
        except SQLAlchemyError as e:
            raise Exception('Erro ao adicionar refeição.') from e

    def add_option(self, **kwargs):
        try:
            return self.opt_repo.insert(MealOpt(**kwargs))
        except SQLAlchemyError as e:
            raise Exception('Erro ao adicionar refeição.') from e

    def add_food(self, **kwargs):
        try:
            return self.food_repo.insert(Food(**kwargs))
        except SQLAlchemyError as e:
            raise Exception('Erro ao adicionar refeição.') from e

    def find_by_id(self, meal_id: int) -> ItemMeals | None:
        try:
            return self.meals_repo.find_by_id(meal_id)
        except SQLAlchemyError as e:
            raise Exception('Erro ao buscar refeição.') from e

    def find_opt_by_id(self, opt_id: int) -> MealOpt | None:
        try:
            return self.opt_repo.find_by_id(opt_id)
        except SQLAlchemyError as e:
            raise Exception('Erro ao buscar refeição.') from e

    def find_food_by_id(self, food_id: int) -> Food | None:
        try:
            return self.food_repo.find_by_id(food_id)
        except SQLAlchemyError as e:
            raise Exception('Erro ao buscar refeição.') from e

    def delete(self, meal):
        try:
            return self.meals_repo.delete(meal)
        except SQLAlchemyError as e:
            raise Exception('Erro ao excluir refeição.') from e

    def delete_opt(self, opt):
        try:
            return self.opt_repo.delete(opt)
        except SQLAlchemyError as e:
            raise Exception('Erro ao excluir refeição.') from e

    def delete_food(self, food):
        try:
            return self.food_repo.delete(food)
        except SQLAlchemyError as e:
            raise Exception('Erro ao excluir refeição.') from e

    def update(self, meal, **kwargs):
        try:
            for arg in kwargs:
                if arg in meal.__dict__:
                    setattr(meal, arg, kwargs[arg])
            self.meals_repo.update(meal)
        except SQLAlchemyError as e:
            raise Exception('Erro ao atualizar refeição.') from e

    def update_opt(self, opt, **kwargs):
        try:
            for arg in kwargs:
                if arg in opt.__dict__:
                    setattr(opt, arg, kwargs[arg])
            self.opt_repo.update(opt)
        except SQLAlchemyError as e:
            raise Exception('Erro ao atualizar refeição.') from e

    def update_food(self, food, **kwargs):
        try:
            for arg in kwargs:
                if arg in food.__dict__:
                    setattr(food, arg, kwargs[arg])
            self.food_repo.update(food)
        except SQLAlchemyError as e:
            raise Exception('Erro ao atualizar refeição.') from e

