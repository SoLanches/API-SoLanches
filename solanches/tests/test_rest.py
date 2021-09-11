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

@mock.patch('solanches.rest.controller.get_comercios')
def test_get_comercios_vazio(mock_get_comercios, client):
    expected_return = []
    
    response = client.get('/comercios')
    response_json = response.json

    mock_get_comercios.return_value = response_json

    assert response.status_code == 200
    assert len(response_json) == 0
    assert type(response_json) == list
    assert response_json == expected_return

@mock.patch('solanches.rest.controller.get_comercios')
def test_get_comercios_sucesso(mock_get_comercios, client):
    comercio_nome, comercio_attr = "SoLanches Test", { "telefone": "91234-5678", "email": "solanches@test.com"}
    expected_return = {
        "_id": "",
        "nome": comercio_nome,
        "cardapio": "23232",
        "created_at": 1212.11,
        "attributes": comercio_attr
    }

    mock_get_comercios.return_value = expected_return

    response = client.get('/comercios')
    response_json = response.json
    
    assert response.status_code == 200
    assert type(response_json) == dict
    assert type(response_json['_id']) == str
    assert type(response_json['nome']) == str
    assert type(response_json['cardapio']) == str
    assert type(response_json['created_at']) == float
    assert type(response_json['attributes']) == dict
    assert response_json == expected_return

def test_get_comercio_by_name_cadastrado(mock_get_comercio_by_name, client):
    comercio_nome, comercio_attr = "SoLanches Test", { "telefone": "91234-5678", "email": "solanches@test.com"}
    expected_return = {
        "_id": "",
        "nome": comercio_nome,
        "cardapio": "23232",
        "created_at": 1212.11,
        "attributes": comercio_attr
    }

    mock_get_comercio_by_name.return_value = expected_return
    response = client.get(f'/comercio/{comercio_nome}')
    response_json = response.json

    assert response.status_code == 200
    assert type(response_json) == dict
    assert type(response_json['_id']) == str
    assert type(response_json['nome']) == str
    assert type(response_json['cardapio']) == str
    assert type(response_json['created_at']) == float
    assert type(response_json['attributes']) == dict
    assert response_json == expected_return

@mock.patch('solanches.rest.controller.get_comercio_by_name')
def test_get_comercio_by_name_inexistente(mock_get_comercio_by_name, client):
    comercio_nome = "SoLanches Test"
    expected_error = f'Erro: comercio com nome {comercio_nome} nao cadastrado!'
    
    mock_get_comercio_by_name.side_effect = expected_error
    response = client.get(f'/comercio/{comercio_nome}')
    response_json = response.json

    assert response.status_code == 400
    assert response_json['message'] == expected_error
    assert response_json['status_code'] == 400
    assert response_json == expected_error

@mock.patch('solanches.rest.controller.get_comercio_by_name')
def test_get_comercio_by_name_sem_informar_nome(mock_get_comercio_by_name, client):
    expected_error = f'Erro: nome de comercio inválido!'
    
    mock_get_comercio_by_name.side_effect = expected_error
    
    response = client.get(f'/comercio/')
    response_json = response.json

    assert response.status_code == 400
    assert response_json == expected_error


@mock.patch('solanches.rest.controller.get_comercio')
def test_get_comercio_com_sucesso(mock_get_comercio, client):
    expected_return = {
        "_id": "",
        "nome": "nome",
        "cardapio": "23232",
        "created_at": 1212.11,
        "attributes": {"telefone": "121212" }
    }

    mock_get_comercio.return_value = expected_return


@mock.patch('solanches.rest.controller.get_comercio')
def test_get_comercio_inexistente(mock_get_comercio, client):
    id_inexistente = "98765"
    expected_error = f'Erro: comercio com id {id_inexistente} não cadastrado!'

    mock_get_comercio.side_effect = expected_error

    response = client.get(f'/comercio?id={id_inexistente}')
    response_json = response.json

    assert response.status_code == 400
    assert response_json['message'] == expected_error

@mock.patch('solanches.rest.controller.get_comercio')
def test_get_comercio_sem_informar_id(mock_get_comercio, client):
    expected_error = f'Erro: id do comercio não informado!'

    mock_get_comercio.side_effect = expected_error

    response = client.get(f'/comercio?id=')
    response_json = response.json

    assert response.status_code == 400
    assert response_json['message'] == expected_error