from core import db
from project.routine import ExerciseItem


class ExerciseItemRepository:

    @staticmethod
    def insert(item: ExerciseItem):
        db.session.add(item)
        db.session.commit()

    @staticmethod
    def update(item: ExerciseItem):
        db.session.commit()

    @staticmethod
    def delete(item: ExerciseItem):
        db.session.delete(item)
        db.session.commit()
