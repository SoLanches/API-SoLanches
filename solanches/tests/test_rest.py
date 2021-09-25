from unittest import mock
import pytest

from solanches.errors import SolanchesNotFoundError


@pytest.fixture
def client(rest):
    client = rest.app.test_client()
    return client


@pytest.fixture
def comercio_cadastrado():
    comercio_json = {
        "_id": "idTest",
        "nome": "SoLanches Comercio", 
        "attributes": { "telefone": "99988-5678", "email": "solanches@test.com"},
        "created_at": 21345324.3456
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


@mock.patch('solanches.rest.controller.get_comercios')
def test_get_comercios_vazio(mock_get_comercios, client):
    expected_return = []
    mock_get_comercios.return_value = expected_return

    response = client.get('/comercios')
    response_json = response.json

    assert response.status_code == 200
    assert isinstance(response_json, list)
    assert response_json == expected_return


@mock.patch('solanches.rest.controller.get_comercios')
def test_get_comercios_categories_false(mock_get_comercios, client):
    expected_return = []
    mock_get_comercios.return_value = expected_return

    response = client.get('/comercios?categories=false')
    response_json = response.json

    assert response.status_code == 200
    assert isinstance(response_json, list)
    assert response_json == expected_return


@mock.patch('solanches.rest.controller.get_comercios')
def test_get_comercios_categories_true(mock_get_comercios, client):
    expected_return = {}
    mock_get_comercios.return_value = expected_return

    response = client.get('/comercios?categories=true')
    response_json = response.json

    assert response.status_code == 200
    assert isinstance(response_json, dict)
    assert response_json == expected_return
    

@mock.patch('solanches.rest.controller.get_comercios')
def test_get_comercios_sucesso(mock_get_comercios, comercio_cadastrado, client):
    expected_return = [comercio_cadastrado]

    mock_get_comercios.return_value = expected_return

    response = client.get('/comercios')
    response_json = response.json
    
    assert response.status_code == 200
    assert response_json == expected_return


@mock.patch('solanches.rest.controller.get_comercios')
def test_get_comercios_exception_controller(mock_get_comercios, client):
    exception_msg = 'Exception no controller'
    expected_error = Exception(exception_msg)
    mock_get_comercios.side_effect = expected_error

    response = client.get(f'/comercios')
    response_json = response.json

    assert response.status_code == 500
    assert response_json['message'] == exception_msg


@mock.patch('solanches.rest.controller.get_comercio_by_name')
def test_get_comercio_by_name_sucesso(mock_get_comercio_by_name, client, comercio_cadastrado):
    expected_return = comercio_cadastrado
    nome = expected_return['nome']

    mock_get_comercio_by_name.return_value = expected_return
    response = client.get(f'/comercio/{nome}')
    response_json = response.json

    assert response.status_code == 200
    assert response_json == expected_return


@mock.patch('solanches.rest.controller.get_comercio_by_name')
def test_get_comercio_by_name_exception_controller(mock_get_comercio_by_name, client):
    nome = "Sem nome"
    exception_msg = 'Exception no controller'
    expected_error = Exception(exception_msg)
    mock_get_comercio_by_name.side_effect = expected_error

    response = client.get(f'/comercio/{nome}')
    response_json = response.json

    assert response.status_code == 500
    assert response_json['message'] == exception_msg


@mock.patch('solanches.rest.controller.get_comercio_by_id')
def test_get_comercio_by_id_com_sucesso(mock_get_comercio, client, comercio_cadastrado):
    expected_return = comercio_cadastrado
    mock_get_comercio.return_value = expected_return
    id = expected_return['_id']
    response = client.get(f'/comercio?id={id}')
    assert response.status_code == 200
    assert response.json == expected_return


@mock.patch('solanches.rest.controller.get_comercio_by_id')
def test_get_comercio_by_id_exception_no_controller(mock_get_comercio, client):
    comercio_id = "irrelevante"
    exception_msg = 'exception no controller'
    expected_error = Exception(exception_msg)

    mock_get_comercio.side_effect = expected_error
    response = client.get(f'/comercio?id={comercio_id}')
    response_json = response.json

    assert response.status_code == 500
    assert response_json['message'] == exception_msg


def test_get_comercio_by_id_sem_informar_id(client):
    exception_msg = f'Erro: id do comercio não informado!'
    response = client.get(f'/comercio')
    response_json = response.json
    assert response.status_code == 400
    assert response_json['message'] == exception_msg


@mock.patch('solanches.rest.controller.remove_comercio')
def test_remove_comercio_sucesso(mock_remove_comercio, client):
    comercio_nome = 'comercio_teste'
    mock_remove_comercio.return_value = 1
    url = f'/comercio/{comercio_nome}'
    response = client.delete(url)
    responseJson = response.json
    assert response.status_code == 200
    assert responseJson['message'] == f'comercio {comercio_nome} removido com sucesso'
    

@mock.patch('solanches.rest.controller.remove_comercio')
def test_remove_comercio_inexistente(mock_remove_comercio, client):
    comercio_nome = 'comercio_teste'
    exception_message = f'Erro: comercio com nome {comercio_nome} não cadastrado!'
    mock_remove_comercio.side_effect = SolanchesNotFoundError(exception_message)
    url = f'/comercio/{comercio_nome}'
    response = client.delete(url)
    responseJson = response.json
    assert response.status_code == 404
    assert responseJson['message'] == exception_message


@mock.patch('solanches.rest.controller.atualiza_comercio')
@mock.patch('solanches.rest.controller.get_comercio_by_name')
def test_edita_comercio(mock_get_comercio_by_name, mock_atualiza_comercio, client):
    updated_base = {
        "_id": "id_mockado",
        "nome": "solanches", 
        "attributes": { "telefone": "4002-8922", "email": "solanches@solania.com", "endereco": "rua floriano peixoto"},
        "created_at": 21345324.3456
    }
    
    mock_get_comercio_by_name.return_value = comercio_cadastrado
    mock_atualiza_comercio.return_value = updated_base
    response = client.patch("/comercio/solanches", json=updated_base)

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


@mock.patch('solanches.rest.controller.atualiza_comercio')
@mock.patch('solanches.rest.controller.get_comercio_by_name')
def test_edita_comercio(mock_get_comercio_by_name, mock_atualiza_comercio, client):
    updated_base = {
        "_id": "idTest",
        "nome": "SoLanches Comercio", 
        "attributes": { "telefone": "4002-8922", "email": "solanches@solania.com", "endereco": "rua floriano peixoto"},
        "created_at": 87443324.6475
    }
    
    mock_get_comercio_by_name.return_value = comercio_cadastrado
    mock_atualiza_comercio.return_value = updated_base
    response = client.patch("/comercio/solanches", json=updated_base)

    response_json = response.json
    assert response_json == updated_base
    assert response.status_code == 200


def test_edita_comercio_com_json_invalido(client):
    comercio_json_invalido = 0
    url = '/comercio/solanches'
    response = client.patch(url, data=comercio_json_invalido)

    response_json = response.json
    assert response.status_code == 400
    assert response_json['message'] == "Erro: json inválido!"


def test_edita_comercio_sem_atributos(client):
    
    comercio_sem_atributos = {
        "nome": "comercio_teste1"
    }
    url = '/comercio/solanches'
    response = client.patch(url, json=comercio_sem_atributos)
    response_json = response.json

    assert response.status_code == 400
    assert isinstance(response_json, dict)
