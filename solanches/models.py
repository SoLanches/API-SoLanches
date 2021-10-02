from datetime import datetime
import hashlib
import time
import json

from . connect2db import DB


class Comercio:

    def __init__(self, nome, password, attributes):
        self._id = None
        self.nome = nome
        self.password = password
        self.attributes = attributes
        self.cardapio = None
        self.created_at = None

    @staticmethod
    def id(nome):
        id_fields = {"nome": nome}
        serialized = json.dumps(id_fields, separators=(',', ':'), sort_keys=True, ensure_ascii=False)
        return hashlib.sha1(serialized.encode('utf-8')).hexdigest()

    def save(self):
        self.created_at = time.time()
        self._id = Comercio.id(self.nome)
        cardapio = Cardapio(self._id)
        self.cardapio = cardapio.save()
        DB.comercio.insert_one(vars(self))

    @staticmethod
    def get_by_id(id):
        query = {"_id": id}
        comercio = DB.comercio.find_one(query)
        if comercio and "password" in comercio:
            comercio.pop("password")        
        return comercio

    @staticmethod
    def get_by_name(name):
        query = {"nome": name}
        comercio = DB.comercio.find_one(query)
        if comercio and "password" in comercio:
            comercio.pop("password")
        return comercio

    @staticmethod
    def get_all():
        comercios = DB.comercio.find({}, {"password": 0})
        return list(comercios)

    @staticmethod
    def update(comercio_id, attributes):
        DB.comercio.update_one({"_id": comercio_id}, {"$set": attributes})

    @staticmethod
    def get_cardapio(comercio_nome):
        comercio = Comercio.get_by_name(comercio_nome)
        return Cardapio.get_by_id(comercio.get("cardapio"))

    @staticmethod
    def add_produto(nome_comercio, produto_data):
        cardapio = Comercio.get_cardapio(nome_comercio)
        cardapio_id = cardapio.get("_id")
        novo_produto = Cardapio.add_produto(cardapio_id, produto_data)
        return novo_produto

    @staticmethod
    def get_produto(comercio_nome, produto_id):
        comercio = Comercio.get_by_name(comercio_nome)
        cardapio_id = comercio.get("cardapio")
        produto = Cardapio.get_produto(cardapio_id, produto_id)
        return produto

    @staticmethod
    def get_produtos(comercio_nome):
        comercio = Comercio.get_by_name(comercio_nome)
        cardapio_id = comercio.get("cardapio")
        produtos = Cardapio.get_produtos(cardapio_id)
        return produtos

    @staticmethod
    def get_produtos_ids(comercio_nome):
        comercio = Comercio.get_by_name(comercio_nome)
        cardapio_id = comercio.get("cardapio")
        produtos = Cardapio.get_produtos_ids(cardapio_id)
        return produtos

    @staticmethod
    def get_destaques(comercio_nome):
        comercio = Comercio.get_by_name(comercio_nome)
        cardapio_id = comercio.get("cardapio")
        destaques = Cardapio.get_destaques(cardapio_id)
        return destaques

    @staticmethod
    def add_destaque(comercio_nome, destaque):
        comercio = Comercio.get_by_name(comercio_nome)
        Cardapio.add_destaque(comercio.get("cardapio"), destaque)

    @staticmethod
    def update_produto(produto_id, fields):
        Cardapio.update_produto(produto_id, fields)

    @staticmethod
    def remove_comercio(comercio_nome):
        cardapio_id = Comercio.id(comercio_nome)
        Cardapio.remove_cardapio(cardapio_id)
        query = {"nome": comercio_nome}
        comercio_deletado = DB.comercio.delete_one(query)
        return comercio_deletado.deleted_count
    
    @staticmethod
    def verify_password(comercio_nome, password):
        query = {"nome": comercio_nome}
        comercio = DB.comercio.find_one(query)
        return comercio.get('password') == password

    @staticmethod
    def remove_produto(comercio_nome, produto_id):
        comercio = Comercio.get_by_name(comercio_nome)
        cardapio_id = comercio.get("cardapio")
        Cardapio.remove_produto(cardapio_id, produto_id)

    @staticmethod
    def remove_produto_destaques(comercio_nome, produto_id):
        comercio = Comercio.get_by_name(comercio_nome)
        Cardapio.remove_produto_destaques(comercio.get("cardapio"), produto_id)

    @staticmethod
    def get_categoria(comercio_nome):
        comercio = Comercio.get_by_name(comercio_nome)
        attributes = comercio.get("attributes")
        categoria = attributes.get("categoria", "")
        return categoria.strip(" ")

    @staticmethod
    def get_produto_categoria(produto_id):
        categoria = Cardapio.get_produto_categoria(produto_id)
        return categoria

    @staticmethod
    def adiciona_categoria(comercio_nome, categoria):
        comercio = Comercio.get_by_name(comercio_nome)
        Cardapio.add_categoria(comercio.get("cardapio"), categoria)

    @staticmethod
    def remove_categoria(comercio_nome, categoria):
        comercio = Comercio.get_by_name(comercio_nome)
        Cardapio.remove_categoria(comercio.get("cardapio"), categoria)

    @staticmethod
    def get_cardapio_categorias(comercio_nome):
        comercio = Comercio.get_by_name(comercio_nome)
        categorias = Cardapio.get_categorias(comercio.get("cardapio"))
        return categorias

    def to_dict(self):
        comercio = vars(self).copy()
        if "password" in comercio:
            comercio.pop("password")
        return comercio


class Cardapio:

    def __init__(self, cardapio_id):
        self._id = cardapio_id
        self.produtos = []
        self.destaques = []
        self.categorias = []
        self.created_at = None

    def save(self):
        self.created_at = time.time()
        DB.cardapio.update_one({"_id": self._id}, {"$set": vars(self)}, upsert=True)
        return self._id

    @staticmethod
    def get_by_id(cardapio_id):
        query = {"_id": cardapio_id}
        cardapio = DB.cardapio.find_one(query)
        return cardapio

    @staticmethod
    def get_all():
        cardapios = DB.cardapio.find()
        return list(cardapios)

    @staticmethod
    def add_produto(cardapio_id, produto_data):
        produto_nome = produto_data.get("nome")
        produto_attributes = produto_data.get("attributes")
        novo_produto = Produto(produto_nome, produto_attributes)
        produto_id = novo_produto.save()

        cardapio = Cardapio.get_by_id(cardapio_id)
        cardapio_produtos = cardapio.get("produtos")
        cardapio_produtos.append(produto_id)

        query = {"_id": cardapio_id}
        new_values = {"$set": {"produtos": cardapio_produtos}}
        DB.cardapio.update_one(query, new_values)
        return novo_produto

    @staticmethod
    def remove_cardapio(cardapio_id):
        produtos = Cardapio.get_produtos(cardapio_id)
        query = {"_id": cardapio_id}
        DB.cardapio.remove(query) 
        Produto.remove_produtos(produtos)

    @staticmethod
    def add_destaque(cardapio_id, destaque):
        query = {"_id": cardapio_id}
        cardapio = Cardapio.get_by_id(cardapio_id)
        new_destaques = cardapio.get("destaques")
        new_destaques += destaque if type(destaque) is list else [destaque]
        new_values = {"$set": {"destaques": new_destaques}}
        DB.cardapio.update_one(query, new_values)

    @staticmethod
    def get_produto(cardapio_id, produto_id):
        cardapio = Cardapio.get_by_id(cardapio_id)
        produtos = cardapio.get("produtos")
        produto = Produto.get_by_id(produto_id) if produto_id in produtos else None
        return produto

    @staticmethod
    def get_produtos(cardapio_id):
        cardapio = Cardapio.get_by_id(cardapio_id)
        produtos = [Produto.get_by_id(produto) for produto in cardapio.get("produtos")]
        return produtos

    @staticmethod
    def get_produtos_ids(cardapio_id):
        cardapio = Cardapio.get_by_id(cardapio_id)
        produtos = cardapio.get("produtos")
        return produtos

    @staticmethod
    def get_destaques(cardapio_id):
        cardapio = Cardapio.get_by_id(cardapio_id)
        return cardapio.get("destaques")

    @staticmethod
    def update_produto(produto_id, fields):
        Produto.update(produto_id, fields)

    @staticmethod
    def remove_produto(cardapio_id, produto_id):
        query = {"_id": cardapio_id}
        cardapio = Cardapio.get_by_id(cardapio_id)
        new_destaques = cardapio.get("destaques")
        new_destaques.remove(produto_id) if produto_id in new_destaques else new_destaques
        new_produtos = cardapio.get("produtos")
        new_produtos.remove(produto_id) if produto_id in new_produtos else new_produtos
        new_values = {"$set": {"destaques": new_destaques, "produtos": new_produtos}}
        DB.cardapio.update_one(query, new_values)
        Produto.remove(produto_id)
        
    @staticmethod
    def remove_produto_destaques(cardapio_id, produto_id):
        query = {"_id": cardapio_id}
        cardapio = Cardapio.get_by_id(cardapio_id)
        destaques = cardapio.get("destaques")
        destaques.remove(produto_id) if produto_id in destaques else destaques
        new_destaques = {"$set": {"destaques": destaques}}
        DB.cardapio.update_one(query, new_destaques)
    
    @staticmethod
    def get_produto_categoria(produto_id):
        categoria = Produto.get_categoria(produto_id)
        return categoria

    @staticmethod
    def add_categoria(cardapio_id, categoria):
        query = {"_id": cardapio_id}
        cardapio = Cardapio.get_by_id(cardapio_id)
        categorias = cardapio.get("categorias")
        categorias.append(categoria)
        new_values = {"$set": {"categorias": categorias}}
        DB.cardapio.update_one(query, new_values)

    @staticmethod
    def remove_categoria(cardapio_id, categoria):
        query = {"_id": cardapio_id}
        cardapio = Cardapio.get_by_id(cardapio_id)
        categories = cardapio.get("categorias")
        categories.remove(categoria) if categoria in categories else categories
        new_values = {"$set": {"categorias": categories}}
        DB.cardapio.update_one(query, new_values)

    @staticmethod
    def get_categorias(cardapio_id):
        cardapio = Cardapio.get_by_id(cardapio_id)
        categorias = cardapio.get("categorias")
        return categorias

    def to_dict(self):
        cardapio = vars(self).copy()
        return cardapio


class Produto:

    def __init__(self, nome, attributes={}):
        self._id = None
        self.nome = nome
        self.attributes = attributes
        self.created_at = None

    @staticmethod
    def id(nome, timestamp):
        id_fields = {"nome": nome, "timestamp": timestamp}
        serial_arq = json.dumps(id_fields, separators=(',', ':'), sort_keys=True, ensure_ascii=False)
        return hashlib.sha1(serial_arq.encode('utf-8')).hexdigest()  

    def save(self):
        self.created_at = time.time()
        self._id = Produto.id(self.nome, self.created_at)
        DB.produto.insert_one(vars(self))
        return self._id

    @staticmethod
    def update(produto_id, fields):
        DB.produto.update_one({"_id": produto_id}, {"$set": fields})

    @staticmethod
    def get_by_id(produto_id):
        query = {"_id": produto_id}
        produto = DB.produto.find_one(query)
        return produto

    @staticmethod
    def remove_produtos(produtos):
        query = {"_id": { "$in": produtos}}
        DB.produto.remove(query) 
  
    @staticmethod
    def get_all():
        produtos = DB.produto.find()
        return list(produtos)

    @staticmethod
    def remove(produto_id):
        query = {"_id": produto_id}
        DB.produto.remove(query)
    
    @staticmethod
    def get_categoria(produto_id):
        produto = Produto.get_by_id(produto_id)
        attributes = produto.get("attributes")
        categoria = attributes.get("categoria", "")
        return categoria.strip(" ")

    def to_dict(self):
        produto = vars(self).copy()
        return produto


class BlockList:

    def __init__(self, token):
        self._id = token
    
    def save(self):
        self.date = datetime.utcnow()
        DB.block_list.insert_one(vars(self))
        return self._id

    @staticmethod
    def contains(token):
        query = {"_id": token}
        token_get = DB.block_list.find_one(query)

        return bool(token_get)
