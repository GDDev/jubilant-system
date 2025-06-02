from flask import render_template
from flask_login import login_required

from core import admin_required
from .. import admin_ds_bp
from ..services import AdminDashboardService

admin_service = AdminDashboardService()


@admin_ds_bp.route('/dashboard', methods=['GET'])
@login_required
@admin_required
def admin_dashboard():
    overall = admin_service.get_overall_stats()
    return render_template('admin/admin_dashboard.html', overall=overall)
