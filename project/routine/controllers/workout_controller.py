from flask import render_template, flash, redirect, url_for, request

from .. import item_bp
from ..forms import NewWorkoutForm
from ..services import ItemService, WorkoutService

item_service = ItemService()
workout_service = WorkoutService()


@item_bp.route('/treino/exercicios', methods=['GET'])
def workout_exercises():
    item_id = request.args.get('item_id')
    routine_id = request.args.get('routine_id')
    try:
        item = item_service.find_by_id(int(item_id))
        if not item:
            raise Exception('Item não encontrado.')
        return render_template('item_exercises.html', item=item)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('item.add', routine_type='treino', routine_id=int(routine_id)))


@item_bp.route('/treino/adicionar', methods=['GET', 'POST'])
def add_exercise():
    item_id = request.args.get('item_id')
    try:
        if not item_id:
            raise Exception('ID do item não informado.')
        item = item_service.find_by_id(int(item_id))
        if item:
            form = NewWorkoutForm()

            if form.validate_on_submit():
                workout_service.add(item.id, form)
                return redirect(url_for('item.workout_exercises', item_id=item.id, routine_id=item.routine_id))

            return render_template('new_exercise_item.html', form=form, item=item)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('routine.list_all', routine_type='treino'))

@item_bp.route('/treino/remover/<int:exercise_id>', methods=['GET'])
def remove_exercise(exercise_id: int):
    try:
        workout_service.delete(exercise_id=exercise_id)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('routine.list_all', routine_type='treino'))

