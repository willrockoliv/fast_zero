from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.models import User
from fast_zero.schemas import UserPublic


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


def test_update_user(client: TestClient, user: User, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'luana',
            'email': 'luana@example.com',
            'password': 'mynewpassword',
            'id': user.id,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'luana',
        'email': 'luana@example.com',
        'id': 1,
    }


def test_update_wrong_user(client: TestClient, user: User, token):
    response = client.put(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'luana',
            'email': 'luana@example.com',
            'password': 'mynewpassword',
            'id': user.id,
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}



def test_delete_user(client: TestClient, user: User, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_wrong_user(client: TestClient, user: User, token):
    response = client.delete(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
