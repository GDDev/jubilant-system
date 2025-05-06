from core import db
from project.routine import Routine


class RoutineRepository:

    @staticmethod
    def insert(routine: Routine):
        db.session.add(routine)
        db.session.commit()

    @staticmethod
    def update(routine: Routine):
        db.session.commit()

    @staticmethod
    def delete(routine: Routine):
        db.session.delete(routine)
        db.session.commit()

    @staticmethod
    def insert_without_commit(routine):
        db.session.add(routine)
        db.session.flush()
