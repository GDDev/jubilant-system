from sqlalchemy.exc import SQLAlchemyError

from ..models import Exercise, ItemExercises
from ..repositories import ItemExerciseRepository, ExerciseRepository


class WorkoutService:

    def __init__(self):
        self.item_exercise_repo = ItemExerciseRepository()
        self.exercise_repo = ExerciseRepository()

    def add(self, item_id: int, form) -> None:
        try:
            exercise = self.exercise_repo.find_by_name_and_muscle_group(form.exercise_name.data, form.muscle_group.data)
            if not exercise:
                exercise = self.exercise_repo.insert(Exercise(
                    name=form.exercise_name.data,
                    muscle_group=form.muscle_group.data,
                    instruction=form.instruction.data))

            if exercise:
                self.item_exercise_repo.insert(ItemExercises(
                    item_id=item_id,
                    exercise_id=exercise.id,
                    min_sets=form.min_sets.data,
                    max_sets=form.max_sets.data,
                    set_duration=form.set_duration.data,
                    set_interval=form.set_interval.data,
                    min_reps=form.min_reps.data,
                    max_reps=form.max_reps.data,
                    weight=form.weight.data,
                ))
        except SQLAlchemyError as e:
            raise Exception('Erro ao adicionar exercício ao treino.') from e

    def delete(self, exercise_id):
        try:
            item_exercise = self.item_exercise_repo.find_by_id(exercise_id)
            self.item_exercise_repo.delete(item_exercise)
        except SQLAlchemyError as e:
            raise Exception('Falha ao deletar exercício do treino.' + e._message()) from e
