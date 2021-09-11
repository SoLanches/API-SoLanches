import pytest
from unittest import mock

@pytest.fixture
def client(rest):
    client = rest.app.test_client()
    return client


def test_status(client):
    expected_keys = ["status", "timestamp", "started_at", "service"]
    response = client.get('/status')
    status = response.json
    assert response.status_code == 200
    assert all(key in status for key in expected_keys)
    assert type(status['status']) is str
    assert type(status['timestamp']) is float
    assert type(status['started_at']) is float
    assert type(status['service']) is str
    assert status['status'] == 'operacional'
    assert status['service'] == 'api-solanches'


@mock.patch('solanches.rest.controller.cadastra_comercio')
def test_cadastra_comercio(mock_cadastra_comercio, client):
    expected_return = {
        "nome": "comercio_teste1",
        "attributes": {
            "telefone": "123"
        }
    }
    comercio_json = expected_return
    mock_cadastra_comercio.return_value = expected_return
    response = client.post("/comercio", json=comercio_json)

    response_json = response.json
    assert response.status_code == 201
    assert response_json == expected_return


def test_cadastra_comercio_sem_nome(client):
    comercio_sem_nome = {
        "attributes": {
            "telefone": "123"
        }
    }
    url = '/comercio'
    response = client.post(url, json=comercio_sem_nome)
    response_json = response.json
    assert response.status_code == 400
    assert response_json['message'] == "Erro: nome não informado!"


def test_cadastra_comercio_sem_atributos(client):
    comercio_sem_atributos = {
        "nome": "comercio_teste2"
    }
    url = '/comercio'
    response = client.post(url, json=comercio_sem_atributos)
    response_json = response.json
    assert response.status_code == 400
    assert response_json['message'] == "Erro: atributos não informados!"


def test_cadastra_comercio_com_json_invalido(client):
    comercio_json_invalido = "nao sou um json válido"
    url = '/comercio'
    response = client.post(url, data=comercio_json_invalido)
    response_json = response.json
    assert response.status_code == 400
    assert response_json['message'] == "Erro: json inválido!"


#TODO: Exception no controller
