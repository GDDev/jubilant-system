from flask import flash, render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required

from .. import major_bp
from ..services import UserMajorService
from ..forms import NewUserMajorForm
from ..exceptions import MajorException


user_major_service = UserMajorService()


@major_bp.route('/adicionar/institucional/', methods=['GET', 'POST'])
@login_required
def add_user_major():
    """
    Adds a Major to the current user.

    Returns:
        render_template: The rendered template for the add_user_major page.
        Or
        redirect: Redirects to the list_all page.
    """
    major_id = request.args.get('major_id')

    if not major_id:
        raise MajorException('Formação não informada.')

    form = NewUserMajorForm()
    try:
        if form.validate_on_submit():
            user_major = user_major_service.add(
                major_id=int(major_id),
                profile_id=current_user.id,
                user_is=form.user_is.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data if not form.check_ongoing.data else None
            )
            email = form.institutional_email.data
            if not email:
                flash('E-mail não informado. Por favor informe o e-mail para aprovar a sua formação.')
            else:
                user_major_service.send_institutional_email_verification(email, user_major.id)
            return redirect(url_for('major.list_all'))
    except MajorException as e:
        flash(str(e))
    except Exception as e:
        flash(str(e))

    return render_template('new_user_major.html', form=form, major_id=major_id)


@major_bp.route('/remover/institucional/<int:user_major_id>', methods=['GET'])
@login_required
def remove_from_user(user_major_id: int):
    """
    Removes a major from the current user.

    Args:
        user_major_id: int of the UserMajor's ID.

    Returns:
        redirect: Redirects to the list_all page.
    """
    try:
        user_major = user_major_service.find_by_id(user_major_id)
        if user_major:
            if user_major.profile_id != current_user.id:
                abort(403)
            user_major_service.remove(user_major_id)
    except MajorException as e:
        flash(str(e))

    return redirect(url_for('major.list_all'))


@major_bp.route('editar/institucional/', methods=['GET', 'POST'])
@login_required
def edit_user_major():
    """
    Updates a UserMajor.

    Args:
        user_major_id: int of the UserMajor's ID.

    Returns:
        render_template: The rendered template for the edit_user_major page.
        Or
        redirect: Redirects to the list_all page.
    """
    user_major_id = request.args.get('user_major_id')
    form = NewUserMajorForm()
    try:
        if not user_major_id:
            raise MajorException('ID não informado.')
        user_major = user_major_service.find_by_id(int(user_major_id))
        if not user_major:
            raise MajorException('Formação não encontrada.')
        if user_major.profile_id != current_user.id:
            abort(403)
        if form.validate_on_submit():
            user_major_service.update(
                user_major,
                user_is=form.user_is.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data
            )
            flash('Edições salvas com sucesso.')
        return render_template('edit_major.html', form=form, user_major=user_major)
    except MajorException as e:
        flash(str(e))
        return redirect(url_for('major.list_all'))


@major_bp.route('/reenviar_confirmacao', methods=['GET'])
@login_required
def resend_institutional_email_verification():
    from utils.regex import re_email_umc
    from re import fullmatch

    email = request.args.get('email')
    user_major_id = request.args.get('user_major_id')
    try:
        if not email:
            raise MajorException('E-mail não informado.')
        if not bool(fullmatch(re_email_umc, email)):
            raise MajorException('Email inválido.')
        if not user_major_id:
            raise MajorException('ID não informado.')
        user_major = user_major_service.find_by_id(int(user_major_id))
        if user_major.profile_id != current_user.id:
            abort(403)
        if user_major.user_is.value == 'estudante' and 'alunos' not in email:
            raise MajorException('Email informado não corresponde à alunos.')
        if user_major.user_is.value == 'professor' and 'alunos' in email:
            raise MajorException('Email informado não corresponde à professores.')

        user_major_service.send_institutional_email_verification(email, user_major_id)
        return redirect(url_for('major.edit_user_major', user_major_id=user_major_id))
    except (MajorException, Exception) as e:
        flash(str(e))
    return redirect(url_for('major.list_all'))
