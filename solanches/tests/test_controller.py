from contextlib import nullcontext
import json
import pytest


def teste_cadastro_comercio_sucesso(controller):
    comercio_nome = 'comercio_teste1'
    attributes = {
            'telefone': '8388775655',
            'endereco': 'rua floriano peixoto'
    }

    result = controller.cadastra_comercio(comercio_nome, attributes)
    assert comercio_nome == result[comercio_nome]


def teste_cadastro_comercio_nome_nulo(controller):
    with pytest.raises(Exception) as execinfo:
        comercio_nome = None
        attributes = {
                'telefone': '8388775655',
                'endereco': 'rua floriano peixoto'
        }

        controller.cadastra_comercio(comercio_nome, attributes)
    assert str(execinfo.value) == 'Comércio com nome nulo não pode ser cadastrado'


def teste_cadastro_comercio_sem_telefone(controller):
    with pytest.raises(Exception) as execinfo:
        comercio_nome = 'comercio_teste2'
        attributes = {
                'endereco': 'rua floriano peixoto'
        }

        controller.cadastra_comercio(comercio_nome, attributes)
    assert str(execinfo.value) == 'Erro: Telefone não informado'


def teste_cadastro_comercio_ja_cadastrado(controller):
    with pytest.raises(Exception) as execinfo:
        comercio_nome = 'comercio_teste1'
        attributes = {
            'telefone': '8388775655',
            'endereco': 'rua floriano peixoto'
        }

        controller.cadastra_comercio(comercio_nome, attributes)

    assert str(execinfo.value) == f'Comércio já cadastrado no banco de dados'


