from werkzeug.exceptions import HTTPException

from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user

from core import db
from project.user import profile
from ..services import UserService, UserProfileService

user_service = UserService()
user_profile_service = UserProfileService()


@profile.route('/<string:code>', methods=['GET', 'POST'])
@login_required
def detail_profile(code: str):
    try:
        if code == current_user.code:
            session['profile_id'] = current_user.id
            session['user_id'] = current_user.user.id
            return render_template('profile/owner_view.html', profile=current_user)

        user_profile = user_profile_service.find_by_code(code)
        friendship, sender = user_profile_service.friendship_request(current_user, user_profile)
        return render_template(
            'profile/visitor_view.html',
            profile=user_profile,
            friendship=friendship,
            sender=sender
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        flash(str(e))
    return redirect(url_for('main.home'))

@profile.route('/update', methods=['POST'])
@login_required
def update_profile():
    pass
    #TODO: Add logic to update profile

@profile.route('/encontrar', methods=['GET', 'POST'])
@login_required
def find():
    search = request.form.get('search')
    profiles = []
    try:
        profiles = user_profile_service.find_profiles_by_search(search)
    except Exception as e:
        flash(str(e))
    return render_template('profile_list.html', profiles=profiles, search=search)

@profile.route('/selecionar_supervisor', methods=['POST'])
@login_required
def select_supervisor():
    sup_id = request.form.get('supervisor_id')
    if user_profile_service.find_by_id(sup_id):
        #TODO: add logic to send notification to chosen user before setting as supervisor.

        # current_user.supervisor_id = sup_id
        # db.session.commit()
        user_profile_service.update(current_user, supervisor_id=sup_id)

    return redirect(url_for('perfil.detail_profile', code=current_user.code))
