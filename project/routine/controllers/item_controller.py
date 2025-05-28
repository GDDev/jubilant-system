from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from .. import item_bp
from ..forms import NewItemForm
from ..services import ItemService, RoutineService


item_service = ItemService()
routine_service = RoutineService()


@item_bp.route('/adicionar/<int:routine_id>', methods=['GET', 'POST'])
def add(routine_id: int):
    form = NewItemForm()
    routine = routine_service.get_by_id(routine_id)
    try:
        if form.validate_on_submit():
            item = item_service.add(
                routine_type=routine.type.value,
                routine_id=routine_id,
                name=form.name.data,
                expiration_date=form.expiration_date.data,
                description=form.description.data,
            )
            if item.type == 'workout_item':
                return redirect(url_for('item.workout_exercises', item_id=item.id))
            if item.type == 'meal_item':
                return redirect(url_for('item.diet_meals', item_id=item.id))
    except Exception as e:
        flash(str(e))
    return render_template('new_item.html', form=form, routine=routine)

@item_bp.route('/remover/<int:item_id>', methods=['GET'])
@login_required
def remove(item_id: int):
    item = item_service.find_by_id(item_id)
    routine_id = item.routine_id
    try:
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
        return render_template('detail_item.html', item=item)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('main.home'))
