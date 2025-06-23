import datetime

from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from ...routine import RoutineService, MealService, ItemService, WorkoutService
from ...routine import RoutineRepository


class ProfessorService:
    def __init__(self):
        self.routine = RoutineService()
        self.routine_repo = RoutineRepository()

    # This goes through the user's friends and then get their open routines
    @staticmethod
    def get_unapproved(r_type:str = 'dietary' or 'workout'):
        try:
            friends_routines = [f.created_routines for f in current_user.friends][0]
            routines = [r for r in friends_routines if r.status.value == 'pending' and r.type.value == r_type]
            return sorted(routines, key=lambda r: r.last_updated_at, reverse=False)
        except Exception as e:
            raise Exception('Erro ao recuperar rotinas para aprovar.') from e

    @staticmethod
    def get_approved(r_type:str = 'dietary' or 'workout'):
        try:
            return sorted([r for r in [f.created_routines for f in current_user.friends][0]
                    if r.status.value == 'approved' and r.type.value == r_type],
                          key=lambda r: r.approved_at, reverse=True)
        except Exception as e:
            raise Exception('Erro ao recuperar rotinas aprovadas.') from e

    def approve(self, r_id):
        from project.routine import RoutineStatus
        try:
            routine = self.routine_repo.find_by_id(int(r_id))
            if not routine: raise Exception('Treino não encontrado.')
            if routine.status.value == 'approved': raise Exception('Treino já aprovado.')
            routine.status = RoutineStatus.APPROVED
            routine.approved_at = datetime.datetime.now()
            routine.supervisor_id = current_user.id
            self.routine_repo.update(routine)
        except (SQLAlchemyError, Exception) as e:
            raise e
