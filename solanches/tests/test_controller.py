import pytest


def test_cadastro_comercio(controller):
    comercio_nome = 'comercio_carol'
    attributes = {
            'telefone': '8388775655',
            'endereco': 'rua floriano peixoto'
    }

    result = controller.cadastra_comercio(comercio_nome, attributes)
    assert result == 1


def test_cadastro_comercio_ja_cadastrado(controller):
    with pytest.raises(Exception) as execinfo:
        comercio_nome = 'comercio_carol'
        attributes = {
            'telefone': '8388775655',
            'endereco': 'rua floriano peixoto'
        }

        controller.cadastra_comercio(comercio_nome, attributes)

    assert str(execinfo.value) == f'Comércio já cadastrado no banco de dados'


