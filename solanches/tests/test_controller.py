from unittest import mock

import pytest


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
   
    expectativa_return = {
        "nome": "comercio_teste1",
        "attributes": {
            "telefone": "123"
        }
    }

    expected_fields = ["nome", "attributes", "created_at"]
    result_fields = result.keys()
    assert all(field in result_fields for field in expected_fields)


def test_cadastra_comercio_sem_nome(controller):
    comercio_attributes = {
          'telefone': '83999999999'
    }

    with pytest.raises(AssertionError) as exinfo:
      controller.cadastra_comercio(None, comercio_attributes)
    assert str(exinfo.value) == "Erro: nome inválido!"


def test_cadastra_comercio_sem_telefone(controller):
    comercio_nome = 'comercio_test2'
    comercio_attributes = {
          'endereco': 'rua floriano peixoto'
    }
    with pytest.raises(AssertionError) as exinfo:
      controller.cadastra_comercio(comercio_nome, comercio_attributes)
    assert str(exinfo.value) == "Erro: Telefone não informado"


@mock.patch('solanches.models.Comercio')
def test_cadastra_comercio_atributos_invalidos(mock_comercio, controller):
    mock_comercio.side_effect = Exception()
    try:
      comercio_nome = 'comercio_test2'
      comercio_attributes = 'rua floriano peixoto'
      controller.cadastra_comercio(comercio_nome, comercio_attributes)
    except Exception as e:
      assert str(e) == "Erro: campo attributes inválidos!"


@pytest.mark.skip(reason="TODO")
@mock.patch('solanches.models.Comercio')
@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Cardapio.get_by_id')
def test_cadastra_comercio_ja_cadastrado(mock_comercio, controller):
    mock_comercio.side_effect = Exception()
    try:
      comercio_nome = 'comercio_test2'
      comercio_attributes = {
            'endereco': 'rua floriano peixoto'
      }
      controller.cadastra_comercio(comercio_nome, comercio_attributes)
      controller.cadastra_comercio(comercio_nome, comercio_attributes)
    except Exception as e:
      assert str(e) == {"error":  "Comércio já cadastrado no banco de dados", "code": 409}
