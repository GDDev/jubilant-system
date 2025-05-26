from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user

from .. import major_bp
from ..services import UserMajorService
from ..forms import NewUserMajorForm
from ..exceptions import MajorException


user_major_service = UserMajorService()


@major_bp.route('/adicionar/institucional', methods=['GET', 'POST'])
def add_user_major():
    major_id = request.args.get('major_id')
    form = NewUserMajorForm()
    try:
        if form.validate_on_submit():
            user_major_service.add(
                profile_id=current_user.id,
                major_id=request.form.get('major_id'),
                college_code=form.college_code.data,
                institutional_email=form.institutional_email.data,
                user_is=form.user_is.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data if not form.check_ongoing.data else None,
                approved=True if form.user_is.data.lower() == 'estudante' else False
            )
            return redirect(url_for('major.list_all'))
    except MajorException as e:
        flash(str(e))

    return render_template('new_user_major.html', form=form, major_id=major_id)
