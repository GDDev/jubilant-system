from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from ...routine import RoutineService, MealService, ItemService, WorkoutService
from ...routine import RoutineRepository


class ProfessorService:
    def __init__(self):
        self.routine = RoutineService()
        self.routine_repo = RoutineRepository()

    def get_unapproved_diets(self):
        try:
            return [d for d in self.routine_repo.get_unapproved_diets() if d.creator in current_user.friends]
        except (SQLAlchemyError, Exception) as e:
            raise e

    def get_unapproved_workouts(self):
        try:
            return [w for w in self.routine_repo.get_unapproved_workouts() if w.creator in current_user.friends]
        except (SQLAlchemyError, Exception) as e:
            raise e
