from solanches.tests.data_test import PRODUTOS_COMERCIO
from unittest import mock
import pytest


@pytest.mark.skip(reason="TODO")
@mock.patch('solanches.models.Comercio.get_produtos')
def test_cadastra_produto(mock_get_produtos, controller):
    produto_nome = 'produto_test1'
    comercio_nome = 'comercio_test1'
    attributes = {
            "marca": "kibom"
    }

    comercio_attributes = {
          "endereco": "rua floriano peixoto"
    }
    controller.cadastra_comercio(comercio_nome, comercio_attributes)
    result = controller.cadastra_produto(comercio_nome, produto_nome, attributes)
    mock_get_produtos.return_value = PRODUTOS_COMERCIO

    expected_fields = ["nome", "attributes"]
    result_fields = result.keys()
    assert all(field in result_fields for field in expected_fields)
    assert result == PRODUTOS_COMERCIO


def test_cadastra_produto_nome_invalido(controller):
    nome_produto = 0
    nome_comercio = {'nome': "nome_comercio"}
    attributes = {
      "descricao": "descricao do produto",
      "preco": 20.50
    }
    comercio_attributes = {
          'endereco': 'rua floriano peixoto'
    }
    controller.cadastra_comercio(nome_comercio, comercio_attributes)
    with pytest.raises(AssertionError) as exinfo:
      controller.cadastra_produto(nome_comercio, nome_produto, attributes)
    assert str(exinfo.value) == "Erro: nome inválido!"


def test_cadastra_produto_sem_atributos(controller):
    nome_produto = {'nome': "nome_produto"}
    nome_comercio = {'nome': "nome_comercio"}
    attributes = 0
    comercio_attributes = {
          'endereco': 'rua floriano peixoto'
    }
    controller.cadastra_comercio(nome_comercio, comercio_attributes)
    with pytest.raises(AssertionError) as exinfo:
      controller.cadastra_produto(nome_comercio, nome_produto, attributes)
    assert str(exinfo.value) == "Erro: campo attributes inválidos!"


def test_cadastra_produto_com_comercio_nao_cadastrado(controller):
    nome_produto = {'nome': "nome_produto"}
    nome_comercio = {'nome': "nome_comercio"}
    attributes = {
      "descricao": "descricao do produto",
      "preco": 20.50
    }
    with pytest.raises(AssertionError) as exinfo:
      controller.cadastra_produto(nome_comercio, nome_produto, attributes)
    assert str(exinfo.value) == "Erro: comércio com nome nome_comercio não cadastrado"