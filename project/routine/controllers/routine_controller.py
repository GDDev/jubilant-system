from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required

from .. import routine_bp
from ..services import RoutineService


routine_service = RoutineService()


@routine_bp.route('/<string:workout_or_meal>', methods=['GET'])
@login_required
def list_all(workout_or_meal: str):
    return render_template('routine.html', workout_or_meal=workout_or_meal)


@routine_bp.route('/criar/<string:workout_or_meal>', methods=['GET', 'POST'])
@login_required
def new(workout_or_meal: str):
    routine = None
    try:
        if request.method == 'POST':
            who_for = request.form.get('who-for')
            if not who_for:
                raise Exception('Selecione um amigo.')
            routine_id = request.form.get('routine_id')

            if routine_id:
                routine = routine_service.get_by_id(int(routine_id))
                routine.created_for = who_for
                routine_service.update(routine)
            else:
                routine = routine_service.add(who_for, workout_or_meal)
            redirect(url_for('routine.new', workout_or_meal=workout_or_meal))
    except Exception as e:
        flash(str(e))

    return render_template('new_routine.html', workout_or_meal=workout_or_meal, routine=routine)

