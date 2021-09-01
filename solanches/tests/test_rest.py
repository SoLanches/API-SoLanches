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

def test_get_comercios_vazio(client):
    response = client.get('/comercios')
    responseJson = response.json

    assert response.status_code == 200
    assert len(responseJson) == 0
    assert type(responseJson) == list

def test_get_comercios_sucesso(client, controller):
    comercio_name1, comercio_attr1 = "SoLanches Test", { "telefone": "91234-5678", "email": "solanches@test.com"}
    comercio_name2, comercio_attr2 = "Test", { "telefone": "98765-4321", "email": "test@test.com"}
    comercio_name3, comercio_attr3 = "SoLanchess", { "telefone": "91234-4321", "email": "solanchess@test.com"}

    comercio = controller.cadastra_comercio(comercio_name1, comercio_attr1)
    controller.cadastra_comercio(comercio_name2, comercio_attr2)
    controller.cadastra_comercio(comercio_name3, comercio_attr3)

    response = client.get('/comercios')
    responseJson = response.json
    
    assert response.status_code == 200
    assert len(responseJson) == 3
    assert type(responseJson) == list
    assert type(responseJson[0]) == dict
    assert type(responseJson[0]['_id']) == str
    assert type(responseJson[0]['nome']) == str
    assert type(responseJson[0]['cardapio']) == str
    assert type(responseJson[0]['created_at']) == float
    assert type(responseJson[0]['attributes']) == dict

    assert responseJson[0]['_id'] == comercio['_id']
    assert responseJson[0]['nome'] == comercio['nome']
    assert responseJson[0]['cardapio'] == comercio['cardapio']
    assert responseJson[0]['created_at'] == comercio['created_at']
    assert responseJson[0]['attributes']['email'] == comercio['attributes']['email']
    assert responseJson[1]['nome'] == comercio_name2
    assert responseJson[1]['attributes']['email'] == comercio_attr2['email']
    assert responseJson[2]['nome'] == comercio_name3
    assert responseJson[2]['attributes']['email'] == comercio_attr3['email']

def test_get_comercio_by_name_cadastrado(client, controller):
    comercio_nome = "SoLanches Test"
    comercio = controller.cadastra_comercio(comercio_nome, { "telefone": "91234-5678", "email": "solanches@test.com"})
    
    response = client.get(f'/comercio/{comercio_nome}')
    responseJson = response.json

    assert response.status_code == 200
    assert type(responseJson) == dict
    assert type(responseJson['_id']) == str
    assert type(responseJson['nome']) == str
    assert type(responseJson['cardapio']) == str
    assert type(responseJson['created_at']) == float
    assert type(responseJson['attributes']) == dict

    assert responseJson['_id'] == comercio['_id']
    assert responseJson['nome'] == comercio['nome']
    assert responseJson['cardapio'] == comercio['cardapio']
    assert responseJson['created_at'] == comercio['created_at']
    assert responseJson['attributes']['email'] == comercio['attributes']['email']
    assert responseJson['attributes']['telefone'] == comercio['attributes']['telefone']

def test_get_comercio_by_name_inexistente(client):
    comercio_nome = "SoLanches Test"
    
    response = client.get(f'/comercio/{comercio_nome}')
    responseJson = response.json

    assert response.status_code == 400
    assert responseJson['message'] == f'Erro: comercio com nome {comercio_nome} nao cadastrado!'
    assert responseJson['status_code'] == 400

def test_get_comercio_com_sucesso(client, controller):
    comercio = controller.cadastra_comercio("SoLanches Test", { "telefone": "91234-5678", "email": "solanches@test.com"})
    comercio_id = comercio['_id']

    response = client.get(f'/comercio?id={comercio_id}')
    responseJson = response.json

    assert response.status_code == 200
    assert responseJson['_id'] == comercio['_id']
    assert responseJson['nome'] == comercio['nome']
    assert responseJson['cardapio'] == comercio['cardapio']
    assert responseJson['created_at'] == comercio['created_at']
    assert responseJson['attributes']['email'] == comercio['attributes']['email']
    assert responseJson['attributes']['telefone'] == comercio['attributes']['telefone']

def test_get_comercio_inexistente(client):
    id_inexistente = "98765"

    response = client.get(f'/comercio?id={id_inexistente}')
    responseJson = response.json

    assert response.status_code == 400
    assert responseJson['message'] == f'Erro: comercio com id {id_inexistente} não cadastrado!'
    assert responseJson['status_code'] == 400
