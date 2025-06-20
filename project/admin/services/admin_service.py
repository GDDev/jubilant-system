from flask import render_template, flash
from flask_login import current_user

from utils import db, send_mail, strip_lower
from project.friendship import Friendship
from project.post import Post
from project.routine import Routine
from project.user import User, UserException, UserProfileException
from project.user import UserProfileService, UserService


class AdminService:
    def __init__(self):
        self.profile_service = UserProfileService()
        self.user_service = UserService()

    @staticmethod
    def get_overall_stats():
        all_routines = db.session.query(Routine).all()
        all_workouts = [r for r in all_routines if r.type == 'workout']
        all_diets = [r for r in all_routines if r.type == 'dietary']

        return {
            'total_users':db.session.query(User).count(),
            'total_posts':db.session.query(Post).count(),
            'total_friends':db.session.query(Friendship).count(),
            'total_workouts':len(all_workouts),
            'total_diets':len(all_diets),
            'diet_workout_ratio':len(all_diets)/len(all_workouts) if all_workouts else 0,
            'workout_diet_ratio':len(all_workouts)/len(all_diets) if all_diets else 0,
            'total_routines':len(all_routines),
        }

    def change_name(self, profile, **kwargs):
        try:
            self.user_service.update(profile.user, name=kwargs.get('name'), surname=kwargs.get('surname'))
        except (UserException, Exception) as e:
            raise e

    def test_method_executable(self, p_id: str):
        if not p_id:
            raise Exception('ID não informado.')
        profile = self.profile_service.find_by_id(p_id)
        if not profile:
            raise Exception('Perfil não encontrado.')
        if current_user.role == 'admin' and profile.role == 'admin' and current_user.id != profile.id:
            raise Exception('Ação não permitida.')
        return profile

    def new_code(self, profile):
        from secrets import token_hex
        try:
            profile.code = token_hex(6)
            self.profile_service.update(profile)
        except (UserProfileException, Exception) as e:
            raise e

    def change_username(self, profile, username):
        try:
            profile.username = username
            self.profile_service.update(profile)
        except (UserProfileException, Exception) as e:
            raise e

    def change_email(self, profile, email):
        try:
            already_exists = self.user_service.find_by_email(email)
            if already_exists:
                raise Exception('Email já cadastrado.')
            profile.user.email = email
            self.user_service.update(profile.user)
        except (UserException, Exception) as e:
            raise e

    def new_password(self, profile):
        from secrets import token_urlsafe
        from werkzeug.security import generate_password_hash
        try:
            new_pwd = token_urlsafe(18)
            profile.pwd = generate_password_hash(new_pwd)
            self.profile_service.update(profile)

            html_body = render_template(
                'new_pwd.html',
                new_password=new_pwd,
                user_name=profile.user.name + " " + profile.user.surname
            )
            send_mail(
                subject='Nova Senha - Jubilant System',
                body='Nova senha referente a sua requisição',
                to=strip_lower(profile.user.email),
                html=html_body,
            )
        except Exception as e:
            raise e

    def promote_or_demote(self, profile):
        try:
            if profile.role == 'user':
                profile.role = 'admin'
                self.profile_service.update(profile)
                flash(f'{profile.username} promovido à administrador.')
            elif profile.role == 'admin':
                profile.role = 'user'
                self.profile_service.update(profile)
                flash(f'{profile.username} rebaixado à usuário.')
        except (UserProfileException, Exception) as e:
            raise e

    def delete(self, profile):
        try:
            self.user_service.delete(profile.user)
        except (UserException, Exception) as e:
            raise e
