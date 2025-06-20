from flask import render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from .. import item_bp
from ..forms import NewItemForm
from ..services import ItemService, RoutineService
from utils.normalize import strip_title


item_service = ItemService()
routine_service = RoutineService()


@item_bp.route('/adicionar/<int:routine_id>', methods=['GET', 'POST'])
def add(routine_id: int):
    form = NewItemForm()
    routine = routine_service.get_by_id(routine_id)
    try:
        if routine.created_by != current_user.id:
            abort(403)
        if form.validate_on_submit():
            item = item_service.add(
                routine_type=routine.type.value,
                routine_id=routine_id,
                name=strip_title(form.name.data),
                expiration_date=form.expiration_date.data,
                source=form.source.data,
            )
            if item.type == 'workout_item':
                return redirect(url_for('item.workout_exercises', item_id=item.id))
            if item.type == 'meal_item':
                return redirect(url_for('item.diet_meals', item_id=item.id))
    except Exception as e:
        flash(str(e))
    return render_template('item_routine/new_item.html', form=form, routine=routine)

@item_bp.route('/remover/<int:item_id>', methods=['GET'])
@login_required
def remove(item_id: int):
    item = item_service.find_by_id(item_id)
    routine_id = item.routine_id
    try:
        routine = routine_service.get_by_id(routine_id)
        if routine:
            if routine.created_by != current_user.id:
                abort(403)
            item_service.delete(item_id)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('routine.update', routine_id=routine_id))


@item_bp.route('/visualizar/<int:item_id>', methods=['GET'])
@login_required
def detail(item_id:int):
    try:
        item = item_service.find_by_id(item_id)
        if not item:
            raise Exception('Item não encontrado.')
        if item.routine.created_for != current_user.id and item.routine.created_by != current_user.id:
            abort(403)
        return render_template('item_routine/detail_item.html', item=item)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('main.home'))
