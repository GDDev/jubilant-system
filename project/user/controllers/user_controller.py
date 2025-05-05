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
    profile = user_profile_service.find_by_id(current_user.id)
    try:
        if request.method == 'POST':
            if request.form.get('btn') == 'Salvar':
                new_email = request.form.get('email')
                if not new_email or not new_email.strip():
                    raise UserException('Email não pode ser vazio.')
                if user_service.find_by_email(new_email):
                    raise UserException('Email já cadastrado.')
                profile = user_profile_service.new_alt_id(profile)
                user_service.update_email(profile.user, new_email)

                login_user(profile)
            return redirect(url_for('perfil.detail_profile', code=profile.code))
    except HTTPException as e:
        raise e
    except UserException as e:
        flash(str(e))
    return render_template('edit_email.html')

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
