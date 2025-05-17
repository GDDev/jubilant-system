from flask_login import current_user

from ..models import Routine, RoutineEnum
from ..repositories import RoutineRepository


class RoutineService:

    def __init__(self):
        self.routine_repo = RoutineRepository()

    def add(self, created_for: str, routine_type: str) -> Routine:
        routine_type = RoutineEnum.WORKOUT if routine_type == 'treino' else RoutineEnum.DIETARY

        routine = Routine(
            created_by=current_user.id,
            created_for=created_for,
            type=routine_type
        )
        self.routine_repo.insert(routine)
        return routine

    def get_by_id(self, routine_id: int) -> Routine | None:
        return self.routine_repo.find_by_id(routine_id)

    def update(self, routine: Routine) -> None:
        self.routine_repo.update(routine)
