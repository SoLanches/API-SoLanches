import logging
import datetime

import jwt

from . models import Produto, Comercio, BlockList
from . import connect2db


def cadastra_comercio(nome, password, attributes):
    assert nome and type(nome) is str, 'Erro: nome inválido!'
    assert password and type(password) is str, "Erro: Senha não informada!"
    assert attributes and type(attributes) is dict, 'Erro: campo attributes inválidos!'
    assert "endereco" in attributes, 'Erro: campo endereco não informado!'
    assert "horarios" in attributes, 'Erro: campo horarios não informados!'
    try:
        novo_comercio = Comercio(nome, password, attributes)
        novo_comercio.save()
        result = novo_comercio.to_dict()
    except connect2db.pymongo.errors.DuplicateKeyError:
        erro = {"error":  "Comércio já cadastrado no banco de dados", "code": 409}
        logging.error(erro)
        result = erro
    return result


def get_comercios(has_categories=False):
    comercios = _get_comercios_categoria() if has_categories else Comercio.get_all()
    return comercios
    

def _get_comercios_categoria():
    result = {}
    comercios = Comercio.get_all()
    for comercio in comercios:
        categoria = Comercio.get_categoria(comercio.get("nome"))
        result.setdefault(categoria, []).append(comercio)
    return result


def get_comercio_by_id(comercio_id):
    assert comercio_id and type(comercio_id) is str, f'Erro: comercio com id {comercio_id} inválido!'
    comercio = Comercio.get_by_id(comercio_id)
    assert comercio, f'Erro: comercio com id {comercio_id} não cadastrado!'
    return comercio


def get_comercio_by_name(comercio_nome):
    assert type(comercio_nome) is str, 'Erro: nome de comercio inválido!'
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


def get_produto(comercio_nome, produto_id):
    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f'Erro: comércio com nome {comercio_nome} não cadastrado'

    assert produto_id and type(produto_id) is str, "Erro: produto com id inválido!"
    produto = Produto.get_by_id(produto_id)
    assert produto, "Erro: produto não cadastrado no sistema"

    produto = Comercio.get_produto(comercio_nome, produto_id)
    assert produto, "Erro: produto não faz parte desse comércio"

    return produto


def get_produtos(comercio_nome, has_categories):
    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f'Erro: comercio com nome {comercio_nome} nao cadastrado!'
    produtos = Comercio.get_produtos(comercio_nome) if not has_categories else _get_produtos_categoria(comercio_nome)
    return produtos

  
def get_produtos_ids(comercio_nome):
    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f'Erro: comercio com nome {comercio_nome} nao cadastrado!'
    produtos = Comercio.get_produtos_ids(comercio_nome)
    return produtos


def _get_produtos_categoria(comercio_nome):
    result = {}
    produtos = Comercio.get_produtos(comercio_nome)
    for produto in produtos:
        categoria = Comercio.get_produto_categoria(produto.get("_id"))
        result.setdefault(categoria, []).append(produto)
    return result
  
  
def edita_produto(produto_id, comercio_nome, attributes, nome):
    assert comercio_nome and type(comercio_nome) is str, "Erro: nome de comércio inválido"

    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f"Erro: comércio com nome {comercio_nome} não cadastrado"

    assert produto_id and type(produto_id) is str, "Erro: produto com id inválido!"
    assert produto_id in Comercio.get_produtos_ids(comercio_nome), "Erro: produto precisa fazer parte do cardápio do comércio"
    assert Comercio.get_produto(comercio_nome, produto_id), "Erro: produto com id não cadastrado!"
    assert type(attributes) is dict, "Erro: attributes inválidos!"
    assert type(nome) is str, "Erro: nome inválido!"

    set_attributes = {f'attributes.{field}': value for field, value in attributes.items()}
    set_nome = {f'nome': nome if nome else Comercio.get_produto(comercio_nome, produto_id).get("nome")}

    Comercio.update_produto(produto_id, set_attributes, set_nome)
    produto = Comercio.get_produto(comercio_nome, produto_id)
    return produto


def adiciona_destaque(comercio_nome, produto_id):
    assert comercio_nome and type(comercio_nome) is str, 'Erro: nome de comércio inválido'
    
    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f'Erro: comercio com nome {comercio_nome} nao cadastrado!'
    
    assert produto_id and type(produto_id) is str, 'Erro: produto com id inválido!'
    assert produto_id in Comercio.get_produtos_ids(comercio_nome), 'Erro: produto não faz parte do cardápio do comércio!'

    destaques = Comercio.get_destaques(comercio_nome)
    assert produto_id not in destaques, f'Erro: produto com id {produto_id} já está nos destaques!'

    Comercio.add_destaque(comercio_nome, produto_id)
    cardapio = Comercio.get_cardapio(comercio_nome)
    return cardapio


def remove_produto(comercio_nome, produto_id):
    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f'Erro: comercio com nome {comercio_nome} nao cadastrado!'
    produtos_comercio = Comercio.get_produtos_ids(comercio_nome)
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


def remove_produto_destaques(comercio_nome, produto_id):
    assert comercio_nome and type(comercio_nome) is str, 'Erro: nome de comércio inválido'
    
    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f'Erro: comercio com nome {comercio_nome} nao cadastrado!'
    
    assert produto_id and type(produto_id) is str, 'Erro: produto com id inválido!'
    assert produto_id in Comercio.get_produtos_ids(comercio_nome), 'Erro: produto não faz parte do cardápio do comércio!'
    assert produto_id in Comercio.get_destaques(comercio_nome), f'Erro: produto com id {produto_id} não está nos destaques!'

    Comercio.remove_produto_destaques(comercio_nome, produto_id)
    cardapio = get_cardapio(comercio_nome)
    return cardapio


def adiciona_categoria(comercio_nome, categoria):
    assert type(categoria) is str, 'Erro: valor de categoria inválida!'
    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f'Erro: comercio com nome {comercio_nome} nao cadastrado!'
    assert categoria not in Comercio.get_cardapio_categorias(comercio_nome), f'Erro: categoria já cadastrada nesse comércio!'

    Comercio.adiciona_categoria(comercio_nome, categoria)

    cardapio_atualizado = Comercio.get_cardapio(comercio_nome)

    return cardapio_atualizado


def remove_categoria(comercio_nome, categoria):
    assert type(categoria) is str, 'Erro: valor de categoria inválida!'
    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f'Erro: comercio com nome {comercio_nome} nao cadastrado!'
    categorias = Comercio.get_cardapio_categorias(comercio_nome)
    assert categoria in categorias, 'Erro: categoria não faz parte do comércio'
    
    Comercio.remove_categoria(comercio_nome, categoria)

    cardapio_atualizado = Comercio.get_cardapio(comercio_nome)

    return cardapio_atualizado


def login(comercio_nome, password, secret):
    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f'Erro: comercio com nome {comercio_nome} nao cadastrado!'
    assert Comercio.verify_password(comercio_nome, password), "Erro! Senha incorreta"

    payload = {
        'id': comercio.get("_id"),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }

    token = jwt.encode(payload, secret, algorithm="HS256")
    return token


def logout(token):
    block_token = BlockList(token)
    block_token.save()
