import logging
from solanches.custom_erros import *
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
        message = f'Erro: comercio com nome {nome} já cadastrado!'
        raise SolanchesDuplicateKey(message)
    return result


def get_comercios():
    return Comercio.get_all()


def get_comercio(comercio_id):
    assert comercio_id and type(comercio_id) is str, f'Erro: comercio com id {comercio_id} inválido!'
    comercio = Comercio.get_by_id(comercio_id)
    if(not comercio):
        message = f'Erro: comercio com id {comercio_id} não cadastrado!'
        raise SolanchesComercioNaoEncontrado(message)
    return comercio


def get_comercio_by_name(comercio_nome):
    assert comercio_nome and type(comercio_nome) is str, f'Erro: nome de comercio inválido!'
    comercio = Comercio.get_by_name(comercio_nome)
    if(not comercio):
        message = f'Erro: comercio com o nome {comercio_nome} não cadastrado!'
        raise SolanchesComercioNaoEncontrado(message)
    return comercio


def atualiza_comercio(attributes, comercio_nome):
    comercio = Comercio.get_by_name(comercio_nome)
    if(not comercio):
        message = f'Erro: comercio com o nome {comercio_nome} não cadastrado!'
        raise SolanchesComercioNaoEncontrado(message)
        
    set_attributes = {f'attributes.{field}': value for field, value in attributes.items()}
    comercio_id = comercio.get("_id")
    Comercio.update(comercio_id, set_attributes)
    comercio = Comercio.get_by_name(comercio_nome)
    return comercio


def remove_comercio(comercio_nome):
    assert comercio_nome and type(comercio_nome) is str, f'Erro: nome de comercio invalido'
    comercio = Comercio.get_by_name(comercio_nome)
    if(not comercio):
        message = f'Erro: comercio com o nome {comercio_nome} não cadastrado!'
        raise SolanchesComercioNaoEncontrado(message)
    return Comercio.remove_comercio(comercio_nome)


def get_cardapio(comercio_nome):
    assert comercio_nome and type(comercio_nome) is str, f'Erro: nome de comercio inválido!'
    comercio = Comercio.get_by_name(comercio_nome)
    if(not comercio):
        message = f'Erro: comercio com o nome {comercio_nome} não cadastrado!'
        raise SolanchesComercioNaoEncontrado(message)
    cardapio = Comercio.get_cardapio(comercio_nome)
    return cardapio


def cadastra_produto(comercio_nome, nome_produto, attributes={}):
    assert nome_produto and type(nome_produto) is str, "Erro: nome inválido!"
    if attributes:
        assert type(attributes) is dict, "Erro: campo attributes inválidos!"

    comercio = Comercio.get_by_name(comercio_nome)
    if(not comercio):
        message = f'Erro: comercio com o nome {comercio_nome} não cadastrado!'
        raise SolanchesComercioNaoEncontrado(message)
    novo_produto = Produto(nome_produto, attributes)
    produto_id = Comercio.add_produto(novo_produto, comercio_nome)
    return produto_id


#TODO: será adaptado
def get_produto(produto_id):
    assert produto_id and type(produto_id) is str, "Erro: produto com id inválido!"
    produto = Produto.get_by_id(produto_id)
    if(not produto):
        message = f'Erro: produto com o id {produto_id} não cadastrado!'
        raise SolanchesProdutoNaoEncontrado(message)
    return produto


def get_produtos(comercio_nome, has_categories):
    comercio = Comercio.get_by_name(comercio_nome)
    if(not comercio):
        message = f'Erro: comercio com o nome {comercio_nome} não cadastrado!'
        raise SolanchesComercioNaoEncontrado(message)

    produtos = Comercio.get_produtos(comercio_nome) if not has_categories else _get_produtos_categoria(comercio_nome)
    return produtos


def edita_produto(produto_id, comercio_nome, attributes):
    assert comercio_nome and type(comercio_nome) is str, "Erro: nome de comércio inválido"
    assert produto_id and type(produto_id) is str, "Erro: produto com id inválido!"
    assert attributes and type(attributes) is dict, "Erro: attributes inválidos!"

    comercio = Comercio.get_by_name(comercio_nome)
    if(not comercio):
        message = f'Erro: comercio com o nome {comercio_nome} não cadastrado!'
        raise SolanchesComercioNaoEncontrado(message)
    if(not produto_id in Comercio.get_produtos(comercio_nome)):
        message = f'Erro: produto com o id {produto_id} não cadastrado!'
        raise SolanchesProdutoNaoEncontrado(message)

    set_attributes = {f'attributes.{field}': value for field, value in attributes.items()}
    Produto.update(produto_id, set_attributes)
    produto = Produto.get_by_id(produto_id)
    return produto


def adiciona_destaques(destaques, comercio_nome):
    assert destaques, f'Erro: destaques vazio!'
    comercio = Comercio.get_by_name(comercio_nome)
    if(not comercio):
        message = f'Erro: comercio com o nome {comercio_nome} não cadastrado!'
        raise SolanchesComercioNaoEncontrado(message)
    produtos_comercio = Comercio.get_produtos(comercio_nome)

    if(not all(produto in produtos_comercio for produto in destaques)):
        message =f'Erro: produto precisa fazer parte do cardápio do comércio!'
        raise SolanchesProdutoNaoEstaNoCardapio(message)

    destaques_comercio = Comercio.get_destaques(comercio_nome)
    destaques_filtrados = [destaque for destaque in destaques if destaque not in destaques_comercio]
    Comercio.add_destaques(comercio_nome, destaques_filtrados)


def remove_produto(comercio_nome, produto_id):
    comercio = Comercio.get_by_name(comercio_nome)
    if(not comercio):
        message = f'Erro: comercio com o nome {comercio_nome} não cadastrado!'
        raise SolanchesComercioNaoEncontrado(message)
    produtos_comercio = Comercio.get_produtos(comercio_nome)
    if(not produto_id in produtos_comercio):
        message = f'Erro: produto não faz parte do cardápio do comércio ou não está cadastrado!'
        raise SolanchesProdutoNaoEncontrado(message)

    Comercio.remove_produto(comercio_nome, produto_id)
    cardapio = get_cardapio(comercio_nome)
    return cardapio


def _get_produtos_categoria(comercio_nome):
    result = {}
    produtos = Comercio.get_produtos(comercio_nome)
    for produto in produtos:
        categoria = Comercio.get_produto_categoria(produto)
        if result.get(categoria):
            result[categoria] = result.get(categoria) + [produto]
        else:
            result[categoria] = [produto]
    return result
