# import uuid
#
# from utils import db
#
# from project.auth.services import AuthService
# from project.user import User
#
#
# def test_user_profile_uuid_conflict(app):
#     profile_id = uuid.uuid4()
#     alt_id = uuid.uuid4()
#
#     user_data_1 = {
#         "email": "test1@example.com",
#         "name": "User1",
#         "surname": "User1"
#     }
#
#     profile_data_1 = {
#         "id": profile_id,
#         "alt_id": alt_id,
#         "username": "user1",
#         "password": "123456"
#     }
#
#     user_data_2 = {
#         "email": "test2@example.com",
#         "name": "User2",
#         "surname": "User2"
#     }
#
#     profile_data_2 = {
#         "id": profile_id,
#         "alt_id": alt_id,
#         "username": "user2",
#         "password": "123456"
#     }
#
#     auth_service = AuthService()
#
#     profile1 = auth_service.sign_up_user(user_data_1, profile_data_1)
#     user_id1 = profile1.user_id
#     assert db.session.get(User, profile1.user_id) is not None, "Expected user1 to be persisted"
#
#     profile2 = auth_service.sign_up_user(user_data_2, profile_data_2)
#     user_id2 = profile2.user_id
#     assert db.session.get(User, profile2.user_id) is not None, "Expected user2 to be persisted"
#
#     db.session.expire_all()
#
#     db.session.delete(profile1.user)
#     db.session.delete(profile2.user)
#     db.session.commit()
#
#     assert db.session.get(User, user_id1) is None, "Expected user1 to be deleted"
#     assert db.session.get(User, user_id2) is None, "Expected user2 to be deleted"
