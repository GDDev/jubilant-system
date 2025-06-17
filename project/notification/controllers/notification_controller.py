from flask import render_template, flash, url_for, redirect, request, abort
from flask_login import current_user, login_required

from ...notification import notification
from ...notification.exceptions import NotificationException
from ..services import NotificationService
from ...user.models.user_profile import RoleEnum

noti_service = NotificationService()

@notification.route('/listar', methods=['GET'])
@login_required
def get_all():
    try:
        return render_template('notifications.html', notifications=current_user.notifications)
    except NotificationException as e:
        flash(str(e))
    return redirect(url_for('main.home'))

@notification.route('/nova_notificacao', methods=['GET', 'POST'])
@login_required
def send_system_noti():
    if current_user.role == RoleEnum.ADMIN or current_user.role == RoleEnum.GOD:
        try:
            if request.method == 'GET':
                return render_template('new_noti.html')
            noti_service.send_system_notification(request.form.get('content'), request.form.get('target'))
        except NotificationException as e:
            flash(str(e))
    return redirect(url_for('notificacao.get_all'))

@notification.route('/ler_todas', methods=['POST'])
@login_required
def read_all():
    try:
        notifications = [n for n in current_user.notifications if n.seen == False]
        noti_service.read_all(notifications)
    except NotificationException as e:
        flash(str(e))
    return redirect(url_for('notificacao.get_all'))


@notification.route('/remover/<int:notification_id>', methods=['GET', 'POST'])
@login_required
def delete(notification_id: int):
    try:
        noti = noti_service.get_by_id(notification_id)
        if noti:
            if noti.receiver_id != current_user.id:
                abort(403)
            noti_service.delete(noti)
    except NotificationException as e:
        flash(str(e))
    return redirect(url_for('notificacao.get_all'))
