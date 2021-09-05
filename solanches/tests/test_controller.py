from solanches.models import Comercio
import pytest
from unittest import mock


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
    
    assert result == expectativa_return


@mock.patch('solanches.models.Comercio')
def test_cadastra_comercio_sem_nome(mock_comercio, controller):
    mock_comercio.side_effect = Exception()
    try:
      comercio_attributes = {
            'telefone': '83999999999'
      }
      controller.cadastra_comercio(None, comercio_attributes)
    except Exception as e:
      assert str(e) == 'Erro: nome inválido!'


@mock.patch('solanches.models.Comercio')
def test_cadastra_comercio_sem_telefone(mock_comercio, controller):
    mock_comercio.side_effect = Exception()
    try:
      comercio_nome = 'comercio_test2'
      comercio_attributes = {
            'endereco': 'rua floriano peixoto'
      }
      controller.cadastra_comercio(comercio_nome, comercio_attributes)
    except Exception as e:
      assert str(e) == "Erro: Telefone não informado"


@mock.patch('solanches.models.Comercio')
def test_cadastra_comercio_aatributos_invalidos(mock_comercio, controller):
    mock_comercio.side_effect = Exception()
    try:
      comercio_nome = 'comercio_test2'
      comercio_attributes = 'rua floriano peixoto'
      controller.cadastra_comercio(comercio_nome, comercio_attributes)
    except Exception as e:
      assert str(e) == "Erro: campo attributes inválidos!"


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