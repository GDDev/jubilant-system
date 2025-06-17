from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user

from .. import item_bp
from ..forms import NewWorkoutForm
from ..services import ItemService, WorkoutService

item_service = ItemService()
workout_service = WorkoutService()


@item_bp.route('/treino/exercicios', methods=['GET'])
def workout_exercises():
    item_id = request.args.get('item_id')
    item = item_service.find_by_id(int(item_id))
    try:
        if not item:
            raise Exception('Item não encontrado.')
        return render_template('workout/item_exercises.html', item=item)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('item.add', routine_id=item.routine_id))


@item_bp.route('/treino/adicionar/exercicio/', methods=['GET', 'POST'])
def add_exercise():
    item_id = request.args.get('item_id')
    try:
        if not item_id:
            raise Exception('ID do item não informado.')
        item = item_service.find_by_id(int(item_id))
        if item:
            form = NewWorkoutForm()
            if form.validate_on_submit():
                workout_service.add(
                    name=form.exercise_name.data,
                    muscle_group=form.muscle_group.data,
                    instruction=form.instruction.data.strip(),
                    item_id=item.id,
                    min_sets=form.min_sets.data,
                    max_sets=form.max_sets.data,
                    set_duration=form.set_duration.data,
                    set_interval=form.set_interval.data,
                    min_reps=form.min_reps.data,
                    max_reps=form.max_reps.data,
                    weight=form.weight.data
                )
                return redirect(url_for('item.workout_exercises', item_id=item.id, routine_id=item.routine_id))

            return render_template('workout/new_exercise_item.html', form=form, item=item)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('routine.list_all', routine_type='workout'))

@item_bp.route('/treino/remover/exercicio/<int:exercise_id>', methods=['GET'])
def remove_exercise(exercise_id: int):
    try:
        exercise = item_service.find_by_id(exercise_id)
        if exercise:
            if exercise.routine.created_by != current_user.id:
                abort(403)
        workout_service.delete(exercise_id=exercise_id)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('routine.list_all', routine_type='workout'))

@item_bp.route('/treino/editar/exercicio/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_exercise(item_id: int):
    form = NewWorkoutForm()
    item_exercise = workout_service.find_by_item_id(item_id)
    try:
        if item_exercise:
            if item_exercise.item.routine.created_by != current_user.id:
                abort(403)
        if form.validate_on_submit():
            if not item_exercise:
                raise Exception('Item de exercício não encontrado.')
            exercise = workout_service.find_by_exercise_id(item_exercise.exercise_id)
            if not exercise:
                raise Exception('Exercício não encontrado.')
            workout_service.update_exercise(
                exercise,
                name=form.exercise_name.data,
                muscle_group=form.muscle_group.data,
                instruction=request.form.get('instruction').strip()
            )
            workout_service.update_item(
                item_exercise,
                min_sets=form.min_sets.data,
                max_sets=form.max_sets.data,
                set_duration=item_exercise.set_duration if form.set_duration.data is None else
            form.set_duration.data,
                set_interval=item_exercise.set_interval if form.set_interval.data is None else form.set_interval.data,
                min_reps=form.min_reps.data,
                max_reps=form.max_reps.data,
                weight=form.weight.data
            )

            return redirect(url_for('item.workout_exercises', item_id=item_exercise.item.id))

    except Exception as e:
        flash(str(e))
    return render_template('workout/edit_exercise.html', form=form, item_exercise=item_exercise)
