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


@mock.patch('solanches.rest.controller.cadastra_produto')
def test_cadastra_produto(mock_cadastra_produto, client):
    
    expected_return = {
        "nome": "produto teste7",
        "attributes":{
            "descricao": "descrição do produto de teste1",
            "imagem": "link de imagem",
            "preco": 20.50,
            "categoria": "salgados"
        }
    }

    produto_json = expected_return
    mock_cadastra_produto.return_value = expected_return
    response = client.post("/comercio/<comercio_nome>/produto", json=produto_json)

    response_json = response.json
    assert response.status_code == 201
    assert response_json == expected_return


def test_cadastra_produto_com_json_invalido(client):
    produto_json_invalido = "nao sou um json válido"
    url = '/comercio/<comercio_nome>/produto'
    response = client.post(url, data=produto_json_invalido)
    response_json = response.json
    assert response.status_code == 400
    assert response_json['message'] == "Erro: json inválido!"


def test_produto_comercio_sem_nome(client):
    produto_sem_nome = {
        "attributes": {
            "descricao": "descrição do produto de teste1",
            "imagem": "link de imagem",
            "categoria": "salgados"
        }
    }
    url = '/comercio/<comercio_nome>/produto'
    response = client.post(url, json=produto_sem_nome)
    response_json = response.json
    assert response.status_code == 400
    assert response_json['message'] == "Erro: nome não informado!"