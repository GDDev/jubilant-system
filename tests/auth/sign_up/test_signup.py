# def test_signup(client):
#     response = client.post("/auth/cadastrar", data={
#         'name': 'Test',
#         'surname': 'Ing',
#         'email': 'testing@gmail.com',
#         'username': 'testing',
#         'pwd': 'password',
#         'pwd2': 'password',
#         'accept_terms': 'on'
#     }, follow_redirects=True)
#
#     assert response.status_code == 200
#     assert response.request.path == '/postagem/feed'
