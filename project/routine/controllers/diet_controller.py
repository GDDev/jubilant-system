from http.client import HTTPException

from flask import request, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from ..models import ItemOpts, OptFoods
from ..services import ItemService, MealService
from ..forms import NewOptionForm, NewOptFoodForm
from .. import item_bp


item_service = ItemService()
opt_service = MealService(ItemOpts)
food_service = MealService(OptFoods)


@item_bp.route('/dieta/opcoes', methods=['GET'])
@login_required
def diet_meals():
    item_id = request.args.get('item_id')
    item = item_service.find_by_id(int(item_id))
    try:
        if not item:
            raise Exception('Item não encontrado.')
        if (item.routine.created_for != current_user.id and
            item.routine.created_by != current_user.id and
            item.routine.supervisor_id != current_user.id):
            abort(403)
        return render_template('diet/item_meals.html', item=item)
    except Exception as e:
        flash(str(e))
    return redirect(url_for('item.add', routine_id=item.routine_id))


@item_bp.route('/dieta/adicionar/opcao/', methods=['GET', 'POST'])
@login_required
def add_opt():
    # Tries to get the id from the URL or from a form
    item_id = request.args.get('item_id') or request.form.get('item_id')

    try:
        if not item_id:
            raise Exception('ID do item não informado.')

        item = item_service.find_by_id(int(item_id))
        if not item:
            raise Exception('Item não encontrado.')

        if not item.routine.created_by != current_user.id and item.routine.supervisor_id != current_user.id:
            abort(403)
        form = NewOptionForm()

        if form.validate_on_submit():
            opt = opt_service.add(
                item_id=item.id,
                ref_time=form.ref_time.data,
                total_calories=form.total_calories.data,
                total_protein=form.total_protein.data,
                total_fat=form.total_fat.data,
                total_carbs=form.total_carbs.data,
                goal=form.goal.data,
            )
            return redirect(url_for('item.add_food')+f'?opt_id={opt.id}')

        return render_template('diet/new_opt_item.html', form=form, item=item)
    except (HTTPException, TypeError, Exception) as e:
        flash(str(e))
    return redirect(url_for('item.diet_meals', item_id=item_id))


@item_bp.route('/dieta/adicionar/alimento/', methods=['GET', 'POST'])
@login_required
def add_food():
    option_id = request.args.get('opt_id')
    try:
        if not option_id:
            raise Exception('Opção não encontrada.')
        option = opt_service.find_by_id(int(option_id))
        if option:
            form = NewOptFoodForm()
            if form.validate_on_submit():
                food_service.add(
                    opt_id=option.id,
                    name=form.name.data,
                    quantity=form.quantity.data,
                    weight=form.weight.data,
                    description=form.description.data,
                )
                return redirect(url_for('item.detail_opt', opt_id=option.id))
            return render_template('diet/new_opt_food.html', form=form, option=option)
    except (HTTPException, TypeError, Exception) as e:
        flash(str(e))
    return redirect(url_for('routine.list_all', routine_type='dietary'))


@item_bp.route('/dieta/remover/opcao', methods=['GET'])
@login_required
def remove_opt():
    option_id = request.args.get('opt_id')
    try:
        if option_id:
            option = opt_service.find_by_id(int(option_id))
            if option:
                item_id = option.item_id
                opt_service.delete(option)
                return redirect(url_for('item.diet_meals', item_id=item_id))
    except Exception as e:
        flash(str(e))
    return redirect(url_for('routine.list_all', routine_type='dietary'))


@item_bp.route('/dieta/remover/alimento', methods=['GET'])
@login_required
def remove_food():
    food_id = request.args.get('food_id')
    try:
        if food_id:
            food = food_service.find_by_id(int(food_id))
            if food:
                opt_id = food.opt_id
                food_service.delete(food)

                return redirect(url_for('item.detail_opt', opt_id=opt_id))
    except (HTTPException, Exception) as e:
        flash(str(e))
    return redirect(url_for('routine.list_all', routine_type='dietary'))


@item_bp.route('/dieta/editar/opcao', methods=['GET', 'POST'])
@login_required
def update_opt():
    option_id = request.args.get('opt_id')
    try:
        if option_id:
            option = opt_service.find_by_id(int(option_id))
            if option:
                form = NewOptionForm()
                if form.validate_on_submit():
                    opt_service.update(option, **form.data)
                    return redirect(url_for('item.diet_meals', item_id=option.item_id))
                return render_template('diet/edit_opt.html', form=form, option=option)
    except (HTTPException, Exception) as e:
        flash(str(e))
    return redirect(url_for('item.detail_opt', opt_id=option_id))


@item_bp.route('/dieta/editar/alimento', methods=['GET', 'POST'])
@login_required
def update_food():
    food_id = request.args.get('food_id')
    try:
        if food_id:
            food = food_service.find_by_id(int(food_id))
            if food:
                form = NewOptFoodForm()
                if form.validate_on_submit():
                    food_service.update(food, **form.data)
                    return redirect(url_for('item.detail_opt', opt_id=food.opt_id))
                return render_template('diet/edit_food.html', form=form, food=food)
    except (HTTPException, Exception) as e:
        flash(str(e))
    return redirect(url_for('routine.list_all', routine_type='dietary'))


@item_bp.route('/dieta/detalhar')
@login_required
def detail_opt():
    option_id = request.args.get('opt_id')
    try:
        if not option_id:
            raise Exception('ID da opção não informado.')
        option = opt_service.find_by_id(int(option_id))
        if not option:
            raise Exception('Opção não encontrada.')
        return render_template('diet/detail_opt.html', option=option)
    except (HTTPException, Exception) as e:
        flash(str(e))
    return redirect(url_for('routine.list_all', routine_type='dietary'))
