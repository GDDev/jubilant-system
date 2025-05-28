from core import db
from ...models import ItemMeals


class ItemMealsRepository:
    @staticmethod
    def insert(item_meal: ItemMeals):
        db.session.add(item_meal)
        db.session.commit()
        return item_meal

    @staticmethod
    def update(item_meal: ItemMeals):
        db.session.commit()

    @staticmethod
    def delete(item_meal: ItemMeals):
        db.session.delete(item_meal)
        db.session.commit()

    @staticmethod
    def find_by_id(item_meal_id: int) -> ItemMeals | None:
        return db.session.get(ItemMeals, item_meal_id)

    @staticmethod
    def find_by_item_id(item_id: int) -> list[ItemMeals] | None:
        return db.session.query(ItemMeals).filter_by(item_id=item_id).all()
