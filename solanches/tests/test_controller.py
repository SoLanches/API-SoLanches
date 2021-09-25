from unittest import mock
from pymongo.errors import DuplicateKeyError
from . data_test import COMERCIOS
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


@pytest.mark.skip(reason="TODO")
@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Cardapio.get_by_id')
def test_cadastra_comercio(mock_get_by_name, mock_get_by_id, controller):
    comercio_nome = 'comercio_test1'
    comercio_attributes = {
            'telefone': '12234'
    }
    result = controller.cadastra_comercio(comercio_nome, comercio_attributes)
    mock_get_by_id.return_value = {'produtos': []}
    mock_get_by_name.return_value = {'nome': 'comercio_teste1', 'attributes': {"telefone": "12234"}}

    expected_fields = ["nome", "attributes", "created_at"]
    result_fields = result.keys()
    assert all(field in result_fields for field in expected_fields)


def test_cadastra_comercio_sem_nome(controller):
    comercio_nome = 90992727
    password = "849439030"
    comercio_attributes = {
        "endereco": "ruaa",
        "horarios": "21h-24h"
    }
    with pytest.raises(SolanchesBadRequestError) as exinfo:
        controller.cadastra_comercio(comercio_nome, password,  comercio_attributes)
    assert str(exinfo.value.message) == 'Erro: campo nome inválido!'


def test_cadastra_comercio_sem_senha(controller):
    comercio_nome = "comercio1"
    password = 0
    comercio_attributes = {
        "endereco": "ruaa",
        "horarios": "21h-24h"
    }
    with pytest.raises(SolanchesBadRequestError) as exinfo:
        controller.cadastra_comercio(comercio_nome, password,  comercio_attributes)
    assert str(exinfo.value.message) == "Erro: Senha não informada!"


def test_cadastra_comercio_atributos_invalidos(controller):
    comercio_nome = 'comercio_test4'
    password = "873838383"
    comercio_attributes = 48488448
    with pytest.raises(SolanchesBadRequestError) as exinfo:
        controller.cadastra_comercio(comercio_nome, password, comercio_attributes)
    assert str(exinfo.value.message) == 'Erro: campo attributes inválidos!'


def test_cadastra_comercio_sem_horarios(controller):
    comercio_nome = 'comercio_test2'
    password = "3838383"
    comercio_attributes = {
          'endereco': 'rua floriano peixoto'
    }
    with pytest.raises(SolanchesBadRequestError) as exinfo:
        controller.cadastra_comercio(comercio_nome, password, comercio_attributes)
    assert str(exinfo.value.message) == 'Erro: campo horarios não informados!'


def test_cadastra_comercio_sem_endereco(controller):
    comercio_nome = 'comercio_test2'
    password = "3838383"
    comercio_attributes = {
          'horarios': '21h-23h'
    }
    with pytest.raises(SolanchesBadRequestError) as exinfo:
        controller.cadastra_comercio(comercio_nome, password, comercio_attributes)
    assert str(exinfo.value.message) == 'Erro: campo endereco não informado!'


# @mock.patch('solanches.models.Comercio.get_by_name')
# def test_cadastra_comercio_ja_cadastrado(mock_get_by_name, controller, um_comercio):
#     comercio_nome = 'comercio1'
#     password = "763738383"
#     comercio_attributes = {
#           'endereco': 'rua floriano peixoto',
#           "horarios": "21h-24h"
#     }
#     mock_get_by_name.return_value = um_comercio
#     with pytest.raises(DuplicateKeyError):
#         result = controller.cadastra_comercio(comercio_nome, password, comercio_attributes)
#     assert isinstance(result, dict)

