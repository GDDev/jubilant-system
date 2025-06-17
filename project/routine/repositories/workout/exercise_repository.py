from utils import db
from project.routine.models import Exercise


class ExerciseRepository:
    @staticmethod
    def insert(exercise):
        db.session.add(exercise)
        db.session.commit()
        return exercise

    @staticmethod
    def update(exercise):
        db.session.commit()

    @staticmethod
    def delete(exercise):
        db.session.delete(exercise)
        db.session.commit()

    @staticmethod
    def find_by_name(name):
        return db.session.query(Exercise).filter_by(name=name).first()

    @staticmethod
    def find_by_name_and_muscle_group(name, muscle_group):
        return db.session.query(Exercise).filter_by(name=name, muscle_group=muscle_group).first()

    @staticmethod
    def find_by_id( exercise_id):
        return db.session.get(Exercise, exercise_id)
