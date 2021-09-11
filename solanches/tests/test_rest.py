from attr import attributes
import pytest
from unittest import mock

@pytest.fixture
def client(rest):
    client = rest.app.test_client()
    return client

@pytest.fixture
def comercio(client):
    comercio_json = {
        "nome": "SoLanches Comercio", 
        "attributes": { "telefone": "99988-5678", "email": "solanches@test.com"}
        }
    return client.post('/comercio', json=comercio_json)


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
def test_get_comercios_categories(mock_get_comercios, client):
    expected_return = []
    

@mock.patch('solanches.rest.controller.get_comercios')
def test_get_comercios_sucesso(mock_get_comercios, client, comercio):
    expected_return = [comercio.json]

    mock_get_comercios.return_value = expected_return

    response = client.get('/comercios')
    response_json = response.json
    
    assert response.status_code == 200
    assert response_json == expected_return

def test_get_comercio_by_name_cadastrado(mock_get_comercio_by_name, client, comercio):
    expected_return = comercio.json
    nome = expected_return['nome']

    mock_get_comercio_by_name.return_value = expected_return
    response = client.get(f'/comercio/{nome}')
    response_json = response.json

    assert response.status_code == 200
    assert response_json == expected_return

@mock.patch('solanches.rest.controller.get_comercio_by_name')
def test_get_comercio_by_name_inexistente(mock_get_comercio_by_name, client):
    nome_teste = "Sem nome"
    expected_error = f'Erro: comercio com nome {nome_teste} nao cadastrado!'
    
    mock_get_comercio_by_name.side_effect = expected_error
    response = client.get(f'/comercio/{nome_teste}')
    response_json = response.json

    assert response.status_code == 400
    assert response_json['message'] == expected_error

@mock.patch('solanches.rest.controller.get_comercio_by_name')
def test_get_comercio_by_name_sem_informar_nome(mock_get_comercio_by_name, client):
    expected_error = f'Erro: nome de comercio inválido!'
    
    mock_get_comercio_by_name.side_effect = expected_error
    
    response = client.get(f'/comercio/')
    response_json = response.json

    assert response.status_code == 400
    assert response_json == expected_error


@mock.patch('solanches.rest.controller.get_comercio')
def test_get_comercio_com_sucesso(mock_get_comercio, client, comercio):
    expected_return = comercio.json
    mock_get_comercio.return_value = expected_return
    print(expected_return)
    id = expected_return['_id']
    response = client.get(f'/comercio?id={id}')

    assert response.status_code == 200
    assert response.json == expected_return


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