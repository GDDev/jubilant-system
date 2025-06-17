# from utils import db
# from project.major import MajorEnum, UserMajor
#
#
# def test_edit_major(app, client, user, user_major):
#     client.post('/auth/entrar', data={
#         'user': user.username,
#         'pwd': 'senha'
#     }, follow_redirects=True)
#
#     assert user_major.college_code == '11223344556'
#
#     response = client.post(
#         f"/formacao/editar/institucional/{user_major.id}",
#         data={
#             "college_code": "11223344566",
#             "institutional_email": "11223344566@alunos.uni.com",
#             "user_is": 'STUDENT',
#             "start_date": "2024-01-01"
#         },
#         follow_redirects=True,
#     )
#
#     user_major = db.session.get(UserMajor, user_major.id)
#
#     assert response.status_code == 200
#     assert 'formacao/listar' in response.request.path
#
#     assert not user_major.college_code == '11223344556'
#     assert user_major.college_code == '11223344566'
