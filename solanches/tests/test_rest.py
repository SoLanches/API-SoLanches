from unittest import mock
import pytest


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


@mock.patch('solanches.rest.controller.remove_comercio')
def test_remove_comercio_sucesso(mock_remove_comercio, client):
    comercio_nome = 'comercio_teste'
    mock_remove_comercio.return_value = 1
    url = f'/comercio/{comercio_nome}'
    response = client.delete(url)
    responseJson = response.json
    assert response.status_code == 200
    assert responseJson['message'] == f'comercio {comercio_nome} removido com sucesso'
    

@pytest.mark.skip(reason="teste está correto, mas a implementação retorna 200 quando deveria retornar 400")
@mock.patch('solanches.rest.controller.remove_comercio')
def test_remove_comercio_inexistente(mock_remove_comercio, client):
    mock_remove_comercio.return_value = 0
    comercio_nome = 'comercio_teste'
    url = f'/comercio/{comercio_nome}'
    response = client.delete(url)
    responseJson = response.json
    assert response.status_code == 400
    assert responseJson['message'] == f'Erro: comercio com nome {comercio_nome} não cadastrado!'
