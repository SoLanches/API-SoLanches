from unittest import mock
import pytest

from . data_test import CARDAPIO, COMERCIO, COMERCIOS, COMERCIO_TESTE, PRODUTO_TESTE, PRODUTOS_TESTE
from solanches.errors import SolanchesNotFoundError
from solanches.errors import SolanchesBadRequestError


@pytest.fixture
def um_cardapio():
    cardapio = CARDAPIO
    return cardapio

@pytest.fixture
def um_comercio():
    comercio = COMERCIO
    return comercio


@pytest.fixture
def comercios():
    return COMERCIOS


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


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produto')
def test_recupera_produto_sucesso(mock_get_produto, mock_get_by_name, controller):
    comercio_nome = 'comercio2'
    produto_id = '213123121e'
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produto.return_value = PRODUTO_TESTE

    result = controller.get_produto(comercio_nome, produto_id)
    assert result == PRODUTO_TESTE


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produto')
def test_recupera_produto_inexistente(mock_get_produto, mock_get_by_name, controller):
    comercio_nome = 'comercio2'
    produto_id = '213123121e'
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produto.return_value = None
    with pytest.raises(SolanchesNotFoundError) as e:
      comercio_nome = 'comercio_sem_id'
      controller.get_produto(comercio_nome, produto_id)
    assert str(e.value.message) == f'Erro: produto com o id {produto_id} não cadastrado no comercio!'


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produtos')
def test_recupera_produtos(mock_get_produtos, mock_get_by_name, controller):
    comercio_nome = 'comercio2'
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produtos.return_value = PRODUTOS_TESTE

    result = controller.get_produtos(comercio_nome, {})
    assert result == PRODUTOS_TESTE


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
