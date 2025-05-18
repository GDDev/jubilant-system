from flask import render_template

from .. import item_bp
from ..forms import NewWorkoutForm, NewDietForm
from ..services import ItemService


item_service = ItemService()


@item_bp.route('/adicionar/<string:routine_type>/<int:routine_id>', methods=['GET', 'POST'])
def add(routine_type: str, routine_id: int):
    form = NewWorkoutForm() if routine_type == 'treino' else NewDietForm()
    return render_template('new_item.html', form=form, routine_type=routine_type, routine_id=routine_id)
