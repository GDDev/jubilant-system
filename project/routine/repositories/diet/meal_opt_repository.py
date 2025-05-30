from core import db
from ...models import MealOpt


class MealOptRepository:
    @staticmethod
    def insert(meal_opt: MealOpt):
        db.session.add(meal_opt)
        db.session.commit()
        return meal_opt

    @staticmethod
    def update(meal_opt: MealOpt):
        db.session.commit()

    @staticmethod
    def delete(meal_opt: MealOpt):
        db.session.delete(meal_opt)
        db.session.commit()

    @staticmethod
    def find_by_id(meal_opt_id: int) -> MealOpt | None:
        return db.session.get(MealOpt, meal_opt_id)
