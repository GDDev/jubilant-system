from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user

from .. import major_bp
from ..services import UserMajorService
from ..forms import NewUserMajorForm
from ..exceptions import MajorException


user_major_service = UserMajorService()


@major_bp.route('/adicionar/institucional/', methods=['GET', 'POST'])
def add_user_major():
    """
    Adds a Major to the current user.

    Returns:
        render_template: The rendered template for the add_user_major page.
        Or
        redirect: Redirects to the list_all page.
    """
    major_id = request.args.get('major_id')
    is_major_temp = request.args.get('is_major_temp')

    if not major_id:
        raise MajorException('Formação não informada.')

    form = NewUserMajorForm()
    try:
        if form.validate_on_submit():
            user_major_service.add(
                major_id=int(major_id) if is_major_temp == 'False' else None,
                temp_major_id=int(major_id) if is_major_temp == 'True' else None,
                profile_id=current_user.id,
                college_code=form.college_code.data,
                institutional_email=form.institutional_email.data,
                user_is=form.user_is.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data if not form.check_ongoing.data else None,
                approved=True if form.user_is.data.lower() == 'student' else False
            )
            return redirect(url_for('major.list_all'))
    except MajorException as e:
        flash(str(e))
    except Exception as e:
        flash(str(e))

    return render_template('new_user_major.html', form=form, major_id=major_id, is_major_temp=is_major_temp)

@major_bp.route('/remover/institucional/<int:user_major_id>', methods=['GET'])
def remove_from_user(user_major_id: int):
    """
    Removes a major from the current user.

    Args:
        user_major_id: int of the UserMajor's ID.

    Returns:
        redirect: Redirects to the list_all page.
    """
    try:
        user_major_service.remove(user_major_id)
    except MajorException as e:
        flash(str(e))

    return redirect(url_for('major.list_all'))

@major_bp.route('editar/institucional/<int:user_major_id>', methods=['GET', 'POST'])
def edit_user_major(user_major_id: int):
    """
    Updates a UserMajor.

    Args:
        user_major_id: int of the UserMajor's ID.

    Returns:
        render_template: The rendered template for the edit_user_major page.
        Or
        redirect: Redirects to the list_all page.
    """
    form = NewUserMajorForm()
    user_major = None
    try:
        user_major = user_major_service.find_by_id(user_major_id)
        if not user_major:
            raise MajorException('Formação não encontrada.')
        if form.validate_on_submit():
            user_major_service.update(
                user_major,
                college_code=form.college_code.data,
                institutional_email=form.institutional_email.data,
                user_is=form.user_is.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data if not form.check_ongoing.data else None,
            )
            return redirect(url_for('major.list_all'))
    except MajorException as e:
        flash(str(e))

    return render_template('edit_major.html', form=form, user_major=user_major)
