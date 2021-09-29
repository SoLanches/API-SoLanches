from unittest import mock
from attr import attributes

import pytest

from . data_test import CARDAPIO, COMERCIOS, PRODUTO
from solanches.errors import SolanchesNotFoundError
from solanches.errors import SolanchesBadRequestError


@pytest.fixture
def comercios():
    return COMERCIOS


@pytest.fixture
def um_comercio():
    comercio = COMERCIOS[0]
    return comercio


@pytest.fixture
def um_produto():
    produto = PRODUTO
    return produto


@pytest.fixture
def um_cardapio():
    cardapio = CARDAPIO
    return cardapio


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
    assert result == [];
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


@mock.patch('solanches.controller.Comercio.get_by_name')
def test_get_comercio_by_name_com_nome_nao_str(mock_comercio_by_name, controller):
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


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.remove_comercio')
def test_remove_comercio_sucesso(mock_remove_comercio, mock_get_by_name,  controller):
    comercio_nome = 'comercio_test'
    mock_get_by_name.return_value = {'produtos': []}
    mock_remove_comercio.return_value = 1
    result = controller.remove_comercio(comercio_nome)
    assert result == 1


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
    nome_produto = 7838383
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.edita_produto(id_valido, nome_comercio, attributes, nome_produto)
    assert str(excinfo.value.message) == "Erro: nome inválido!"


@mock.patch('solanches.controller.Comercio.get_by_name')
@mock.patch('solanches.controller.Comercio.get_produto')
def test_edita_produto_sucesso(mock_get_produto, mock_get_by_name, controller, um_produto, um_comercio):

    attributes = {"categoria": "okok"}
    nome_comercio = "comercio1"
    produto_id = "d763e108f053ad2354ff9285b70c48cfc770d9f7"
    mock_get_produto.return_value = um_produto
    mock_get_by_name.return_value = um_comercio

    result = controller.edita_produto(produto_id, nome_comercio, attributes, "produto")

    assert "attributes" in result
    assert isinstance(result, object)
   
    