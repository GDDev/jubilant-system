from core import db


class ExerciseItemRepository:

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
