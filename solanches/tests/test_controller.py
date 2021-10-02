from unittest import mock
import copy

import pytest
from pymongo import errors

from solanches.tests.data_test import *
from solanches.errors import SolanchesNotFoundError
from solanches.errors import SolanchesBadRequestError


@pytest.fixture
def comercios():
    return copy.deepcopy(COMERCIOS)


@pytest.fixture
def um_comercio():
    return copy.deepcopy(COMERCIO)


@pytest.fixture
def um_produto():
    return copy.deepcopy(PRODUTO)


@pytest.fixture
def um_cardapio():
    return copy.deepcopy(CARDAPIO)


@pytest.fixture
def um_produto_editado():
    return copy.deepcopy(PRODUTO_EDITADO)


@pytest.fixture
def comercio_editado():
    return COMERCIO_EDITADO


@mock.patch('solanches.controller.Comercio.get_all')
def test_get_comercios_sistema_vazio_has_categories_true(mock_comercio_get_all, controller):
    mock_comercio_get_all.return_value = []
    has_categories = True
    result = controller.get_comercios(has_categories)
    assert isinstance(result, dict)


@mock.patch('solanches.controller._get_comercios_categoria')
@mock.patch('solanches.controller.Comercio.get_all')
def test_get_comercios_sistema_vazio_sem_has_categories(mock_comercio_get_all, mock_get_comercios_categoria, controller):
    mock_comercio_get_all.return_value = []
    result = controller.get_comercios()
    assert result == []
    assert not mock_get_comercios_categoria.called


@mock.patch('solanches.controller.Comercio.get_categoria')
@mock.patch('solanches.controller.Comercio.get_all')
def test_get_comercios_com_comercios_no_bd_categories_true(mock_comercio_get_all, mock_comercio_get_categoria, controller, comercios):
    mock_comercio_get_all.return_value = comercios
    mock_comercio_get_categoria.return_value = "categoria"
    has_categories = True
    result = controller.get_comercios(has_categories)
    assert isinstance(result, dict)
    assert "categoria" in result
    assert all(comercio in result.get("categoria") for comercio in comercios)


@mock.patch('solanches.controller._get_comercios_categoria')
@mock.patch('solanches.controller.Comercio.get_all')
def test_get_comercios_com_comercios_no_bd_sem_has_categories(mock_comercio_get_all, mock_get_comercios_categoria, controller, comercios):
    mock_comercio_get_all.return_value = comercios
    has_categories = False
    result = controller.get_comercios(has_categories)
    assert isinstance(result, list)
    assert not mock_get_comercios_categoria.called
    assert all(comercio in result for comercio in comercios)


@mock.patch('solanches.controller.Comercio.get_by_id')
def test_get_comercio_by_id_nao_cadastrado(mock_comercio_by_id, controller):
    id_invalido = "nao estou cadastrado"
    mock_comercio_by_id.return_value = None

    with pytest.raises(SolanchesNotFoundError) as excinfo:
        controller.get_comercio_by_id(id_invalido)
    assert str(excinfo.value.message) == f'Erro: comercio com id {id_invalido} não cadastrado!'


@mock.patch('solanches.controller.Comercio.get_by_id')
def test_get_comercio_by_id_com_id_nao_str(mock_comercio_by_id, controller):
    id_invalido = 123
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.get_comercio_by_id(id_invalido)
    assert str(excinfo.value.message) == f'Erro: comercio com id {id_invalido} inválido!'


@mock.patch('solanches.controller.Comercio.get_by_id')
def test_get_comercio_by_id_valido(mock_comercio_by_id, controller, um_comercio):
    id_valido = "id valido"
    expected_return = um_comercio
    mock_comercio_by_id.return_value = expected_return
    result = controller.get_comercio_by_id(id_valido)
    assert result == expected_return


@mock.patch('solanches.controller.Comercio.get_by_name')
def test_get_comercio_by_name_nao_cadastrado(mock_comercio_by_name, controller):
    nome_invalido = "nao estou cadastrado"
    mock_comercio_by_name.return_value = None

    with pytest.raises(SolanchesNotFoundError) as excinfo:
        controller.get_comercio_by_name(nome_invalido)
    assert str(excinfo.value.message) == f'Erro: comercio com o nome {nome_invalido} não cadastrado!'


def test_get_comercio_by_name_com_nome_nao_str(controller):
    nome_invalido = 123
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.get_comercio_by_name(nome_invalido)
    assert str(excinfo.value.message) == f'Erro: nome de comercio inválido!'


@mock.patch('solanches.controller.Comercio.get_by_name')
def test_get_comercio_by_name_valido(mock_comercio_by_name, controller, um_comercio):
    nome_valido = "id valido"
    expected_return = um_comercio
    mock_comercio_by_name.return_value = expected_return
    result = controller.get_comercio_by_name(nome_valido)
    assert result == expected_return


@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_comercio_inexistente(mock_comercio_by_name, controller):
    mock_comercio_by_name.return_value = None
    with pytest.raises(SolanchesNotFoundError) as excinfo:
        comercio_nome = 'comercio_sem_id'
        controller.remove_comercio(comercio_nome)
    assert str(excinfo.value.message) == f'Erro: comercio com o nome {comercio_nome} não cadastrado!'


def test_remove_comercio_nome_invalido(controller):
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        comercio_nome_invalido = None
        controller.remove_comercio(comercio_nome_invalido)
    assert str(excinfo.value.message) == f'Erro: nome de comercio invalido'


@mock.patch('solanches.controller.Comercio.get_by_name')
@mock.patch('solanches.controller.Comercio.get_cardapio')
def test_get_cardapio_sucesso(mock_get_cardapio, mock_comercio_by_name,controller, um_cardapio):
    mock_get_cardapio.return_value = um_cardapio
    mock_comercio_by_name.return_value = um_comercio

    nome_comercio = 'solanches'

    result = controller.get_cardapio(nome_comercio)
    assert result == CARDAPIO
    assert isinstance(result, dict)


def test_get_cardapio_by_nome_comercio_invalido(controller):
    nome_invalido = 123
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.get_cardapio(nome_invalido)
    assert str(excinfo.value.message) == 'Erro: nome de comercio inválido!'


@mock.patch('solanches.controller.Comercio.get_by_name')
@mock.patch('solanches.controller.Comercio.get_cardapio')
def test_get_cardapio_by_nome_comercio_valido(mock_get_cardapio, mock_comercio_by_name, controller, um_cardapio, um_comercio):
    mock_get_cardapio.return_value = um_cardapio
    mock_comercio_by_name.return_value = um_comercio
    nome = 'solanches'

    result = controller.get_cardapio(nome)

    assert result == um_cardapio
    assert isinstance(result, dict)


@mock.patch('solanches.controller.Comercio.get_cardapio')
def test_get_cardapio_nao_encontrado(mock_get_cardapio, controller):
    mock_get_cardapio.return_value = None
    nome = 'TEXAS'
    with pytest.raises(SolanchesNotFoundError) as excinfo:
        controller.get_cardapio(nome)
    assert str(excinfo.value.message) == 'Erro: comercio com o nome TEXAS não cadastrado!'


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produto')
def test_get_produto_by_id_sucesso(mock_get_produto, mock_get_by_name, controller):
    comercio_nome = 'comercio2'
    produto_id = '213123121e'
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produto.return_value = PRODUTO_TESTE

    result = controller.get_produto(comercio_nome, produto_id)
    assert result == PRODUTO_TESTE


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produto')
def test_get_produto_by_id_invalido(mock_get_produto, mock_get_by_name, controller):
    comercio_nome = 'comercio2'
    produto_id = 123
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.get_produto(comercio_nome, produto_id)
    assert str(excinfo.value.message) == "Erro: produto com id inválido!"


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produto')
def test_get_produto_by_id_comercio_inexistente(mock_get_produto, mock_get_by_name, controller):
    comercio_nome = 'comercio inexistente'
    produto_id = '213123121e'
    mock_get_by_name.return_value = None
    with pytest.raises(SolanchesNotFoundError) as excinfo:
        controller.get_produto(comercio_nome, produto_id)
    assert str(excinfo.value.message) == f'Erro: comercio com o nome {comercio_nome} não cadastrado!'


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produto')
def test_get_produto_by_id_inexistente(mock_get_produto, mock_get_by_name, controller):
    comercio_nome = 'comercio2'
    produto_id = '213123121e'
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produto.return_value = None
    with pytest.raises(SolanchesNotFoundError) as e:
        comercio_nome = 'comercio_sem_id'
        controller.get_produto(comercio_nome, produto_id)


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produtos')
def test_get_produtos_has_categories_false(mock_get_produtos, mock_get_by_name, controller):
    comercio_nome = 'comercio2'
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produtos.return_value = PRODUTOS_TESTE

    result = controller.get_produtos(comercio_nome, False)
    assert result == PRODUTOS_TESTE
    assert isinstance(result, list)


@mock.patch('solanches.models.Comercio.get_produto_categoria')
@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produtos')
def test_get_produtos_has_categories_true(mock_get_produtos, mock_get_by_name, mock_get_produto_categoria, controller):
    comercio_nome = 'comercio2'
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produtos.return_value = PRODUTOS_TESTE
    mock_get_produto_categoria.return_value = "categoria"

    result = controller.get_produtos(comercio_nome, True)
    assert all(produto in result.get("categoria") for produto in PRODUTOS_TESTE)
    assert isinstance(result, dict)


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produtos')
def test_get_produtos_comercio_inexistente(mock_get_produto, mock_get_by_name, controller):
    comercio_nome = 'nome qualquer'
    mock_get_by_name.return_value = None
    with pytest.raises(SolanchesNotFoundError) as e:
        controller.get_produtos(comercio_nome)
    assert str(e.value.message) == f'Erro: comercio com o nome {comercio_nome} não cadastrado!'


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produtos_ids')
def test_get_produtos_ids_comercio_inexistente(mock_get_produtos_ids, mock_get_by_name, controller):
    comercio_nome = 'nome qualquer'
    mock_get_by_name.return_value = None
    with pytest.raises(SolanchesNotFoundError) as e:
        controller.get_produtos_ids(comercio_nome)
    assert str(e.value.message) == f'Erro: comercio com o nome {comercio_nome} não cadastrado!'


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produtos_ids')
def test_get_produtos_ids_sucesso(mock_get_produtos_ids, mock_get_by_name, controller):
    comercio_nome = 'nome qualquer'
    expected_result = ["id1", "id2"]
    mock_get_by_name.return_value = um_comercio
    mock_get_produtos_ids.return_value = expected_result

    result = controller.get_produtos_ids(comercio_nome)
    assert result == expected_result


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.remove_comercio')
def test_remove_comercio_sucesso(mock_remove_comercio, mock_get_by_name,  controller):
    comercio_nome = 'comercio_test'
    mock_get_by_name.return_value = {'produtos': []}
    mock_remove_comercio.return_value = 1
    result = controller.remove_comercio(comercio_nome)
    assert result == 1


def test_edita_comercio_com_nome_invalido(controller):
    nome_invalido = 18189
    attributes = {"endereco": "2344222"}
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.atualiza_comercio(attributes, nome_invalido)
    assert str(excinfo.value.message) == 'Erro: nome de comercio inválido!'


def test_edita_comercio_atributos_invalidos(controller):
    nome_comercio = "comercio1"
    attributes = "atributos"
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.atualiza_comercio(attributes, nome_comercio)
    assert str(excinfo.value.message) == "Erro: campo attributes inválidos!"


@mock.patch('solanches.models.Comercio.get_by_name')
def test_edita_comercio_nao_cadastrado(mock_get_by_name, controller):
    nome_comercio = "comercio1"
    attributes = {"endereco": "2344222"}
    mock_get_by_name.return_value = None
    with pytest.raises(SolanchesNotFoundError) as excinfo:
        controller.atualiza_comercio(attributes, nome_comercio)
    assert str(excinfo.value.message) == 'Erro: comercio com o nome comercio1 não cadastrado!'


@mock.patch('solanches.controller.Comercio.update')
@mock.patch('solanches.controller.Comercio.get_by_name')
def test_edita_comercio_sucesso(mock_comercio_by_name, mock_update, controller, um_comercio, comercio_editado):
    nome_comercio = "comercio1"
    attributes = {"telefone": "4002-8922", "categoria": "1"}

    mock_comercio_by_name.return_value = um_comercio
    mock_update.return_value = comercio_editado
    mock_comercio_by_name.return_value = comercio_editado

    result = controller.atualiza_comercio(attributes, nome_comercio)
    assert result == comercio_editado


@mock.patch('solanches.models.Produto.to_dict')
@mock.patch('solanches.models.Comercio.add_produto')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_cadastra_produto(mock_get_by_name, mock_add_produto, mock_produto_to_dict, controller, models, um_comercio, um_produto):
    produto_nome = "produto teste7"
    comercio_nome = 'comercio_test1'
    attributes = {
        "descricao": "descrição do produto de teste1",
        "imagem": "link de imagem",
        "preco": 20.50,
        "categoria": "salgados"
    }

    mock_get_by_name.return_value = um_comercio
    mock_add_produto.return_value = mock.Mock(wraps=models.Produto)
    mock_produto_to_dict.return_value = um_produto

    result = controller.cadastra_produto(comercio_nome, produto_nome, attributes)

    expected_fields = ["nome", "attributes"]
    result_fields = result.keys()
    assert all(field in result_fields for field in expected_fields)
    assert result == um_produto


def test_cadastra_produto_nome_invalido(controller):
    nome_produto = 0
    nome_comercio = {'nome': "nome_comercio"}
    attributes = {
      "descricao": "descricao do produto",
      "preco": 20.50
    }
    with pytest.raises(SolanchesBadRequestError) as exinfo:
        controller.cadastra_produto(nome_comercio, nome_produto, attributes)
    assert str(exinfo.value.message) == "Erro: nome inválido!"


@mock.patch('solanches.models.Comercio.get_by_name')
def test_cadastra_produto_atributos_invalidos(mock_get_by_name, controller, um_comercio):
    nome_produto = "nome_produto"
    nome_comercio = "nome_comercio"
    comercio_attributes = 3763737
    mock_get_by_name.return_value = um_comercio
    with pytest.raises(SolanchesBadRequestError) as exinfo:
        controller.cadastra_produto(nome_comercio, nome_produto, comercio_attributes)
    assert str(exinfo.value.message) == "Erro: campo attributes inválidos!"


def test_edita_produto_comercio_invalido(controller):
    comercio_nome = 0
    produto_id = "d763e108f053ad2354ff9285b70c48cfc770d9f7"
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.edita_produto(produto_id, comercio_nome, {'sabor': "morango"}, "")
    assert str(excinfo.value.message) == "Erro: nome de comércio inválido"


def test_edita_produto_by_id_invalido(controller):
    id_invalido = 0
    nome_comercio = "comercio1"
    attributes = {"endereco": "jhjhdjhd"}
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.edita_produto(id_invalido, nome_comercio, attributes, "")
    assert str(excinfo.value.message) == "Erro: produto com id inválido!"


def test_edita_produto_by_atributos_invalidos(controller):
    id_valido = "d763e108f053ad2354ff9285b70c48cfc770d9f7"
    nome_comercio = "comercio1"
    attributes = "oioi"
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.edita_produto(id_valido, nome_comercio, attributes, "")
    assert str(excinfo.value.message) == "Erro: attributes inválidos!"


def test_edita_produto_by_nome_invalido(controller):
    id_valido = "d763e108f053ad2354ff9285b70c48cfc770d9f7"
    nome_comercio = "comercio1"
    attributes = {"descricao": "uhu"}
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.edita_produto(id_valido, nome_comercio, attributes, 7838383)
    assert str(excinfo.value.message) == "Erro: nome do produto inválido!"


@mock.patch('solanches.controller.Comercio.get_by_name')
def test_edita_produto_by_comercio_nao_cadastrado(mock_get_by_name, controller):
    id_valido = "d763e108f053ad2354ff9285b70c48cfc770d9f7"
    nome_comercio = "algum"
    attributes = {"descricao": "uhu"}
    mock_get_by_name.return_value = None
    with pytest.raises(SolanchesNotFoundError) as excinfo:
        controller.edita_produto(id_valido, nome_comercio, attributes, "nome_produto")
    assert str(excinfo.value.message) == f'Erro: comercio com o nome algum não cadastrado!'


@mock.patch('solanches.controller.Comercio.get_produto')
@mock.patch('solanches.controller.Comercio.get_by_name')
def test_edita_produto_nao_cadastrado_no_comercio(mock_get_by_name, mock_get_produto, controller, um_comercio):
    id_valido = "d763e108f053ad2354ff9285b70c48cfc770d9f7"
    nome_comercio = "algum"
    attributes = {
            "categoria": "edicao feita",
            "descricao": "descrição atualizada",
            "imagem": "link de imagem",
            "preco": 20.5
    }
    mock_get_by_name.return_value = um_comercio
    mock_get_produto.return_value = None
    with pytest.raises(SolanchesNotFoundError) as excinfo:
        controller.edita_produto(id_valido, nome_comercio, attributes, "nome_produto")
    assert str(excinfo.value.message) == 'Erro: produto com o id d763e108f053ad2354ff9285b70c48cfc770d9f7 não cadastrado no comercio!'


@mock.patch('solanches.controller.Comercio.get_produtos')
@mock.patch('solanches.controller.Comercio.update_produto')
@mock.patch('solanches.controller.Comercio.get_by_name')
@mock.patch('solanches.controller.Comercio.get_produto')
def test_edita_produto_sucesso(mock_get_produto, mock_get_by_name, mock_update_produto, mock_get_produtos, controller, um_comercio, um_produto_editado):

    attributes =  {
            "categoria": "sa",
            "descricao": "descrição atualizada",
            "imagem": "link de imagem",
            "preco": 20.5
    }
    nome_comercio = "comercio1"
    produto_id = "d763e108f053ad2354ff9285b70c48cfc770d9f7"
    mock_get_by_name.return_value = um_comercio
    mock_update_produto.return_value = um_produto_editado
    mock_get_produto.return_value = um_produto_editado
    mock_get_produtos.return_value = [um_produto_editado]

    result = controller.edita_produto(produto_id, nome_comercio, attributes, "produto")
    assert isinstance(result, object)
    assert result == um_produto_editado


def test_adiciona_destaque_nome_comercio_invalido(controller):
    with pytest.raises(SolanchesBadRequestError) as e:
        comercio_nome = ''
        produto_id = 'produtoteste1'
        controller.adiciona_destaque(comercio_nome, produto_id)
    assert str(e.value.message) == 'Erro: nome de comércio inválido'


def test_adiciona_destaque_produto_id_invalido(controller):
    with pytest.raises(SolanchesBadRequestError) as e:
        comercio_nome = 'comercio 1'
        produto_id = 3
        controller.adiciona_destaque(comercio_nome, produto_id)
    assert str(e.value.message) == 'Erro: produto com id inválido!'


@mock.patch('solanches.models.Comercio.get_by_name')
def test_adiciona_destaque_comercio_inexistente(mock_get_by_name, controller):
    mock_get_by_name.return_value = None
    with pytest.raises(SolanchesNotFoundError) as e:
        comercio_nome = 'comercio 1'
        produto_id = 'produto teste'
        controller.adiciona_destaque(comercio_nome, produto_id)
    assert str(e.value.message) == f'Erro: comercio com o nome {comercio_nome} não cadastrado!'


@mock.patch('solanches.models.Comercio.get_produtos_ids')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_adiciona_destaque_produto_fora_comercio(mock_get_by_name, mock_get_produtos, controller):
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produtos.return_value = []
    with pytest.raises(SolanchesNotFoundError) as e:
        comercio_nome = 'comercio 1'
        produto_id = 'produto teste'
        controller.adiciona_destaque(comercio_nome, produto_id)
    assert str(e.value.message) == f'Erro: produto com o id {produto_id} não cadastrado no comercio!'


@mock.patch('solanches.models.Comercio.get_destaques')
@mock.patch('solanches.models.Comercio.get_produtos_ids')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_adiciona_destaque_produto_ja_destacado(mock_get_by_name, mock_get_produtos, mock_get_destaques, controller):
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produtos.return_value = ['produto teste']
    mock_get_destaques.return_value = ['produto teste']
    with pytest.raises(SolanchesBadRequestError) as e:
        comercio_nome = 'comercio 1'
        produto_id = 'produto teste'
        controller.adiciona_destaque(comercio_nome, produto_id)
    assert str(e.value.message) == f'Erro: produto já está nos destaques!'


@mock.patch('solanches.models.Comercio.get_cardapio')
@mock.patch('solanches.models.Comercio.add_destaque')
@mock.patch('solanches.models.Comercio.get_destaques')
@mock.patch('solanches.models.Comercio.get_produtos_ids')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_adiciona_destaque_produto_sucesso(mock_get_by_name, mock_get_produtos, mock_get_destaques, mock_add_destaque, mock_get_cardapio, controller):
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produtos.return_value = ['produto teste']
    mock_get_destaques.return_value = []
    cardapio_esperado = {'produtos': [], 'destaques': ['produto aleatorio', 'produto teste'], 'categorias': []}
    mock_get_cardapio.return_value = cardapio_esperado
    comercio_nome = 'comercio 1'
    produto_id = 'produto teste'
    resultado = controller.adiciona_destaque(comercio_nome, produto_id)
    assert resultado == cardapio_esperado


@mock.patch('solanches.models.Comercio.to_dict')
def test_cadastra_comercio( mock_comercio_to_dict, controller, um_comercio):
    comercio_nome = 'lanche_feliz'
    password = "3671361e6d5dc1ee674156beed67b1fd"
    comercio_attributes = {
         "endereco": "orestes fialho",
         "horarios": "11h-22h"
    }
    mock_comercio_to_dict.return_value = um_comercio
    result = controller.cadastra_comercio(comercio_nome,password, comercio_attributes)

    expected_fields = ["nome", "attributes", "created_at"]
    result_fields = result.keys()
    assert all(field in result_fields for field in expected_fields)


def test_cadastra_comercio_nome_invalido(controller):
    comercio_nome = 90992727
    password = "849439030"
    comercio_attributes = {
        "endereco": "ruaa",
        "horarios": "21h-24h"
    }
    with pytest.raises(SolanchesBadRequestError) as exinfo:
        controller.cadastra_comercio(comercio_nome, password,  comercio_attributes)
    assert str(exinfo.value.message) == 'Erro: campo nome inválido!'


def test_cadastra_comercio_senha_invalida(controller):
    comercio_nome = "comercio1"
    password = 0
    comercio_attributes = {
        "endereco": "ruaa",
        "horarios": "21h-24h"
    }
    with pytest.raises(SolanchesBadRequestError) as exinfo:
        controller.cadastra_comercio(comercio_nome, password,  comercio_attributes)
    assert str(exinfo.value.message) == "Erro: campo senha inválido!"


def test_cadastra_comercio_atributos_invalidos(controller):
    comercio_nome = 'comercio_test4'
    password = "873838383"
    attributes_nao_eh_dict = 48488448
    with pytest.raises(SolanchesBadRequestError) as exinfo:
        controller.cadastra_comercio(comercio_nome, password, attributes_nao_eh_dict)
    assert str(exinfo.value.message) == 'Erro: campo attributes inválidos!'


def test_cadastra_comercio_attributes_sem_horarios(controller):
    comercio_nome = 'comercio_test2'
    password = "3838383"
    comercio_attributes = {
          'endereco': 'rua floriano peixoto'
    }
    with pytest.raises(SolanchesBadRequestError) as exinfo:
        controller.cadastra_comercio(comercio_nome, password, comercio_attributes)
    assert str(exinfo.value.message) == 'Erro: campo horarios não informado!'


def test_cadastra_comercio_attributes_sem_endereco(controller):
    comercio_nome = 'comercio_test2'
    password = "3838383"
    comercio_attributes = {
          'horarios': '21h-23h'
    }
    with pytest.raises(SolanchesBadRequestError) as exinfo:
        controller.cadastra_comercio(comercio_nome, password, comercio_attributes)
    assert str(exinfo.value.message) == 'Erro: campo endereco não informado!'


@mock.patch('solanches.models.Comercio.save')
def test_cadastra_comercio_ja_cadastrado(mock_comercio_save, controller, um_comercio):
    comercio_nome = 'já estou cadastrado'
    password = "763738383"
    comercio_attributes = {
          'endereco': 'rua floriano peixoto',
          "horarios": "21h-24h"
    }
    mock_comercio_save.side_effect = errors.DuplicateKeyError("chave duplicada")
    with pytest.raises(SolanchesBadRequestError) as exinfo:
        controller.cadastra_comercio(comercio_nome, password, comercio_attributes)
    assert str(exinfo.value.message) ==f'Erro: comercio com nome {comercio_nome} já cadastrado!'


@mock.patch('solanches.models.Comercio.get_by_name')
def test_adiciona_categoria_comercio_inexistente(mock_get_by_name, controller):
    nome_invalido = "comercioinvalido"
    categoria = "lanches"
    mock_get_by_name.return_value = None
    with pytest.raises(SolanchesNotFoundError) as excinfo:
        controller.adiciona_categoria(nome_invalido, categoria)
    assert str(excinfo.value.message) == f'Erro: comercio com o nome {nome_invalido} não cadastrado!'


@mock.patch('solanches.models.Comercio.get_by_name')
def test_adiciona_categoria_invalida(mock_get_by_name, controller):
    nome_comercio = 'comercio'
    categoria = None
    mock_get_by_name.return_value = COMERCIO_TESTE
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.adiciona_categoria(nome_comercio, categoria)
    assert str(excinfo.value.message) == f'Erro: valor de categoria inválida!'


@mock.patch('solanches.models.Comercio.get_cardapio_categorias')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_adiciona_categoria_existente(mock_get_by_name, mock_get_categorias, controller):
    nome_invalido = 'comercio'
    categoria = 'salgados'
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_categorias.return_value = ['lanches', 'salgados']
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.adiciona_categoria(nome_invalido, categoria)
    assert str(excinfo.value.message) == f'Erro: categoria já cadastrada nesse comércio!'


@mock.patch('solanches.models.Comercio.adiciona_categoria')
@mock.patch('solanches.models.Comercio.get_cardapio')
@mock.patch('solanches.models.Comercio.get_cardapio_categorias')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_adiciona_categoria_sucesso(mock_get_by_name, mock_get_categorias, mock_get_cardapio, mock_add_categoria, controller):
    nome_comercio = "comercio"
    categoria = 'salgados'
    expected_updated_menu = {'produtos': 'Cardápio exemplo','destaques': [], 'categorias': ['lanches', 'salgados']}
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_categorias.return_value = []
    mock_get_cardapio.return_value = expected_updated_menu
    result = controller.adiciona_categoria(nome_comercio, categoria)
    assert result == expected_updated_menu


@mock.patch('solanches.controller.get_cardapio')
@mock.patch('solanches.models.Comercio.get_produtos_ids')
@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.remove_produto')
def test_remove_produto_sucesso(mock_remove_produto, mock_get_by_name, mock_get_produtos_ids, mock_get_cardapio, controller):
    mock_get_by_name.return_value = COMERCIO_TESTE
    comercio_nome = 'comercio2'
    produto_id = 'idtesteproduto'
    mock_get_produtos_ids.return_value = [PRODUTO_TESTE['_id']]
    mock_get_cardapio.return_value = CARDAPIO_TESTE
    result = controller.remove_produto(comercio_nome, produto_id)
    assert CARDAPIO_TESTE == result


@mock.patch('solanches.models.Comercio.get_produtos_ids')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_produto_fora_comercio(mock_get_by_name, mock_get_produtos_ids, controller):
    mock_get_by_name.return_value = COMERCIO_TESTE
    comercio_nome = 'comercio2'
    produto_id = 'idtesteproduto'
    mock_get_produtos_ids.return_value = []
    with pytest.raises(SolanchesNotFoundError) as e:
        controller.remove_produto(comercio_nome, produto_id)
    assert str(e.value.message) == f'Erro: produto com o id {produto_id} não cadastrado no comercio!'


@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_produto_comercio_inexistente(mock_get_by_name, controller):
    mock_get_by_name.return_value = None
    comercio_nome = 'comercio2'
    produto_id = 'idtesteproduto'
    with pytest.raises(SolanchesNotFoundError) as e:
        controller.remove_produto(comercio_nome, produto_id)
    assert str(e.value.message) == f'Erro: comercio com o nome {comercio_nome} não cadastrado!'


@mock.patch('solanches.models.Comercio.get_destaques')
@mock.patch('solanches.controller.get_cardapio')
@mock.patch('solanches.models.Comercio.get_produtos_ids')
@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.remove_produto_destaques')
def test_remove_produto_destaques_sucesso(mock_remove_produto, mock_get_by_name, mock_get_produtos_ids, mock_get_cardapio, mock_get_destaques, um_comercio, controller):
    mock_get_by_name.return_value = um_comercio
    comercio_nome = 'comercio2'
    produto_id = PRODUTO_TESTE['_id']
    mock_get_produtos_ids.return_value = [produto_id]
    mock_get_cardapio.return_value = CARDAPIO_TESTE
    mock_get_destaques.return_value = [produto_id]
    result = controller.remove_produto_destaques(comercio_nome, produto_id)
    assert CARDAPIO_TESTE == result


@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_produto_destaques_comercio_inexistente(mock_get_by_name, controller):
    mock_get_by_name.return_value = None
    comercio_nome = 'comercio2'
    produto_id = 'idtesteproduto'
    with pytest.raises(SolanchesNotFoundError) as e:
        controller.remove_produto_destaques(comercio_nome, produto_id)
    assert str(e.value.message) == f'Erro: comercio com o nome {comercio_nome} não cadastrado!'


@mock.patch('solanches.models.Comercio.get_produtos_ids')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_produto_destaques_fora_comercio(mock_get_by_name, mock_get_produtos_ids, controller):
    comercio_nome = 'comercio2'
    produto_id = 'idtesteproduto'
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produtos_ids.return_value = []
    with pytest.raises(SolanchesNotFoundError) as e:
        controller.remove_produto_destaques(comercio_nome, produto_id)
    assert str(e.value.message) == f'Erro: produto com o id {produto_id} não cadastrado no comercio!'


@mock.patch('solanches.models.Comercio.get_destaques')
@mock.patch('solanches.models.Comercio.get_produtos_ids')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_produto_destaques_produto_fora_dos_destaques(mock_get_by_name, mock_get_produtos_ids, mock_get_destaques, controller):
    comercio_nome = 'comercio2'
    produto_id = 'idtesteproduto'
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produtos_ids.return_value = [produto_id]
    mock_get_destaques.return_value = []
    with pytest.raises(SolanchesBadRequestError) as e:
        controller.remove_produto_destaques(comercio_nome, produto_id)
    assert str(e.value.message) == f'Erro: produto com id {produto_id} não está nos destaques!'


def test_remove_categoria_invalida(controller):
    categoria = None
    comercio_nome = 'nome teste'
    with pytest.raises(SolanchesBadRequestError) as e:
        controller.remove_categoria(comercio_nome, categoria)
    assert str(e.value.message) == f'Erro: valor de categoria inválida!'


@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_categoria_comercio_invalido(mock_get_by_name, controller):
    mock_get_by_name.return_value = None
    categoria = 'salgados'
    comercio_nome = 'nome teste'
    with pytest.raises(SolanchesNotFoundError) as e:
        controller.remove_categoria(comercio_nome, categoria)
    assert str(e.value.message) == f'Erro: comercio com o nome {comercio_nome} não cadastrado!'


@mock.patch('solanches.models.Comercio.get_cardapio_categorias')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_categoria_fora_comercio(mock_get_by_name, mock_get_categorias, controller):
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_categorias.return_value = []
    categoria = 'salgados'
    comercio_nome = 'comercio2'
    with pytest.raises(SolanchesBadRequestError) as e:
        controller.remove_categoria(comercio_nome, categoria)
    assert str(e.value.message) == f'Erro: categoria não faz parte do comércio'


@mock.patch('solanches.models.Comercio.remove_categoria')
@mock.patch('solanches.models.Comercio.get_cardapio')
@mock.patch('solanches.models.Comercio.get_cardapio_categorias')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_categoria_sucesso(mock_get_by_name, mock_get_categorias, mock_get_cardapio, mock_remove_categoria, controller):
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_categorias.return_value = ['salgados', 'doces']
    mock_get_cardapio.return_value = CARDAPIO_TESTE
    categoria = 'salgados'
    comercio_nome = 'comercio2'
    result = controller.remove_categoria(comercio_nome, categoria)
    assert result == CARDAPIO_TESTE
