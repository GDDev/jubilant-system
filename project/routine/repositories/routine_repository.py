from core import db
from project.routine.models import Routine


class RoutineRepository:

    @staticmethod
    def insert(routine):
        db.session.add(routine)
        db.session.commit()

    @staticmethod
    def update(routine):
        db.session.commit()

    @staticmethod
    def delete(routine):
        db.session.delete(routine)
        db.session.commit()

    @staticmethod
    def insert_without_commit(routine):
        db.session.add(routine)
        db.session.flush()

    @staticmethod
    def find_by_id(routine_id):
        return db.session.get(Routine, routine_id)
