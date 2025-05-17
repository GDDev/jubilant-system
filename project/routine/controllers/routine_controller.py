from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from .. import routine_bp
from ..forms.new_routine_form import NewRoutineForm
from ..services import RoutineService


routine_service = RoutineService()


@routine_bp.route('/<string:routine_type>', methods=['GET'])
@login_required
def list_all(routine_type: str):
    return render_template('routine.html', routine_type=routine_type)


@routine_bp.route('/criar/<string:routine_type>', methods=['GET', 'POST'])
@login_required
def new(routine_type: str):
    try:
        # Initializes routine variable
        routine_id = request.args.get('routine_id')
        if routine_id is not None:
            routine = routine_service.get_by_id(int(routine_id))
        else:
            routine = None

        # Checks if a supervisor is selected
        if not current_user.supervisor:
            raise Exception('Você precisa selecionar um professor como supervisor.')

        form = NewRoutineForm()
        form.who_for.choices = [('', 'Selecione um amigo...')] + [
            (friend.id, f'{friend.user.name} {friend.user.surname}') for friend in current_user.friends
        ]

        if form.validate_on_submit():
            who_for = form.who_for.data
            # Should be None for the first time creating it
            routine_id = form.routine_id.data

            if routine_id is None:
                # Creates a new routine
                routine = routine_service.add(who_for, routine_type)
            else:
                routine = routine_service.get_by_id(routine_id)
                if not routine:
                    raise Exception(f'Rotina não encontrada para ID: {routine_id}')

                routine.created_for = who_for
                routine_service.update(routine)
            # For the love of GOD DO NOT remove "+ '?routine_id={}'.format(routine.id)" DON'T EVEN THINK ABOUT IT
            return redirect(url_for('routine.new', routine_type=routine_type) + '?routine_id={}'.format(routine.id))
        return render_template('new_routine.html', form=form, routine_type=routine_type, routine=routine)

    except Exception as e:
        flash(str(e))
        if str(e) == 'Você precisa selecionar um professor como supervisor.':
            return redirect(url_for('perfil.detail_profile', code=current_user.code))
        return redirect(url_for('routine.list_all', routine_type=routine_type))


@routine_bp.route('/editar/<string:routine_type>/<int:routine_id>', methods=['GET', 'POST'])
@login_required
def update(routine_type: str, routine_id: int):
    try:
        routine = routine_service.get_by_id(int(routine_id))
        if routine:
            return render_template('edit_routine.html', routine_type=routine_type, routine=routine)

    except Exception as e:
        flash(str(e))

    return redirect(url_for('routine.list_all', routine_type=routine_type))


@routine_bp.route('/remover/<string:routine_type>/<int:routine_id>', methods=['GET'])
@login_required
def delete(routine_type: str, routine_id: int):
    try:
        if routine_id:
            routine_service.delete(routine_id)
        return redirect(url_for('routine.list_all', routine_type=routine_type))
    except Exception as e:
        flash(str(e))
    return redirect(url_for('routine.list_all', routine_type=routine_type))
