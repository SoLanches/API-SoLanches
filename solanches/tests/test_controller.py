from . data_test import CARDAPIO, COMERCIO
from unittest import mock

import pytest


@pytest.fixture
def um_cardapio():
    cardapio = CARDAPIO
    return cardapio

@pytest.fixture
def um_comercio():
    comercio = COMERCIO
    return comercio


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
    with pytest.raises(AssertionError) as excinfo:
        controller.get_cardapio(nome_invalido)
    assert str(excinfo.value) == 'Erro: nome de comercio inválido!'


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

    with pytest.raises(AssertionError) as excinfo:
         controller.get_cardapio(nome)
    assert str(excinfo.value) == 'Erro: comercio com nome TEXAS não cadastrado!'
