from flask import redirect, render_template, session, request, url_for, flash
from flask_login import fresh_login_required, current_user, login_user, logout_user
from sqlalchemy.exc import SQLAlchemyError

from project.user import user
from ..services import UserService, UserProfileService
from ...auth.exceptions import AuthException

user_service = UserService()
user_profile_service = UserProfileService()


@user.route('/alterar_email', methods=['GET', 'POST'])
@fresh_login_required
def update_email():
    profile = user_profile_service.find_by_id(session.get('profile_id'))
    c_user = user_service.find_by_id(session.get('user_id'))
    if request.method == 'POST':
        if request.form.get('btn') == 'Salvar':
            try:
                if user_service.find_by_email(request.form.get('email')):
                    raise AuthException('Email já cadastrado.')
                profile = user_profile_service.new_alt_id(profile)
                c_user.profile = profile
                user_service.update_email(c_user, request.form.get('email'))

                login_user(profile)
            except AuthException as e:
                flash(str(e))
        return redirect(url_for('perfil.detail_profile', code=profile.code))
    return render_template('edit_email.html', profile=profile, user=c_user)

@user.route('/excluir', methods=['POST'])
@fresh_login_required
def delete():
    c_user = user_service.find_by_id(int(request.form.get('user_id')))
    if c_user:
        try:
            user_service.delete(c_user)
            logout_user()
            flash('Conta excluída com sucesso!')
        except SQLAlchemyError as e:
            flash(str(e))
            return redirect(url_for('perfil.detail_profile', code=current_user.code))
    return redirect(url_for('main.home'))
