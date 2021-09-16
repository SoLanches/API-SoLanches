import datetime

import jwt

from . import connect2db
from . errors import *
from . models import Produto, Comercio, BlockList


def _assert(condition, message, SolanchesError=SolanchesBadRequestError):
    if condition: return
    raise SolanchesError(message)


def cadastra_comercio(nome, password, attributes):
    _assert(nome and type(nome) is str, 'Erro: campo nome inválido!')
    _assert(password and type(password) is str, "Erro: Senha não informada!")
    _assert(attributes and type(attributes) is dict, 'Erro: campo attributes inválidos!')
    _assert("endereco" in attributes, 'Erro: campo endereco não informado!')
    _assert("horarios" in attributes, 'Erro: campo horarios não informados!')
    try:
        novo_comercio = Comercio(nome, password, attributes)
        novo_comercio.save()
        result = novo_comercio.to_dict()
    except connect2db.pymongo.errors.DuplicateKeyError:
        message = f'Erro: comercio com nome {nome} já cadastrado!'
        _assert(False, message)
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
    _assert(comercio_id and type(comercio_id) is str, f'Erro: comercio com id {comercio_id} inválido!')
    comercio = Comercio.get_by_id(comercio_id)
    _assert(comercio, f'Erro: comercio com id {comercio_id} não cadastrado!', SolanchesNotFoundError)
    return comercio


def get_comercio_by_name(comercio_nome):
    _assert(comercio_nome and type(comercio_nome) is str, 'Erro: nome de comercio inválido!')
    comercio = Comercio.get_by_name(comercio_nome)
    _assert(comercio, f'Erro: comercio com o nome {comercio_nome} não cadastrado!', SolanchesNotFoundError)
    return comercio


def atualiza_comercio(attributes, comercio_nome):
    _assert(attributes and isinstance(attributes, dict), 'Erro: attributes inválidos')
    comercio = Comercio.get_by_name(comercio_nome)
    _assert(comercio, f'Erro: comercio com o nome {comercio_nome} não cadastrado!', SolanchesNotFoundError)
    set_attributes = {f'attributes.{field}': value for field, value in attributes.items()}
    comercio_id = comercio.get("_id")
    Comercio.update(comercio_id, set_attributes)
    comercio = Comercio.get_by_name(comercio_nome)
    return comercio


def remove_comercio(comercio_nome):
    _assert(comercio_nome and type(comercio_nome) is str, f'Erro: nome de comercio invalido')
    comercio = Comercio.get_by_name(comercio_nome)
    _assert(comercio, f'Erro: comercio com o nome {comercio_nome} não cadastrado!', SolanchesNotFoundError)
    result = Comercio.remove_comercio(comercio_nome)
    _assert(result, f'Erro: não foi possível remover o comércio com nome {comercio_nome}', SolanchesInternalServerError)
    return result


def get_cardapio(comercio_nome):
    _assert(comercio_nome and type(comercio_nome) is str, 'Erro: nome de comercio inválido!')
    comercio = Comercio.get_by_name(comercio_nome)
    _assert(comercio, f'Erro: comercio com o nome {comercio_nome} não cadastrado!', SolanchesNotFoundError)
    cardapio = Comercio.get_cardapio(comercio_nome)
    return cardapio


def cadastra_produto(comercio_nome, nome_produto, attributes):
    _assert(nome_produto and type(nome_produto) is str, "Erro: nome inválido!")
    _assert(type(attributes) is dict if attributes else True, "Erro: campo attributes inválidos!")
    comercio = Comercio.get_by_name(comercio_nome)
    _assert(comercio, f'Erro: comercio com o nome {comercio_nome} não cadastrado!', SolanchesNotFoundError)
    novo_produto = Produto(nome_produto, attributes)
    produto_cadastrado = Comercio.add_produto(novo_produto, comercio_nome)
    result = produto_cadastrado.to_dict()
    return result


def get_produto(comercio_nome, produto_id):
    _assert(type(produto_id) is str, "Erro: produto com id inválido!")
    comercio = Comercio.get_by_name(comercio_nome)
    _assert(comercio, f'Erro: comercio com o nome {comercio_nome} não cadastrado!', SolanchesNotFoundError)
    produto = Comercio.get_produto(comercio_nome, produto_id)
    _assert(produto, f'Erro: produto com o id {produto_id} não cadastrado no comercio!', SolanchesNotFoundError)
    return produto


def get_produtos(comercio_nome, has_categories=False):
    comercio = Comercio.get_by_name(comercio_nome)
    _assert(comercio, f'Erro: comercio com o nome {comercio_nome} não cadastrado!', SolanchesNotFoundError)
    produtos = Comercio.get_produtos(comercio_nome) if not has_categories else _get_produtos_categoria(comercio_nome)
    return produtos


def _get_produtos_categoria(comercio_nome):
    result = {}
    produtos = Comercio.get_produtos(comercio_nome)
    for produto in produtos:
        categoria = Comercio.get_produto_categoria(produto.get("_id"))
        result.setdefault(categoria, []).append(produto)
    return result

  
def get_produtos_ids(comercio_nome):
    comercio = Comercio.get_by_name(comercio_nome)
    _assert(comercio, f'Erro: comercio com o nome {comercio_nome} não cadastrado!', SolanchesNotFoundError)
    produtos = Comercio.get_produtos_ids(comercio_nome)
    return produtos


def edita_produto(produto_id, comercio_nome, attributes, nome):
    _assert(comercio_nome and type(comercio_nome) is str, "Erro: nome de comércio inválido")
    _assert(produto_id and type(produto_id) is str, "Erro: produto com id inválido!")
    _assert(attributes and type(attributes) is dict if attributes else True, "Erro: attributes inválidos!")
    _assert(nome and type(nome) is str if nome else True, "Erro: nome inválido!")

    comercio = Comercio.get_by_name(comercio_nome)
    _assert(comercio, f'Erro: comercio com o nome {comercio_nome} não cadastrado!', SolanchesNotFoundError)
    produto = Comercio.get_produto(comercio_nome, produto_id)
    _assert(produto, f'Erro: produto com o id {produto_id} não cadastrado no comercio!', SolanchesNotFoundError)
    
    set_fields = {f'attributes.{field}': value for field, value in attributes.items()} if attributes else {}
    set_fields["nome"] = nome if nome else None

    set_fields_filtered = {key:value for key, value in set_fields.items() if value}
    
    Comercio.update_produto(produto_id, set_fields_filtered)
    produto = Comercio.get_produto(comercio_nome, produto_id)
    return produto


def remove_produto(comercio_nome, produto_id):
    comercio = Comercio.get_by_name(comercio_nome)
    _assert(comercio, f'Erro: comercio com o nome {comercio_nome} não cadastrado!', SolanchesNotFoundError)
    produto_no_comercio =  produto_id in Comercio.get_produtos_ids(comercio_nome)
    _assert(produto_no_comercio, f'Erro: produto com o id {produto_id} não cadastrado no comercio!', SolanchesNotFoundError)
    Comercio.remove_produto(comercio_nome, produto_id)
    cardapio = get_cardapio(comercio_nome)
    return cardapio


def adiciona_destaque(comercio_nome, produto_id):
    _assert(comercio_nome and type(comercio_nome) is str, 'Erro: nome de comércio inválido')
    _assert(produto_id and type(produto_id) is str, 'Erro: produto com id inválido!')

    comercio = Comercio.get_by_name(comercio_nome)
    _assert(comercio, f'Erro: comercio com o nome {comercio_nome} não cadastrado!', SolanchesNotFoundError)
    produto_no_comercio =  produto_id in Comercio.get_produtos_ids(comercio_nome)
    _assert(produto_no_comercio, f'Erro: produto com o id {produto_id} não cadastrado no comercio!', SolanchesNotFoundError)
    produto_nos_destaques = produto_id in Comercio.get_destaques(comercio_nome)
    _assert(not produto_nos_destaques, f'Erro: produto já está nos destaques!')

    Comercio.add_destaque(comercio_nome, produto_id)
    cardapio = Comercio.get_cardapio(comercio_nome)
    return cardapio


def remove_produto_destaques(comercio_nome, produto_id):
    _assert(comercio_nome and type(comercio_nome) is str, 'Erro: nome de comércio inválido')
    comercio = Comercio.get_by_name(comercio_nome)
    _assert(comercio, f'Erro: comercio com o nome {comercio_nome} não cadastrado!', SolanchesNotFoundError)
    _assert(produto_id and type(produto_id) is str, 'Erro: produto com id inválido!')
    produto_no_comercio =  produto_id in Comercio.get_produtos_ids(comercio_nome)
    _assert(produto_no_comercio, f'Erro: produto com o id {produto_id} não cadastrado no comercio!', SolanchesNotFoundError)
    produto_nos_destaques = produto_id in Comercio.get_destaques(comercio_nome)
    _assert(produto_nos_destaques, f'Erro: produto com id {produto_id} não está nos destaques!')

    Comercio.remove_produto_destaques(comercio_nome, produto_id)
    cardapio = get_cardapio(comercio_nome)
    return cardapio


def adiciona_categoria(comercio_nome, categoria):
    _assert(categoria and type(categoria) is str, 'Erro: valor de categoria inválida!')
    comercio = Comercio.get_by_name(comercio_nome)
    _assert(comercio, f'Erro: comercio com o nome {comercio_nome} não cadastrado!', SolanchesNotFoundError)
    _assert(categoria not in Comercio.get_cardapio_categorias(comercio_nome), f'Erro: categoria já cadastrada nesse comércio!')

    Comercio.adiciona_categoria(comercio_nome, categoria)
    cardapio_atualizado = Comercio.get_cardapio(comercio_nome)
    return cardapio_atualizado


def remove_categoria(comercio_nome, categoria):
    _assert(type(categoria) is str, 'Erro: valor de categoria inválida!')
    comercio = Comercio.get_by_name(comercio_nome)
    _assert(comercio, f'Erro: comercio com o nome {comercio_nome} não cadastrado!', SolanchesNotFoundError)
    categorias = Comercio.get_cardapio_categorias(comercio_nome)
    _assert(categoria in categorias, 'Erro: categoria não faz parte do comércio')
    
    Comercio.remove_categoria(comercio_nome, categoria)
    cardapio_atualizado = Comercio.get_cardapio(comercio_nome)
    return cardapio_atualizado


def login(comercio_nome, password, secret):
    comercio = Comercio.get_by_name(comercio_nome)
    _assert(comercio, f'Erro: comercio com o nome {comercio_nome} não cadastrado!', SolanchesNotFoundError)
    _assert(Comercio.verify_password(comercio_nome, password), "Erro! Senha incorreta")

    payload = {
        'id': comercio.get("_id"),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }

    token = jwt.encode(payload, secret, algorithm="HS256")
    return token


def logout(token):
    block_token = BlockList(token)
    block_token.save()
