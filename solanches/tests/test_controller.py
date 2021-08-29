import pytest


def test_remove_comercio_inexistente(controller):
    with pytest.raises(Exception) as execinfo:
        comercio_nome = 'comercio_sem_id'
        controller.remove_comercio(comercio_nome)
    assert str(execinfo.value) == f'Erro: comercio com nome {comercio_nome} não cadastrado!'


def test_remove_comercio_sucesso(controller):
    comercio_nome = 'comercio_test'
    comercio_attributes = {
            'telefone': '83999999999'
    }

    controller.cadastra_comercio(comercio_nome, comercio_attributes)
    result = controller.remove_comercio(comercio_nome)
    assert result == 1
