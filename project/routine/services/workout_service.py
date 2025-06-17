from sqlalchemy.exc import SQLAlchemyError

from ..models import Exercise, ItemExercises
from ..repositories import ItemExerciseRepository, ExerciseRepository


class WorkoutService:

    def __init__(self):
        self.item_exercise_repo = ItemExerciseRepository()
        self.exercise_repo = ExerciseRepository()

    def add(self, **kwargs) -> None:
        try:
            # exercise = self.exercise_repo.find_by_name_and_muscle_group(
            #     kwargs.get('exercise_name'),
            #     kwargs.get('muscle_group')
            # )
            exercise = self.exercise_repo.insert(
                Exercise(
                    name=kwargs.get('name'),
                    muscle_group=kwargs.get('muscle_group'),
                    instruction=kwargs.get('instruction')
                )
            )
            if not exercise:
                raise Exception('Falha ao adicionar exercício à base de dados.')

            item_exercise = ItemExercises()
            for arg in kwargs:
                if arg in ItemExercises.__table__.columns.keys():
                    setattr(item_exercise, arg, kwargs[arg])
            item_exercise.exercise_id=exercise.id

            self.item_exercise_repo.insert(item_exercise)

        except SQLAlchemyError as e:
            raise Exception('Erro ao adicionar exercício ao treino.') from e

    def delete(self, exercise_id):
        try:
            item_exercise = self.item_exercise_repo.find_by_id(exercise_id)
            self.item_exercise_repo.delete(item_exercise)
        except SQLAlchemyError as e:
            raise Exception('Falha ao deletar exercício do treino.') from e

    def delete_exercise(self, exercise_id):
        try:
            exercise = self.exercise_repo.find_by_id(exercise_id)
            if exercise:
                self.exercise_repo.delete(exercise)
        except SQLAlchemyError as e:
            raise Exception('Falha ao deletar exercício da base de dados.') from e

    def find_by_exercise_id(self, exercise_id: int) -> Exercise | None:
        try:
            return self.exercise_repo.find_by_id(exercise_id)
        except SQLAlchemyError as e:
            raise Exception('Falha ao buscar exercício.') from e

    def find_by_item_id(self, item_id: int) -> ItemExercises | None:
        try:
            return self.item_exercise_repo.find_by_id(item_id)
        except SQLAlchemyError as e:
            raise Exception('Falha ao buscar item.') from e

    def update_item(self, item, **kwargs):
        try:
            for arg in kwargs:
                if arg in item.__dict__:
                    setattr(item, arg, kwargs[arg])
            self.item_exercise_repo.update(item)
        except SQLAlchemyError as e:
            raise Exception('Falha ao atualizar item.') from e

    def update_exercise(self, exercise, **kwargs):
        try:
            for arg in kwargs:
                if arg in exercise.__dict__:
                    setattr(exercise, arg, kwargs[arg])
            self.exercise_repo.update(exercise)
        except SQLAlchemyError as e:
            raise Exception('Falha ao atualizar exercício.') from e
