from unittest import mock

import pytest

from solanches.errors import *
from solanches.tests.data_test import *


@pytest.fixture
def client(rest):
    client = rest.app.test_client()
    return client


@pytest.fixture
def cardapio_cadastrado():
    cardapio_json = {
        "_id": "6b6aae29176271992b0278509f15a63900f1f1a9",
        "created_at": 1631415578.674395,
        "destaques": [],
        "produtos": []
    }
    return cardapio_json


@pytest.fixture
def comercio_cadastrado():
    comercio_json = {
        "_id": "idTest",
        "nome": "SoLanches Comercio", 
        "attributes": { "telefone": "99988-5678", "email": "solanches@test.com"},
        "created_at": 21345324.3456
    }
    return comercio_json


@pytest.fixture
def cardapio_cadastrado():
    cardapio_json = {
        "_id": "idTest",
        "created_at": 1631415578.674395,
        "destaques": [],
        "produtos": ["d763e108f053ad2354ff9285b70c48cfc770d9f7"]   
    }
    return cardapio_json


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
            "telefone": "123",
            "endereco": "rua",
            "horarios": "21h-23h"
        },
        "password": "6747838dd"
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
    assert response_json['message'] == "Erro: campo nome não informado!"


def test_cadastra_comercio_sem_senha(client):
    comercio_sem_nome = {
        "nome": "comercio_teste1",
        "attributes": {
            "telefone": "123",
            "endereco": "rua",
            "horarios": "21h-23h"
        }
    }
    url = '/comercio'
    response = client.post(url, json=comercio_sem_nome)
    response_json = response.json
    assert response.status_code == 400
    assert response_json['message'] ==  "Erro: campo senha não informado!"


def test_cadastra_comercio_sem_atributos(client):
    comercio_sem_atributos = {
        "nome": "comercio_teste1",
        "password": "6747838dd"
    }
    url = '/comercio'
    response = client.post(url, json=comercio_sem_atributos)
    response_json = response.json
    assert response.status_code == 400
    assert response_json['message'] == 'Erro: campo attributes não informado!'


def test_cadastra_comercio_com_json_invalido(client):
    comercio_json_invalido = "nao sou um json válido"
    url = '/comercio'
    response = client.post(url, data=comercio_json_invalido)
    response_json = response.json
    assert response.status_code == 400
    assert response_json['message'] == "Erro: json inválido!"


@mock.patch('solanches.rest.controller.cadastra_comercio')
def test_cadastra_comercio_exception_controller(mock_cadastra_comercio, client):
    exception_msg = "uma exceção ocorreu"
    mock_cadastra_comercio.side_effect = Exception(exception_msg)
    comercio = {
        "nome": "comercio_teste1",
        "password": "7373733",
        "attributes": {
            "endereco": "rua da lua"
        }
    }
    url = '/comercio'
    response = client.post(url, json=comercio)
    response_json = response.json
    assert response.status_code == 500
    assert response_json['message'] == exception_msg


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
    response_json = response.json
    assert response.status_code == 200
    assert response_json['message'] == f'comercio {comercio_nome} removido com sucesso'
    

@mock.patch('solanches.rest.controller.remove_comercio')
def test_remove_comercio_inexistente(mock_remove_comercio, client):
    comercio_nome = 'comercio_teste'
    exception_message = f'Erro: comercio com nome {comercio_nome} não cadastrado!'
    mock_remove_comercio.side_effect = SolanchesNotFoundError(exception_message)
    url = f'/comercio/{comercio_nome}'
    response = client.delete(url)
    response_json = response.json
    assert response.status_code == 404
    assert response_json['message'] == exception_message


@mock.patch('solanches.rest.controller.adiciona_destaque')
def test_adiciona_destaque_bad_request(mock_adiciona_destaque, client):
    exception_message = f'Erro: bad request'
    comercio_nome = 'comerciotest'
    produto_id = 'produtoid'
    mock_adiciona_destaque.side_effect = SolanchesBadRequestError(exception_message)
    url = f'/comercio/{comercio_nome}/destaques/{produto_id}'
    response = client.post(url)
    response_json = response.json
    assert response.status_code == 400
    assert response_json['message'] == exception_message


@mock.patch('solanches.rest.controller.adiciona_destaque')
def test_adiciona_destaque_not_found(mock_adiciona_destaque, client):
    exception_message = f'Erro: not found'
    comercio_nome = 'comerciotest'
    produto_id = 'produtoid'
    mock_adiciona_destaque.side_effect = SolanchesNotFoundError(exception_message)
    url = f'/comercio/{comercio_nome}/destaques/{produto_id}'
    response = client.post(url)
    response_json = response.json
    assert response.status_code == 404
    assert response_json['message'] == exception_message


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


def test_cadastra_produto_comercio_sem_nome(client):
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


@mock.patch('solanches.rest.controller.adiciona_destaque')
def test_adiciona_destaque_sucesso(mock_adiciona_destaque, client):
    exception_message = f'Erro: not found'
    comercio_nome = 'comerciotest'
    produto_id = 'produtoid'
    mock_adiciona_destaque.return_value = {'produtos': [], 'destaques': ['produto aleatorio', 'produto teste'], 'categorias': []}
    url = f'/comercio/{comercio_nome}/destaques/{produto_id}'
    response = client.post(url)
    response_json = response.json
    assert response.status_code == 201
    assert response_json == {'produtos': [], 'destaques': ['produto aleatorio', 'produto teste'], 'categorias': []}



@mock.patch('solanches.rest.controller.get_cardapio')
def test_get_cardapio_sucesso(mock_get_cardapio, client, cardapio_cadastrado):
    expected_return = cardapio_cadastrado
    mock_get_cardapio.return_value = expected_return
    response = client.get('/comercio/solanches/cardapio')
    response_json = response.json
    assert response.status_code == 200
    assert isinstance(response_json, dict)
    assert response_json == expected_return


@mock.patch('solanches.rest.controller.get_cardapio')
def test_get_cardapio_exception_controller(mock_get_cardapio, client):
    exception_msg = 'Exception no controller'
    expected_error = Exception(exception_msg)
    mock_get_cardapio.side_effect = expected_error

    response = client.get('/comercio/solanches/cardapio')
    response_json = response.json
    assert response.status_code == 500
    assert response_json['message'] == exception_msg


@mock.patch('solanches.rest.controller.get_produto')
def test_get_produto_by_id_sucesso(mock_get_produto, client):
    comercio_nome = 'comercio2'
    produto_id = '1231241'
    mock_get_produto.return_value = PRODUTO_TESTE
    url = f'/comercio/{comercio_nome}/produto/{produto_id}'
    response = client.get(url)
    response_json = response.json
    assert response.status_code == 200
    assert response_json == PRODUTO_TESTE


@mock.patch('solanches.rest.controller.get_produto')
def test_get_produto_by_id_inexistente(mock_get_produto, client):
    comercio_nome = 'comercio2'
    produto_id= '1231241'
    message = f'Erro: produto com o id {produto_id} não cadastrado no comercio!'
    mock_get_produto.side_effect = SolanchesNotFoundError(message)
    url = f'/comercio/{comercio_nome}/produto/{produto_id}'
    response = client.get(url)
    response_json = response.json
    assert response.status_code == 404
    assert response_json['message'] == message


@mock.patch('solanches.rest.controller.get_produtos')
def test_get_produtos(mock_get_produtos, client):
    comercio_nome = 'comercio2'
    mock_get_produtos.return_value = PRODUTOS_TESTE
    url = f'/comercio/{comercio_nome}/produtos'
    response = client.get(url)
    response_json = response.json
    assert response.status_code == 200
    assert response_json == PRODUTOS_TESTE


@mock.patch('solanches.rest.controller.remove_categoria')
def test_remove_categoria_erro(mock_remove_categoria, client):
    mensagem = f'Erro: no controller'
    mock_remove_categoria.side_effect= SolanchesBadRequestError(mensagem)
    comercio_nome = 'comercio1'
    categoria = {'categoria': 'salgados'}
    url = f'/comercio/{comercio_nome}/categoria'
    response = client.delete(url, json = categoria)
    response_json = response.json

    assert response.status_code == 400
    assert response_json['message'] == mensagem


@mock.patch('solanches.rest.controller.remove_categoria')
def test_remove_categoria_json_invalido(mock_remove_categoria, client):
    mensagem = "Erro: json inválido!"
    comercio_nome = 'comercio1'
    json_invalido = "não sou um json válido"
    url = f'/comercio/{comercio_nome}/categoria'
    response = client.delete(url, data=json_invalido)
    response_json = response.json
    assert response.status_code == 400
    assert response_json['message'] == mensagem


@mock.patch('solanches.rest.controller.remove_categoria')
def test_remove_categoria_nao_informada(mock_remove_categoria, client):
    mensagem = "Erro: categoria não informada!"
    comercio_nome = 'comercio1'
    json_sem_categoria = {"sem campo": "informado"}
    url = f'/comercio/{comercio_nome}/categoria'
    response = client.delete(url, json=json_sem_categoria)
    response_json = response.json
    assert response.status_code == 400
    assert response_json['message'] == mensagem


@mock.patch('solanches.rest.controller.remove_categoria')
def test_remove_categoria_sucesso(mock_remove_categoria, client):
    mock_remove_categoria.return_value = CARDAPIO_TESTE
    comercio_nome = 'comercio1'
    categoria = {'categoria': 'salgados'}
    url = f'/comercio/{comercio_nome}/categoria'
    response = client.delete(url, json = categoria)
    response_json = response.json
    assert response.status_code == 200
    assert response_json == CARDAPIO_TESTE
    

@mock.patch('solanches.rest.controller.remove_produto')
def test_remove_produto_sucesso(mock_remove_produto, client):
    mock_remove_produto.return_value = CARDAPIO_TESTE
    comercio_nome = 'comercio2'
    produto_id = 'idtesteproduto'
    url = f'/comercio/{comercio_nome}/produto/{produto_id}'
    response = client.delete(url)
    response_json = response.json
    assert response.status_code == 200
    assert response_json == CARDAPIO_TESTE


@mock.patch('solanches.rest.controller.remove_produto')
def test_remove_produto_comercio_inexistente(mock_remove_produto, client):
    comercio_nome = 'comercio inexistente'
    produto_id = 'idtesteproduto'
    exception_message = f'Erro: comercio com nome {comercio_nome} não cadastrado!'
    mock_remove_produto.side_effect = SolanchesNotFoundError(exception_message)
    url = f'/comercio/{comercio_nome}/produto/{produto_id}'
    response = client.delete(url)
    response_json = response.json
    assert response.status_code == 404
    assert response_json['message'] == exception_message


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


@mock.patch('solanches.rest.controller.atualiza_comercio')
def test_edita_comercio(mock_atualiza_comercio, client):
    updated_base = {
        "_id": "idTest",
        "nome": "SoLanches Comercio", 
        "attributes": { "telefone": "4002-8922", "email": "solanches@solania.com", "endereco": "rua floriano peixoto"},
        "created_at": 87443324.6475
    }
    mock_atualiza_comercio.return_value = updated_base
    response = client.patch("/comercio/solanches", json=updated_base)
    assert response.status_code == 200
    assert isinstance(response.json, dict)


@mock.patch('solanches.rest.controller.edita_produto')
def test_edita_produto(mock_atualiza_comercio, client):
    updated_base = {
        "_id": "d763e108f053ad2354ff9285b70c48cfc770d9f7",
        "attributes": {
            "categoria": "sa",
            "descricao": "descrição do produto de teste1",
            "imagem": "link de imagem",
            "preco": 20.5
        },
        "created_at": 1631415611.4404533,
        "nome": "comercio6"
    }
    mock_atualiza_comercio.return_value = updated_base
    response = client.patch("/comercio/solanches/produto/d763e108f053ad2354ff9285b70c48cfc770d9f7", json=updated_base)

    response_json = response.json
    assert response_json == updated_base
    assert response.status_code == 200


@mock.patch('solanches.rest.controller.get_cardapio')
def test_edita_produto_com_json_invalido(mock_get_cardapio, client, cardapio_cadastrado):
    comercio_json_invalido = 0

    mock_get_cardapio.return_value = [cardapio_cadastrado]
    url = '/comercio/solanches/produto/d763e108f053ad2354ff9285b70c48cfc770d9f7'
    response = client.patch(url, data=comercio_json_invalido)

    response_json = response.json
    assert response.status_code == 400
    assert response_json['message'] == "Erro: json inválido!"

