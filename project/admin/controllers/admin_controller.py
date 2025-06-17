from flask import render_template, request
from flask_login import login_required

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
    if profile_id is None:
        pass
    profile = profile_service.find_by_id(profile_id)
    return render_template('control_user.html', profile=profile)
