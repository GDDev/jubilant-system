from .. import routine_bp


@routine_bp.route('/dieta/<int:item_id>/opcoes', methods=['GET'])
def meal_options(item_id: int):
    pass
