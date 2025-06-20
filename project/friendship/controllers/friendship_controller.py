from flask import redirect, flash, url_for, request, render_template, abort
from flask_login import current_user, login_required

from .. import friendship
from ..services import FriendshipService
from ..exceptions import FriendshipException

from ...notification import NotificationException, NotificationService, NotificationType

friendship_service = FriendshipService()
notification_service = NotificationService()


@friendship.route('/adicionar', methods=['GET'])
@login_required
def send_request():
    try:
        # Sends friend request
        new_friendship = friendship_service.send_request(request.args.get('friend_id'))
        # Sends notification to user receiving friend request
        notification_service.send_notification(
            receiver_id=request.args.get('friend_id'),
            sender_id=current_user.id,
            type=NotificationType.FRIEND_REQUEST,
            content=f'{current_user.user.name} {current_user.user.surname} te enviou uma solicitação de amizade.',
            url=url_for('perfil.detail_profile', code=current_user.code),
            friendship_id=new_friendship.id
        )
    except (FriendshipException, NotificationException) as e:
        flash(str(e))
    return redirect(url_for('perfil.detail_profile', code=request.args.get('friend_code')))


@friendship.route('/aceitar/<int:friendship_id>', methods=['GET', 'POST'])
@login_required
def accept_request(friendship_id: int):
    friend = friendship_service.find_by_id(friendship_id)
    try:
        if friend:
            if friend.receiver_id != current_user.id:
                abort(403)
            notification_service.delete_by_friendship_id(friend.id)
            friendship_service.accept_request(friend)
    except FriendshipException as e:
        flash(str(e))
    return redirect(url_for('main.home'))


@friendship.route('/recusar/<int:friendship_id>', methods=['GET', 'POST'])
@login_required
def decline_request(friendship_id: int):
    friend = friendship_service.find_by_id(friendship_id)
    try:
        if friend:
            if friend.receiver_id != current_user.id:
                abort(403)
            notification_service.delete_by_friendship_id(friendship_id)
            friendship_service.decline_request(friendship_id)
    except FriendshipException as e:
        flash(str(e))
    return redirect(url_for('main.home'))


@friendship.route('/remover/<int:friendship_id>', methods=['GET', 'POST'])
@login_required
def remove_friendship(friendship_id: int):
    friend = friendship_service.find_by_id(friendship_id)
    user_code = friend.receiver.code if friend else None
    try:
        if friend:
            if friend.receiver_id != current_user.id and friend.sender_id != current_user.id:
                abort(403)
            notification_service.delete_by_friendship_id(friend.id)
            friendship_service.remove_friendship(friend)
    except (FriendshipException, NotificationException) as e:
        flash(str(e))
    if friend:
        return redirect(url_for('perfil.detail_profile', code=user_code))
    return redirect(url_for('main.home'))


@friendship.route('/listar', methods=['GET'])
@login_required
def get_friends():
    suggestions = []
    try:
        suggestions = friendship_service.get_friend_suggestions()
    except FriendshipException as e:
        flash(str(e))
    return render_template('friend_list.html', friends=current_user.friends, suggestions=suggestions)
