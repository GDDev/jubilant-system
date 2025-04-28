from flask import render_template, flash, url_for, redirect
from flask_login import current_user, login_required

from ...notification import notification
from ...notification.exceptions import NotificationException
from ..services import NotificationService

noti_service = NotificationService()

@notification.route('/listar', methods=['GET'])
@login_required
def get_all():
    try:
        return render_template('notifications.html', notifications=current_user.notifications)
    except NotificationException as e:
        flash(str(e))
    return redirect(url_for('main.home'))
