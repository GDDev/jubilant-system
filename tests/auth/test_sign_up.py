import uuid

import pytest

from core import db

from project import create_app
from project.auth.exceptions import AuthException
from project.auth.services import AuthService
from project.user import User


@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield

@pytest.mark.usefixtures("app_context")
def test_user_profile_uuid_conflict(monkeypatch):
    fake_uuid = uuid.uuid4()
    monkeypatch.setattr("uuid.uuid4", lambda: fake_uuid)

    user_data_1 = {
        "email": "test1@example.com",
        "name": "User1",
        "surname": "User1"
    }

    profile_data_1 = {
        "username": "user1",
        "user_id": 3,
        "password": "123456"
    }

    user_data_2 = {
        "email": "test2@example.com",
        "name": "User2",
        "surname": "User2"
    }

    profile_data_2 = {
        "username": "user2",
        "user_id": 2,
        "password": "123456"
    }

    auth_service = AuthService()

    profile1 = auth_service.sign_up_user(user_data_1, profile_data_1)
    assert db.session.get(User, profile1.user_id) is not None, "Expected user1 to be persisted"

    with pytest.raises(AuthException, match="Erro interno ao cadastrar usuário, por favor tente novamente."):
        _ = auth_service.sign_up_user(user_data_2, profile_data_2)

    db.session.rollback()
    db.session.expire_all()

    # Now safely delete profile1 (this will also delete the User via cascade)
    db.session.delete(profile1.user)
    db.session.commit()

    assert db.session.get(User, profile_data_1['user_id']) is None, ("Expected user1 to be "
                                                                                            "deleted")
    assert db.session.get(User, profile_data_2['user_id']) is None, "Expected user2 to be deleted"
