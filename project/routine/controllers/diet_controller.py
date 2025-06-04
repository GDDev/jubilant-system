from flask import request, render_template, flash, redirect, url_for
from flask_login import login_required

from ..services import ItemService, MealService
from ..forms import NewMealForm, NewOptionForm, NewOptFoodForm
from .. import item_bp


item_service = ItemService()
meal_service = MealService()


@item_bp.route('/dieta/refeicoes', methods=['GET'])
@login_required
def diet_meals():
    item_id = request.args.get('item_id')
    item = item_service.find_by_id(int(item_id))
    try:
        if not item:
            raise Exception('Item não encontrado.')
        return render_template('diet/item_meals.html', item=item)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('item.add', routine_id=item.routine_id))


@item_bp.route('/dieta/adicionar/refeicao/', methods=['GET', 'POST'])
@login_required
def add_meal():
    item_id = request.args.get('item_id')
    if not item_id:
        item_id = request.form.get('item_id')

    try:
        if not item_id:
            raise Exception('ID do item não informado.')
        item = item_service.find_by_id(int(item_id))

        if not item:
            raise Exception('Item não encontrado.')
        form = NewMealForm()

        if form.validate_on_submit():
            meal = meal_service.add(
                item_id=item.id,
                total_calories=form.total_calories.data,
                total_protein=form.total_protein.data,
                total_fat=form.total_fat.data,
                total_carbs=form.total_carbs.data,
                goal=form.goal.data,
            )
            return redirect(url_for('item.add_option')+f'?meal_id={meal.id}')

        return render_template('diet/new_meal_item.html', form=form, item=item)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('item.diet_meals', item_id=item_id))


@item_bp.route('/dieta/adicionar/opcao/', methods=['GET', 'POST'])
@login_required
def add_option():
    meal_id = request.args.get('meal_id')
    meal = meal_service.find_by_id(int(meal_id))
    form = NewOptionForm()
    try:
        if not meal:
            raise Exception('Refeição não encontrada.')

        if form.validate_on_submit():
            opt = meal_service.add_option(
                item_id=meal.id,
                name=form.name.data,
                description=form.description.data,
                meal_time=form.meal_time.data,
            )
            return redirect(url_for('item.add_food', opt_id=opt.id))
    except Exception as e:
        flash(str(e))

    return render_template('diet/new_meal_option.html', form=form, meal=meal)


@item_bp.route('/dieta/adicionar/alimento/', methods=['GET', 'POST'])
@login_required
def add_food():
    option_id = request.args.get('opt_id')
    option = meal_service.find_opt_by_id(int(option_id))
    form = NewOptFoodForm()
    try:
        if form.validate_on_submit():
            meal_service.add_food(
                option_id=option.id,
                name=form.name.data,
                quantity=form.quantity.data,
                weight=form.weight.data,
                description=form.description.data,
            )
            return redirect(url_for('item.diet_meals', item_id=option.item_meal.item_id))
    except Exception as e:
        flash(str(e))
    return render_template('diet/new_opt_food.html', form=form, option=option)


@item_bp.route('/dieta/remover/refeicao/<int:meal_id>', methods=['GET'])
@login_required
def remove_meal(meal_id: int):
    item_id = None
    try:
        meal = meal_service.find_by_id(meal_id)
        item_id = meal.item_id
        if meal:
            meal_service.delete(meal)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('item.diet_meals', item_id=item_id))


@item_bp.route('/dieta/remover/opcao/<int:opt_id>', methods=['GET'])
@login_required
def remove_option(opt_id: int):
    option = meal_service.find_opt_by_id(opt_id)
    try:
        if option:
            meal_service.delete_opt(option)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('routine.list_all', routine_type='dietary'))


@item_bp.route('/dieta/remover/alimento/<int:food_id>', methods=['GET'])
@login_required
def remove_food(food_id: int):
    option = meal_service.find_food_by_id(food_id)
    try:
        if option:
            meal_service.delete_food(option)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('routine.list_all', routine_type='dietary'))


@item_bp.route('/dieta/editar/refeicao/<int:meal_id>', methods=['GET', 'POST'])
@login_required
def update_meal(meal_id: int):
    pass


@item_bp.route('/dieta/editar/opcao/<int:opt_id>', methods=['GET', 'POST'])
@login_required
def update_option(opt_id: int):
    pass


@item_bp.route('/dieta/editar/alimento/<int:food_id>', methods=['GET', 'POST'])
@login_required
def update_food(food_id: int):
    pass

@item_bp.route('/dieta/detalhar')
@login_required
def detail_meal():
    pass
