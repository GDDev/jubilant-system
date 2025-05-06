from flask_login import current_user

from project.routine import Routine, RoutineEnum
from project.routine.repositories.routine_repository import RoutineRepository


class RoutineService:

    def __init__(self):
        self.routine_repo = RoutineRepository()

    def add(self, routine_data: dict) -> Routine:
        routine_type = RoutineEnum(routine_data['type'])

        routine = Routine(
            created_by=current_user.id,
            created_for=routine_data.get('created_for'),
            type=routine_type
        )
        self.routine_repo.insert(routine)
        return routine
