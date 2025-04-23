from flask import redirect, render_template, session, request, url_for
from flask_login import fresh_login_required, current_user

from project.user import user
from ..services import UserService, UserProfileService

user_service = UserService()
user_profile_service = UserProfileService()


@user.route('/alterar_email', methods=['GET', 'POST'])
@fresh_login_required
def update_email():
    profile = user_profile_service.find_by_id(session.get('profile_id'))
    c_user = user_service.find_by_id(session.get('user_id'))
    if request.method == 'POST':
        if request.form.get('btn') == 'Salvar':
            user_service.update_email(c_user, request.form.get('email'))
        return redirect(url_for('perfil.detail_profile', username=profile.username))
    return render_template('edit_email.html', profile=profile, user=c_user)

@user.route('/delete', methods=['POST'])
def delete_user():
    pass
