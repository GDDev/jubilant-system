from http.client import HTTPException

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from .. import routine_bp
from ..forms.new_routine_form import NewRoutineForm
from ..services import RoutineService
from ...major import AreaTags

routine_service = RoutineService()


@routine_bp.route('/listar/', methods=['GET'])
@login_required
def list_all():
    routine_type = request.args.get('routine_type')
    routines = []
    try:
        routines = routine_service.get_routines_by_type(routine_type)
    except Exception as e:
        flash(str(e))

    return render_template('routine/routine_list.html', routines=routines)


@routine_bp.route('/criar/', methods=['GET', 'POST'])
@login_required
def new():
    routine_type = request.args.get('routine_type')
    form = NewRoutineForm()
    form.who_for.choices = [('', 'Selecione um amigo...')] + [
        (friend.id, f'{friend.user.name} {friend.user.surname}') for friend in current_user.friends
    ]

    routine_id = request.args.get('routine_id')
    routine = routine_service.get_by_id(int(routine_id)) if routine_id else None
    try:
        if form.validate_on_submit():
            who_for = form.who_for.data
            # Should be None for the first time creating it
            routine_id = form.routine_id.data

            if not routine:
                # Creates a new routine
                routine = routine_service.add(who_for, routine_type)
            if not routine:
                raise Exception(f'Rotina não encontrada para ID: {routine_id}')

            routine.created_for = who_for
            routine_service.update(routine)
            # Doing a redirect so it doesn't submit the form again
            return redirect(url_for('routine.new')+f'?routine_type={routine.type.value}&routine_id={routine.id}')
        return render_template('routine/new_routine.html', form=form, routine=routine, routine_type=routine_type)

    except Exception as e:
        flash(str(e))

        return redirect(url_for('routine.list_all', routine_type=routine_type))


@routine_bp.route('/editar/<int:routine_id>', methods=['GET', 'POST'])
@login_required
def update(routine_id: int):
    routine = routine_service.get_by_id(int(routine_id))
    try:
        if routine:
            return render_template('routine/edit_routine.html', routine=routine)

    except Exception as e:
        flash(str(e))

    return redirect(url_for('routine.list_all')+f'?routine_type={routine.type.value}')


@routine_bp.route('/remover/<int:routine_id>', methods=['GET'])
@login_required
def delete(routine_id: int):
    routine = routine_service.get_by_id(routine_id)
    routine_type = routine.type.value
    try:
        if routine:
            routine_service.delete(routine)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('routine.list_all', routine_type=routine_type))


@routine_bp.route('/visualizar/<int:routine_id>', methods=['GET'])
@login_required
def detail(routine_id: int):
    try:
        routine = routine_service.get_by_id(routine_id)
        if not routine:
            raise Exception('Rotina não encontrada.')

        return render_template('routine/detail_routine.html', routine=routine)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('main.home'))

@routine_bp.route('/selecionar/revisor', methods=['GET', 'POST'])
@login_required
def select_supervisor():
    routine_id = request.args.get('routine_id')
    routine = routine_service.get_by_id(int(routine_id))
    major_tag = AreaTags.NUTRI if routine.type.value == 'dietary' else AreaTags.PE
    professors = [friend for friend in current_user.friends if friend.teaches(major_tag)]
    try:
        if not professors:
            raise Exception('Você precisa ser amigo de um professor desta área para submeter essa rotina à análise.')
        if not routine:
            raise Exception('Rotina não encontrada.')

    except (HTTPException, Exception) as e:
        flash(str(e))
        return redirect(url_for('main.home'))
    return render_template('routine/select_supervisor.html', professors=professors)
