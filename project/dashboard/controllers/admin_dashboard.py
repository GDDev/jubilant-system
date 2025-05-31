from flask import render_template
from flask_login import login_required

from core import admin_required
from .. import admin_ds_bp


@admin_ds_bp.route('/dashboard', methods=['GET'])
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')
