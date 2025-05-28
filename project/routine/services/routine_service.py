from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from ..models import Routine, RoutineEnum
from ..repositories import RoutineRepository


class RoutineService:

    def __init__(self):
        self.routine_repo = RoutineRepository()

    def add(self, created_for: str, routine_type: str) -> Routine:

        routine = Routine(
            created_by=current_user.id,
            created_for=created_for,
            type=RoutineEnum.WORKOUT.value if routine_type == 'workout' else RoutineEnum.DIETARY.value
        )
        self.routine_repo.insert(routine)
        return routine

    def get_by_id(self, routine_id: int) -> Routine | None:
        return self.routine_repo.find_by_id(routine_id)

    def update(self, routine: Routine) -> None:
        self.routine_repo.update(routine)

    def delete(self, routine: Routine) -> None:
        self.routine_repo.delete(routine)

    def get_routines_by_type(self, routine_type:str) -> list[Routine] | None:
        try:
            return self.routine_repo.get_routines_by_type(routine_type=routine_type, user_id=current_user.id)
        except SQLAlchemyError as e:
            raise Exception('Erro ao recuperar rotinas.') from e
