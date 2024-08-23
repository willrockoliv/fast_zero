from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_get_html_deve_retornar_ok_e_ola_mundo_em_html(client):
    expected_response = """
        <html>
        <head>
            <title> Nosso olá mundo!</title>
        </head>
        <body>
            <h1> Olá Mundo </h1>
        </body>
        </html>
    """

    response = client.get('/html/')

    assert response.status_code == HTTPStatus.OK
    assert response.text == expected_response


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'luana',
            'email': 'luana@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'luana',
        'email': 'luana@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'luana',
                'email': 'luana@example.com',
                'id': 1,
            }
        ]
    }


def test_read_users_by_id(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'luana',
        'email': 'luana@example.com',
        'id': 1,
    }


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'luana',
            'email': 'luana@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'luana',
        'email': 'luana@example.com',
        'id': 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/9999',
        json={
            'username': 'luana',
            'email': 'luana@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
