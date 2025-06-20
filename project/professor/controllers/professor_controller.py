from flask import redirect, url_for, flash, render_template
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
    diets = []
    try:
        diets = professor_service.get_unapproved_diets()
    except (HTTPException, Exception) as e:
        flash(e.message) if hasattr(e, 'message') else flash('Ocorreu um erro desconhecido.')
    return render_template('list_diets.html', diets=diets)


@professor_bp.route('/ver_treinos', methods=['GET'])
@login_required
@pe_professor_required
def pending_workouts():
    workouts = []
    try:
        workouts = professor_service.get_unapproved_workouts()
    except (HTTPException, Exception) as e:
        flash(e.message) if hasattr(e, 'message') else flash('Ocorreu um erro desconhecido.')
    return render_template('list_workouts.html', workouts=workouts)
