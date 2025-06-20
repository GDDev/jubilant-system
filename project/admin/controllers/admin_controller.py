from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import HTTPException

from utils import admin_required
from .. import admin_bp
from ..services import AdminService

admin_service = AdminService()


@admin_bp.route('/', methods=['GET'])
@login_required
@admin_required
def panel():
    overall = admin_service.get_overall_stats()
    return render_template('panel.html', overall=overall)


@admin_bp.route('/usuario', methods=['GET'])
@login_required
@admin_required
def control_user():
    from project.user import UserProfileService
    profile_service = UserProfileService()

    profile_id = request.args.get('p_id')
    try:
        if profile_id is None:
            raise Exception('ID não encontrado.')
        profile = profile_service.find_by_id(profile_id)
        if current_user.role != 'god' and current_user.id != profile.id:
            raise Exception('Admins não podem alterar informações de outros admins.')
        return render_template('control_user.html', profile=profile)
    except (HTTPException, Exception) as e:
        flash(str(e))
        return redirect(url_for('admin.panel'))