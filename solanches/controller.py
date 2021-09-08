import logging

from . models import Produto, Comercio
from . import connect2db


def cadastra_comercio(nome, attributes):
    assert nome and type(nome) is str, "Erro: nome inválido!"
    assert attributes and type(attributes) is dict, "Erro: campo attributes inválidos!"
    assert "telefone" in attributes, "Erro: Telefone não informado"
    try:
        novo_comercio = Comercio(nome, attributes)
        novo_comercio.save()
        result = novo_comercio.to_dict()
    except connect2db.pymongo.errors.DuplicateKeyError:
        erro = {"error":  "Comércio já cadastrado no banco de dados", "code": 409}
        logging.error(erro)
        result = erro
    return result


def get_comercios():
    return Comercio.get_all()


def get_comercio(comercio_id):
    assert comercio_id and type(comercio_id) is str, f'Erro: comercio com id {comercio_id} inválido!'
    comercio = Comercio.get_by_id(comercio_id)
    assert comercio, f'Erro: comercio com id {comercio_id} não cadastrado!'
    return comercio


def get_comercio_by_name(comercio_nome):
    assert comercio_nome and type(comercio_nome) is str, 'Erro: nome de comercio inválido!'
    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f'Erro: comercio com nome {comercio_nome} nao cadastrado!'
    return comercio


def atualiza_comercio(attributes, comercio_nome):
    comercio = Comercio.get_by_name(comercio_nome)
    set_attributes = {f'attributes.{field}': value for field, value in attributes.items()}

    comercio_id = comercio.get("_id")
    Comercio.update(comercio_id, set_attributes)
    comercio = Comercio.get_by_name(comercio_nome)
    return comercio


def remove_comercio(comercio_nome):
    assert comercio_nome and type(comercio_nome) is str, 'Erro: nome de comercio invalido'
    comercio = Comercio.get_by_name(comercio_nome) 
    assert comercio, f'Erro: comercio com nome {comercio_nome} não cadastrado!'
    return Comercio.remove_comercio(comercio_nome)


def get_cardapio(comercio_nome):
    assert comercio_nome and type(comercio_nome) is str, 'Erro: nome de comercio inválido!'
    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f'Erro: comercio com nome {comercio_nome} não cadastrado!'
    cardapio = Comercio.get_cardapio(comercio_nome)
    assert cardapio, 'Erro: cardapio não encontrado!'
    return cardapio


def cadastra_produto(comercio_nome, nome_produto, attributes):
    assert nome_produto and type(nome_produto) is str, "Erro: nome inválido!"
    if attributes:
        assert type(attributes) is dict, "Erro: campo attributes inválidos!"

    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f"Erro: comércio com nome {comercio_nome} não cadastrado"

    novo_produto = Produto(nome_produto, attributes)
    produto_id = Comercio.add_produto(novo_produto, comercio_nome)
    return produto_id


#TODO: será adaptado
def get_produto(produto_id):
    assert produto_id and type(produto_id) is str, "Erro: produto com id inválido!"
    produto = Produto.get_by_id(produto_id)
    assert produto, "Erro: produto com id não cadastrado!"
    return produto


def get_produtos(comercio_nome, has_categories):
    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f'Erro: comercio com nome {comercio_nome} nao cadastrado!'
    produtos = Comercio.get_produtos(comercio_nome) if not has_categories else _get_produtos_categoria(comercio_nome)
    return produtos


def edita_produto(produto_id, comercio_nome, attributes):
    assert comercio_nome and type(comercio_nome) is str, "Erro: nome de comércio inválido"

    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f"Erro: comércio com nome {comercio_nome} não cadastrado"

    assert produto_id and type(produto_id) is str, "Erro: produto com id inválido!"
    assert produto_id in Comercio.get_produtos(comercio_nome), "Erro: produto com id não cadastrado!"
    assert attributes and type(attributes) is dict, "Erro: attributes inválidos!"

    set_attributes = {f'attributes.{field}': value for field, value in attributes.items()}

    Produto.update(produto_id, set_attributes)

    produto = Produto.get_by_id(produto_id)
    return produto


def adiciona_destaques(destaques, comercio_nome):
    assert destaques, 'Erro: destaques vazio!'
    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f'Erro: comercio com nome {comercio_nome} nao cadastrado!'
    produtos_comercio = Comercio.get_produtos(comercio_nome)
    assert all(produto in produtos_comercio for produto in destaques), 'Erro: produto precisa fazer parte do cardápio do comércio'

    destaques_comercio = Comercio.get_destaques(comercio_nome)
    filtered_destaques = [destaque for destaque in destaques if destaque not in destaques_comercio]
    Comercio.add_destaques(comercio_nome, filtered_destaques)


def remove_produto(comercio_nome, produto_id):
    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f'Erro: comercio com nome {comercio_nome} nao cadastrado!'
    produtos_comercio = Comercio.get_produtos(comercio_nome)
    assert produto_id in produtos_comercio, 'Erro: produto não faz parte do cardápio do comércio'

    Comercio.remove_produto(comercio_nome, produto_id)
    cardapio = get_cardapio(comercio_nome)
    return cardapio


def _get_produtos_categoria(comercio_nome):
    result = {}
    produtos = Comercio.get_produtos(comercio_nome)
    for produto in produtos:
        categoria = Comercio.get_produto_categoria(produto.get("_id"))
        result.setdefault(categoria, []).append(produto)
    return result
