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
    assert responseJson['message'] == f'Comercio {comercio_nome} cadastrado com sucesso.'
    assert responseJson['status_code'] == 200
    

def test_cadastra_comercio_nome_nulo(client, controller):
    controller.cadastra_comercio(None, {'telefone': '83999999999'})
    url = '/comercio'
    response = client.post(url)
    responseJson = response.json
    assert response.status_code == 400
    assert responseJson['message'] == f'Erro: Comercio com nome nulo nao pode ser cadastrado.'
    assert responseJson['status_code'] == 400


def test_cadastra_comercio_sem_telefone(client, controller):
    controller.cadastra_comercio(None, {'endereco': 'floriano peixoto'})
    url = '/comercio'
    response = client.post(url)
    responseJson = response.json
    assert response.status_code == 400
    assert responseJson['message'] == f'Erro: Comercio nao pode cadastrar sem informar um telefone.'
    assert responseJson['status_code'] == 400


def test_cadastro_comercio_ja_cadastrado(client, controller):
    comercio_nome = 'test_comercio'
    controller.cadastra_comercio(comercio_nome, {'telefone': '66666666666'})
    url = '/comercio'
    response = client.post(url)
    responseJson = response.json
    assert response.status_code == 400
    assert responseJson['message'] == 'Erro: Comércio já cadastrado no banco de dados'
    assert responseJson['status_code'] == 400

