from unittest import mock

import pytest

from . data_test import CARDAPIO_TESTE, COMERCIO_TESTE, COMERCIOS, PRODUTO_TESTE


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
    
    with pytest.raises(AssertionError) as excinfo:
        controller.get_comercio_by_id(id_invalido)
    assert str(excinfo.value) == f'Erro: comercio com id {id_invalido} não cadastrado!'


@mock.patch('solanches.controller.Comercio.get_by_id')
def test_get_comercio_by_id_com_id_nao_str(mock_comercio_by_id, controller):
    id_invalido = 123
    with pytest.raises(AssertionError) as excinfo:
        controller.get_comercio_by_id(id_invalido)
    assert str(excinfo.value) == f'Erro: comercio com id {id_invalido} inválido!'


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
    
    with pytest.raises(AssertionError) as excinfo:
        controller.get_comercio_by_name(nome_invalido)
    assert str(excinfo.value) == f'Erro: comercio com nome {nome_invalido} nao cadastrado!'


@mock.patch('solanches.controller.Comercio.get_by_name')
def test_get_comercio_by_name_com_nome_nao_str(mock_comercio_by_name, controller):
    nome_invalido = 123
    with pytest.raises(AssertionError) as excinfo:
        controller.get_comercio_by_name(nome_invalido)
    assert str(excinfo.value) == f'Erro: nome de comercio inválido!'


@mock.patch('solanches.controller.Comercio.get_by_name')
def test_get_comercio_by_name_valido(mock_comercio_by_name, controller, um_comercio):
    nome_valido = "id valido"
    expected_return = um_comercio
    mock_comercio_by_name.return_value = expected_return
    result = controller.get_comercio_by_name(nome_valido)
    assert result == expected_return


@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_comercio_inexistente(mock_comercio, controller):
    mock_comercio.return_value = None
    with pytest.raises(Exception) as e:
      comercio_nome = 'comercio_sem_id'
      controller.remove_comercio(comercio_nome)
    assert str(e.value) == f'Erro: comercio com nome {comercio_nome} não cadastrado!'


def test_remove_comercio_nome_invalido(controller):
    with pytest.raises(Exception) as e:
        comercio_nome_invalido = None
        controller.remove_comercio(comercio_nome_invalido)
    assert str(e.value) == f'Erro: nome de comercio invalido'


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.remove_comercio')
def test_remove_comercio_sucesso(mock_remove_comercio, mock_get_by_name,  controller):
    comercio_nome = 'comercio_test'
    mock_get_by_name.return_value = {'produtos': []}
    mock_remove_comercio.return_value = 1
    result = controller.remove_comercio(comercio_nome)
    assert result == 1


@mock.patch('solanches.models.Cardapio.get_by_id')
@mock.patch('solanches.models.Comercio.get_produtos_ids')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_produto_sucesso(mock_get_by_name, mock_get_produtos_ids, mock_get_by_id, controller):
    mock_get_by_name.return_value = COMERCIO_TESTE
    comercio_nome = 'comercio2'
    produto_id = 'idtesteproduto'
    mock_get_produtos_ids.return_value = [PRODUTO_TESTE['_id']]
    mock_get_by_id.return_value = CARDAPIO_TESTE
    result = controller.remove_produto(comercio_nome, produto_id)
    assert CARDAPIO_TESTE == result


@mock.patch('solanches.models.Comercio.get_produtos_ids')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_produto_fora_comercio(mock_get_by_name, mock_get_produtos_ids, controller):
    mock_get_by_name.return_value = COMERCIO_TESTE
    comercio_nome = 'comercio2'
    produto_id = 'idtesteproduto'
    mock_get_produtos_ids.return_value = []
    with pytest.raises(Exception) as e:
        controller.remove_produto(comercio_nome, produto_id)
    assert str(e.value) == f'Erro: produto não faz parte do cardápio do comércio'


@mock.patch('solanches.models.Comercio.get_produtos_ids')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_produto_fora_comercio(mock_get_by_name, mock_get_produtos_ids, controller):
    mock_get_by_name.return_value = COMERCIO_TESTE
    comercio_nome = 'comercio2'
    produto_id = 'idtesteproduto'
    mock_get_produtos_ids.return_value = []
    with pytest.raises(Exception) as e:
        controller.remove_produto(comercio_nome, produto_id)
    assert str(e.value) == f'Erro: produto não faz parte do cardápio do comércio'


@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_produto_comercio_inexistente(mock_get_by_name, controller):
    mock_get_by_name.return_value = None
    comercio_nome = 'comercio2'
    produto_id = 'idtesteproduto'
    with pytest.raises(Exception) as e:
        controller.remove_produto(comercio_nome, produto_id)
    assert str(e.value) == f'Erro: comercio com nome {comercio_nome} nao cadastrado!'
