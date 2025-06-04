def test_signin(client, user):
    response = client.post("/auth/entrar", data={
        'user': 'testing',
        'pwd': 'senha'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == '/postagem/feed'
