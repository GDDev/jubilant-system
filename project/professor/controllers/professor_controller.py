from flask import redirect, url_for, flash, render_template, request
from flask_login import login_required
from werkzeug.exceptions import HTTPException

from utils.decorators import nutri_professor_required, pe_professor_required
from .. import professor_bp
from ..services import ProfessorService


professor_service = ProfessorService()


@professor_bp.route('/ver_dietas', methods=['GET'])
@login_required
@nutri_professor_required
def pending_diets():
    unapproved = []
    approved = []
    try:
        unapproved = professor_service.get_unapproved('dietary')
        approved = professor_service.get_approved('dietary')
    except (HTTPException, Exception) as e:
        flash(e.message) if hasattr(e, 'message') else flash('Ocorreu um erro desconhecido.')
    return render_template('list_diets.html', unapproved=unapproved, approved=approved)


@professor_bp.route('/ver_treinos', methods=['GET'])
@login_required
@pe_professor_required
def pending_workouts():
    unapproved = []
    approved = []
    try:
        unapproved = professor_service.get_unapproved('workout')
        approved = professor_service.get_approved('workout')
    except (HTTPException, Exception) as e:
        flash(e.message) if hasattr(e, 'message') else flash('Ocorreu um erro desconhecido.')
    return render_template('list_workouts.html', unapproved=unapproved, approved=approved)


@professor_bp.route('/detalhes', methods=['GET'])
@login_required
@pe_professor_required
def detail():
    from project.routine import RoutineService
    service = RoutineService()
    try:
        r_id = request.args.get('routine_id')
        if not r_id: raise Exception('ID não informado.')
        routine = service.get_by_id(int(r_id))
        if not routine: raise Exception('Rotina não encontrada.')
        return render_template('detail_diet.html', diet=routine) if routine.type.value == 'dietary' \
            else render_template('detail_workout.html', workout=routine)
    except (HTTPException, Exception) as e:
        flash(e.message) if hasattr(e, 'message') else flash('Ocorreu um erro desconhecido.')
    return redirect(url_for('main.home'))


@professor_bp.route('/aprovar', methods=['GET'])
@login_required
@pe_professor_required
def approve():
    try:
        r_id = request.args.get('routine_id')
        if not r_id: raise Exception('ID não informado')
        professor_service.approve(r_id)
    except (HTTPException, Exception) as e:
        flash(e.message) if hasattr(e, 'message') else flash('Ocorreu um erro desconhecido ao aprovar o treino.')
    return redirect(url_for('main.home'))
