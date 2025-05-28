from core import db
from ...models import Food


class FoodRepository:
    @staticmethod
    def insert(food: Food):
        db.session.add(food)
        db.session.commit()

    @staticmethod
    def update(food: Food):
        db.session.commit()

    @staticmethod
    def delete(food: Food):
        db.session.delete(food)
        db.session.commit()

    @staticmethod
    def find_by_id(food_id: int) -> Food | None:
        return db.session.get(Food, food_id)
