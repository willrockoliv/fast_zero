from http import HTTPStatus

from fastapi.testclient import TestClient


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
