from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.models import User
from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client: TestClient):
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


def test_create_user(client: TestClient):
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


def test_read_users(client: TestClient):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_by_id(client: TestClient, user: User):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_read_users_with_users(client: TestClient, user: User):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client: TestClient, user: User):
    response = client.put(
        f'/users/{user.id}',
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


def test_update_user_not_found(client: TestClient):
    response = client.put(
        '/users/9999',
        json={
            'username': 'luana',
            'email': 'luana@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client: TestClient, user: User):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client: TestClient):
    response = client.delete('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
