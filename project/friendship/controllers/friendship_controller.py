from flask import redirect, flash, url_for, request, render_template
from flask_login import current_user, login_required

from .. import friendship
from ..services import FriendshipService
from ..exceptions import FriendshipException

from ...notification import NotificationException, NotificationService, NotificationType

friendship_service = FriendshipService()
notification_service = NotificationService()


@friendship.route('/adicionar', methods=['POST'])
@login_required
def send_request():
    try:
        # Sends friend request
        new_friendship = friendship_service.send_request(request.form.get('friend_id'))
        # Sends notification to user receiving friend request
        notification_service.send_notification(
            receiver_id=request.form.get('friend_id'),
            sender_id=current_user.id,
            type=NotificationType.FRIEND_REQUEST,
            content=f'{current_user.user.name} {current_user.user.surname} te enviou uma solicitação de amizade.',
            url=url_for('perfil.detail_profile', code=current_user.code),
            friendship_id=new_friendship.id
        )
    except (FriendshipException, NotificationException) as e:
        flash(str(e))
    return redirect(url_for('perfil.detail_profile', code=request.form.get('friend_code')))


@friendship.route('/aceitar/<int:friendship_id>', methods=['GET', 'POST'])
@login_required
def accept_request(friendship_id: int):
    try:
        notification = [n for n in current_user.notifications if n.friendship_id == friendship_id][0]
        notification_service.delete(notification)
        friendship_service.accept_request(friendship_id)
    except FriendshipException as e:
        flash(str(e))
    return redirect(url_for('main.home'))


@friendship.route('/recusar/<int:friendship_id>', methods=['GET', 'POST'])
@login_required
def decline_request(friendship_id: int):
    try:
        notification = [n for n in current_user.notifications if n.friendship_id == friendship_id][0]
        notification_service.delete(notification)

        friendship_service.decline_request(friendship_id)
    except FriendshipException as e:
        flash(str(e))
    return redirect(url_for('main.home'))


@friendship.route('/cancelar', methods=['POST'])
@login_required
def cancel_request():
    try:
        pass
        #TODO: Add logic to cancel friend request
    except FriendshipException as e:
        flash(str(e))
    return redirect(url_for('main.home'))


@friendship.route('/listar', methods=['GET'])
@login_required
def get_friends():
    return render_template('friend_list.html', friends=current_user.friends)


@friendship.route('/remover', methods=['GET', 'POST'])
@login_required
def remove():
    pass
    #TODO: Add logic to remove friend


@friendship.route('/solicitacoes', methods=['GET'])
@login_required
def get_open_requests():
    return render_template('request_list.html', requests=current_user.pending_friend_requests)