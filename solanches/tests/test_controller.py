from unittest import mock

import pytest

from . data_test import COMERCIO_TESTE, COMERCIOS
from solanches.errors import SolanchesNotFoundError
from solanches.errors import SolanchesBadRequestError


@pytest.fixture
def comercios():
    return COMERCIOS


@pytest.fixture
def um_comercio():
    comercio = COMERCIOS[0]
    return comercio


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


@mock.patch('solanches.models.Cardapio.get_by_id')
@mock.patch('solanches.models.Comercio.get_destaques')
@mock.patch('solanches.models.Comercio.get_produtos_ids')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_adiciona_destaque_produto_sucesso(mock_get_by_name, mock_get_produtos, mock_get_destaques, mock_get_cardapio, controller):
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produtos.return_value = ['produto teste']
    mock_get_destaques.return_value = []
    cardapio_desatualizado = {'produtos': [], 'destaques': ['produto aleatorio'], 'categorias': []}
    mock_get_cardapio.return_value = cardapio_desatualizado
    comercio_nome = 'comercio 1'
    produto_id = 'produto teste'
    resultado = controller.adiciona_destaque(comercio_nome, produto_id)
    cardapio_esperado = {'produtos': [], 'destaques': ['produto aleatorio', 'produto teste'], 'categorias': []}
    assert resultado == cardapio_esperado