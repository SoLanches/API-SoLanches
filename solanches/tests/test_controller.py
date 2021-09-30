from solanches.tests.data_test import PRODUTO, PRODUTOS_COMERCIO, COMERCIOS
from unittest import mock
from solanches.errors import SolanchesNotFoundError
from solanches.errors import SolanchesBadRequestError
import pytest


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


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.remove_comercio')
def test_remove_comercio_sucesso(mock_remove_comercio, mock_get_by_name,  controller):
    comercio_nome = 'comercio_test'
    mock_get_by_name.return_value = {'produtos': []}
    mock_remove_comercio.return_value = 1
    result = controller.remove_comercio(comercio_nome)
    assert result == 1


@mock.patch('solanches.models.Comercio.add_produto')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_cadastra_produto(mock_get_by_name, mock_add_produto, controller, um_comercio, um_produto):
    produto_nome = "produto teste7"
    comercio_nome = 'comercio_test1'
    attributes = {
        "descricao": "descrição do produto de teste1",
        "imagem": "link de imagem",
        "preco": 20.50,
        "categoria": "salgados"
    }

    mock_get_by_name.return_value = um_comercio
    mock_add_produto.return_value = um_produto

    result = controller.cadastra_produto(comercio_nome, produto_nome, attributes)
    
    expected_fields = ["nome", "attributes"]
    result_fields = result.keys()
    assert all(field in result_fields for field in expected_fields)
    assert result == PRODUTO


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

