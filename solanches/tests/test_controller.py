import pytest
from unittest import mock

@mock.patch('solanches.models.Comercio')
def test_remove_comercio_inexistente(mock_comercio, controller):
    mock_comercio.side_effect = Exception()
    try:
      comercio_nome = 'comercio_sem_id'
      controller.remove_comercio(comercio_nome)
    except Exception as e:
      assert str(e) == f'Erro: comercio com nome {comercio_nome} não cadastrado!'


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.remove_comercio')
@mock.patch('solanches.models.Cardapio.get_by_id')
def test_remove_comercio_sucesso(mock_get_by_id, mock_remove_comercio, mock_get_by_name, controller):
    comercio_nome = 'comercio_test'
    comercio_attributes = {
            'telefone': '83999999999'
    }
    mock_get_by_name.return_value = {'nome': comercio_nome,
                                           'attributes': comercio_attributes}
    mock_get_by_id.return_value = {'produtos': []}
    mock_remove_comercio.return_value = 1
    result = controller.remove_comercio(comercio_nome)
    assert result == 1
