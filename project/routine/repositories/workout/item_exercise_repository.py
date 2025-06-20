from utils import db
from ...models import ItemExercises


class ItemExerciseRepository:

    @staticmethod
    def insert(item):
        db.session.add(item)
        db.session.commit()

    @staticmethod
    def update(item):
        db.session.commit()

    @staticmethod
    def delete(item):
        db.session.delete(item)
        db.session.commit()

    @staticmethod
    def find_by_id(item_id):
        return db.session.get(ItemExercises, item_id)
