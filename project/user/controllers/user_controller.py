from werkzeug.exceptions import HTTPException

from flask import redirect, render_template, session, request, url_for, flash
from flask_login import fresh_login_required, current_user, login_user, logout_user
from sqlalchemy.exc import SQLAlchemyError

from project.user import user
from ..services import UserService, UserProfileService
from ..exceptions import UserException

user_service = UserService()
user_profile_service = UserProfileService()


@user.route('/alterar_email', methods=['GET', 'POST'])
@fresh_login_required
def update_email():
    from re import fullmatch
    from utils.regex import re_email_open

    profile = current_user
    try:
        if request.method == 'POST':
            new_email = request.form.get('email')
            if not new_email or not new_email.strip():
                raise UserException('Email não pode ser vazio.')
            if not bool(fullmatch(re_email_open, new_email)):
                raise UserException('Email inválido.')
            if user_service.find_by_email(new_email):
                raise UserException('Email já cadastrado.')

            user_service.update_email(profile.user, new_email)

            profile = user_profile_service.new_alt_id(profile)

            login_user(profile)
            return redirect(url_for('perfil.settings'))
    except (HTTPException, UserException, Exception) as e:
        flash(str(e))
    return render_template('edit_email.html')

@user.route('/excluir', methods=['GET', 'POST'])
@fresh_login_required
def delete():
    if request.method == 'POST':
        c_user = current_user.user
        if c_user:
            try:
                if current_user.role == 'god':
                    raise Exception("Nuh Uh, Gods can't quit.")
                user_service.delete(c_user)
                logout_user()
                flash('Conta excluída com sucesso!')
            except (HTTPException, SQLAlchemyError, Exception) as e:
                flash(str(e))
                return redirect(url_for('perfil.settings'))
        return redirect(url_for('main.home'))
    return render_template('profile/delete_account.html')
