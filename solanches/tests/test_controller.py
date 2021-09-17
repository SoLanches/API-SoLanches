from unittest import mock
from . data_test import COMERCIO_EDITADO, COMERCIOS
import pytest

@pytest.fixture
def comercios():
    return COMERCIOS


@pytest.fixture
def um_comercio():
    comercio = COMERCIOS[0]
    return comercio


@mock.patch('solanches.controller.Comercio.get_by_name')
def test_edita_comercio_by_name_valido(mock_comercio_by_name, controller, um_comercio):
    nome_valido = "id valido"
    expected_return = um_comercio
    mock_comercio_by_name.return_value = expected_return
    result = controller.get_comercio_by_name(nome_valido)
    assert result == expected_return


def test_edita_comercio_nome_invalido(controller):
    nome_invalido = 18189
    with pytest.raises(AssertionError) as excinfo:
        controller.atualiza_comercio({"endereco": "vuvuvu"}, nome_invalido)
    assert str(excinfo.value) == 'Erro: nome de comercio inválido!'


def test_edita_comercio_sem_atributos(controller):
    comercio_nome = "comercio1"
    with pytest.raises(AssertionError) as excinfo:
        response = controller.atualiza_comercio({"nome": "comercio1"}, comercio_nome)
    assert str(excinfo.value) == "Erro: campo attributes inválidos!"
    assert isinstance(response.json , dict)


@mock.patch('solanches.controller.Comercio.get_by_name')
def test_edita_comercio_com_atributos(mock_get_by_name, controller, um_comercio):
    attributes = {"endereco": "2344222"}
    nome_comercio = "comercio1"
    mock_get_by_name.return_value = um_comercio

    result = controller.atualiza_comercio(attributes, nome_comercio)
    assert "attributes" in result
    assert isinstance(result, object)


