import uuid

import pytest
from werkzeug.security import generate_password_hash

from project import create_app
from utils import db
from project.major import Major, UserMajor, MajorEnum
from project.testing_config import TestingConfig
from project.user import User, UserProfile
from project.user.models.user_profile import RoleEnum

from datetime import date

@pytest.fixture()
def app():
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def add_user(app, **kwargs):
    with app.app_context():
        user = (User(
            name=kwargs.get('name'),
            surname=kwargs.get('surname'),
            email=kwargs.get('email')
        ))
        db.session.add(user)
        db.session.flush()
        db.session.add(UserProfile(
            id = str(uuid.uuid4()),
            alt_id = str(uuid.uuid4()),
            user_id=user.id,
            username=kwargs.get('username'),
            pwd=kwargs.get('pwd'),
            role=kwargs.get('role') or RoleEnum.USER
        ))
        db.session.commit()
        return user.profile

@pytest.fixture()
def user(app):
    return add_user(
        app,
        name='Test',
        surname='Ing',
        email='testing@gmail.com',
        username='testing',
        pwd=generate_password_hash('senha')
    )
    # with app.app_context():
    #     user = User(
    #         name='Test',
    #         surname='Ing',
    #         email='testing@gmail.com'
    #     )
    #     db.session.add(user)
    #     db.session.flush()
    #     db.session.add(UserProfile(
    #         user_id=user.id,
    #         username='testing',
    #         pwd=generate_password_hash('senha')
    #     ))
    #     db.session.commit()
    #     return user.profile

@pytest.fixture()
def admin(app):
    return add_user(
        app,
        name='Ad',
        surname='min',
        email='admin@gmail.com',
        username='admin',
        pwd=generate_password_hash('senha'),
        role=RoleEnum.ADMIN
    )

@pytest.fixture()
def major_nutri(app):
    with app.app_context():
        major = Major(
            name='Nutrição',
            level='Bacharelado',
            university='Universidade de Mogi das Cruzes',
            uni_acronym='UMC',
            area_tag='Nutrição',
            morning='8.00 Semestres'
        )
        db.session.add(major)
        db.session.commit()
        db.session.refresh(major)
        return major

@pytest.fixture()
def user_major(app, user, major_nutri):
    with app.app_context():
        user_major = UserMajor(
            profile_id=user.id,
            major_id=major_nutri.id,
            college_code='11223344556',
            institutional_email='11223344566@alunos.uni.com',
            user_is=MajorEnum.STUDENT,
            start_date=date(year=2024, month=1, day=1),
            end_date=None,
            approved=True
        )
        db.session.add(user_major)
        db.session.commit()
        db.session.refresh(user_major)
        return user_major

@pytest.fixture()
def pe_student(app):
    with app.app_context():
        user = User(
            name='PE',
            surname='Student',
            email='pe.student@gmail.com'
        )
        db.session.add(user)
        db.session.flush()
        db.session.add(UserProfile(
            user_id=user.id,
            username='pe.student',
            pwd=generate_password_hash('senha')
        ))
        db.session.commit()
        return user.profile
