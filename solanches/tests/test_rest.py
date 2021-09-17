from unittest import mock
import pytest

@pytest.fixture
def client(rest):
    client = rest.app.test_client()
    return client


@pytest.fixture
def comercio_cadastrado():
    comercio_json = {
        "_id": "id_mockado",
        "nome": "solanches", 
        "attributes": { "telefone": "4002-8922", "email": "solanches@solania.com"},
        "created_at": 87443324.6475
    }
    return comercio_json


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


@mock.patch('solanches.rest.controller.atualiza_comercio')
@mock.patch('solanches.rest.controller.get_comercio')
def test_edita_comercio(mock_get_comercio, mock_atualiza_comercio, client):
    updated_base = {
        "_id": "id_mockado",
        "nome": "solanches", 
        "attributes": { "telefone": "4002-8922", "email": "solanches@solania.com", "endereco": "rua floriano peixoto"},
        "created_at": 87443324.6475
    }
    
    mock_get_comercio.return_value = comercio_cadastrado
    mock_atualiza_comercio.return_value = updated_base
    response = client.patch("/comercio/solanches", json={"endereco": "rua floriano peixoto"})

    response_json = response.json
    assert response_json == updated_base
    assert response.status_code == 200


@mock.patch('solanches.rest.controller.get_comercio')
def test_edita_comercio_com_json_invalido(mock_get_comercio, client):
    comercio_json_invalido = 0

    mock_get_comercio.return_value = [comercio_cadastrado]
    url = '/comercio/solanches'
    response = client.patch(url, data=comercio_json_invalido)

    response_json = response.json
    assert response.status_code == 400
    assert response_json['message'] == "Erro: json inválido!"


@mock.patch('solanches.rest.controller.get_comercio')
def test_edita_comercio_sem_atributos(mock_get_comercio, client):
    
    comercio_sem_atributos = {
        "nome": "comercio_teste1"
    }
    mock_get_comercio.return_value = [comercio_cadastrado]
    url = '/comercio/solanches'
    response = client.patch(url, json=comercio_sem_atributos)
    response_json = response.json

    assert response.status_code == 400
    assert isinstance(response_json, dict)
