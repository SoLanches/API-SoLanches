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

def test_cadastra_comercio(client, controller):
    comercio_nome = 'test_comercio'
    controller.cadastra_comercio(comercio_nome, {'telefone': '83999999999'})
    url = '/comercio'
    response = client.post(url)
    responseJson = response.json
    assert response.status_code == 200
    assert responseJson['message'] == f'Erro: Comercio {comercio_nome} cadastrado com sucesso'
    assert responseJson['status_code'] == 200
    

def test_cadastro_comercio_ja_cadastrado(client, controller):
    comercio_nome = 'test_comercio'
    controller.cadastra_comercio(comercio_nome, {'telefone': '66666666666'})
    url = '/comercio'
    response = client.post(url)
    responseJson = response.json
    assert response.status_code == 400
    assert responseJson['message'] == f'Comércio já cadastrado no banco de dados'
    assert responseJson['status_code'] == 400
