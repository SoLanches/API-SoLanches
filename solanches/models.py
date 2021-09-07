"""
high level support for doing this and that.
"""
import hashlib
import time
import json

from . connect2db import DB


class Comercio:
    """
    trade's model
    """
    def __init__(self, nome, attributes):
        """
        high level support for init
        """
        self.nome = nome
        self.attributes = attributes

    @staticmethod
    def id(nome):
        """
        high level support for id_comercio
        """
        id_fields = {"nome": nome}
        serialized = json.dumps(id_fields, separators=(',', ':'), sort_keys=True, ensure_ascii=False)
        return hashlib.sha1(serialized.encode('utf-8')).hexdigest()

    def save(self):
        """
        high level support for save
        """
        self.created_at = time.time()
        self._id = Comercio.id(self.nome)
        cardapio = Cardapio(self._id)
        self.cardapio = cardapio.save()
        DB.comercio.insert_one(vars(self))

    @staticmethod
    def get_by_id(id):
        """
        high level about return a trade from a id
        """
        query = {"_id": id}
        comercio = DB.comercio.find_one(query)
        return comercio

    @staticmethod
    def get_all():
        """
        high level about return all trades
        """
        comercios = DB.comercio.find()
        return list(comercios)

    @staticmethod
    def update(comercio_id, attributes):
        """
        high level about update a trade
        """
        DB.comercio.update_one({"_id": comercio_id}, {"$set": attributes})

    @staticmethod
    def get_by_name(name):
        """
        high level about return a trade from a name
        """
        query = {"nome": name}
        comercio = DB.comercio.find_one(query)
        return comercio

    @staticmethod
    def get_cardapio(comercio_nome):
        """
        high level about return a menu
        """
        comercio = Comercio.get_by_name(comercio_nome)
        return Cardapio.get_by_id(comercio.get("cardapio"))

    @staticmethod
    def add_produto(produto, nome_comercio):
        """
        high level about add a product
        """
        produto_id = produto.save()
        comercio = Comercio.get_cardapio(nome_comercio)
        comercio_id = comercio.get("_id")
        Cardapio.add_produtos(comercio_id, produto_id)
        return produto_id

    @staticmethod
    def get_produtos(comercio_nome):
        """
        high level about return all products
        """
        comercio = Comercio.get_by_name(comercio_nome)
        cardapio_id = comercio.get("cardapio")
        produtos = Cardapio.get_produtos(cardapio_id)
        return produtos

    @staticmethod
    def get_destaques(comercio_nome):
        """
        high level about return all hightlights
        """
        comercio = Comercio.get_by_name(comercio_nome)
        cardapio_id = comercio.get("cardapio")
        destaques = Cardapio.get_destaques(cardapio_id)
        return destaques

    @staticmethod
    def add_destaques(comercio_nome, destaques):
        """
        high level about add hightlights
        """
        comercio = Comercio.get_by_name(comercio_nome)
        Cardapio.add_destaques(comercio.get("cardapio"), destaques)

    @staticmethod
    def remove_comercio(comercio_nome):
        """
        high level about remove trade
        """
        cardapio_id = Comercio.id(comercio_nome)
        Cardapio.remove_cardapio(cardapio_id)
        query = {"nome": comercio_nome}
        comercio_deletado = DB.comercio.delete_one(query)
        return comercio_deletado.deleted_count

    def remove_produto(comercio_nome, produto_id):
        """
        high level about remove product
        """
        comercio = Comercio.get_by_name(comercio_nome)
        cardapio_id = comercio.get("cardapio")
        Cardapio.remove_produto(cardapio_id, produto_id)

    def to_dict(self):
        """
        high level support for turn into dictionary
        """
        comercio = vars(self).copy()
        return comercio

    @staticmethod
    def get_produto_categoria(produto_id):
        categoria = Cardapio.get_produto_categoria(produto_id)
        return categoria


class Cardapio:
    """
    menu's model
    """
    def __init__(self, cardapio_id):
        """
        high level support for init
        """
        self._id = cardapio_id
        self.produtos = []
        self.destaques = []

    def save(self):
        """
        high level support for save
        """
        self.created_at = time.time()
        DB.cardapio.update_one({"_id": self._id}, {"$set": vars(self)}, upsert=True)
        return self._id

    @staticmethod
    def get_by_id(id_cardapio):
        """
        high level about return a menu from a id
        """
        query = {"_id": id_cardapio}
        cardapio = DB.cardapio.find_one(query)
        return cardapio

    @staticmethod
    def get_all():
        """
        high level about return all menu
        """
        cardapios = DB.cardapio.find()
        return list(cardapios)

    @staticmethod
    def add_produtos(cardapio_id, produtos):
        """
        high level support for add product
        """
        query = {"_id": cardapio_id}
        cardapio = Cardapio.get_by_id(cardapio_id)
        new_produtos = cardapio.get("produtos")
        new_produtos += produtos if type(produtos) is list else [produtos]
        new_values = {"$set": {"produtos": new_produtos}}
        DB.cardapio.update_one(query, new_values)

    @staticmethod
    def remove_cardapio(cardapio_id):
        """
        high level support for remove a menu
        """
        produtos = Cardapio.get_produtos(cardapio_id)
        query = {"_id": cardapio_id}
        DB.cardapio.remove(query) 
        Produto.remove_produtos(produtos)

    @staticmethod
    def add_destaques(cardapio_id, destaques):
        """
        high level support for add a hightlights
        """
        query = {"_id": cardapio_id}
        cardapio = Cardapio.get_by_id(cardapio_id)
        new_destaques = cardapio.get("destaques")
        new_destaques += destaques if type(destaques) is list else [destaques]
        new_values = {"$set": {"destaques": new_destaques}}
        DB.cardapio.update_one(query, new_values)

    @staticmethod
    def get_produtos(cardapio_id):
        """
        high level support for return all products
        """
        cardapio = Cardapio.get_by_id(cardapio_id)
        return cardapio.get("produtos")

    @staticmethod
    def get_destaques(cardapio_id):
        """
        high level support for return aall hightlights
        """
        cardapio = Cardapio.get_by_id(cardapio_id)
        return cardapio.get("destaques")

    @staticmethod
    def remove_produto(cardapio_id, produto_id):
        """
        high level support for remove product
        """
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
    def get_produto_categoria(produto_id):
        categoria = Produto.get_categoria(produto_id)
        return categoria

    def to_dict(self):
        """
        high level support for turn into dictionary
        """
        cardapio = vars(self).copy()
        return cardapio


class Produto:
    """
    product's model
    """
    def __init__(self, nome, attributes={}):
        """
        high level support for init
        """
        self.nome = nome
        self.attributes = attributes

    @staticmethod
    def id(nome, timestamp):
        """
        high level support for id_comercio
        """
        id_fields = {"nome": nome, "timestamp": timestamp}
        serial_arq = json.dumps(id_fields, separators=(',', ':'), sort_keys=True, ensure_ascii=False)
        return hashlib.sha1(serial_arq.encode('utf-8')).hexdigest()  

    def save(self):
        """
        high level support for save
        """
        self.created_at = time.time()
        self._id = Produto.id(self.nome, self.created_at)
        DB.produto.insert_one(vars(self))
        return self._id

    @staticmethod
    def update(produto_id, attributes):
        """
        high level support for update product
        """
        DB.produto.update_one({"_id": produto_id}, {"$set": attributes})

    @staticmethod
    def get_by_id(produto_id):
        """
        high level support for return product from id
        """
        query = {"_id": produto_id}
        produto = DB.produto.find_one(query)
        return produto

    @staticmethod
    def remove_produtos(produtos):
        """
        high level support for remove product
        """
        query = {"_id": { "$in": produtos}}
        DB.produto.remove(query) 
  
    @staticmethod
    def get_all():
        """
        high level support for return all products
        """
        produtos = DB.produto.find()
        return list(produtos)

    @staticmethod
    def remove(produto_id):
        """
        high level support for remove
        """
        query = {"_id": produto_id}
        DB.produto.remove(query)
    
    @staticmethod
    def get_categoria(produto_id):
        produto = Produto.get_by_id(produto_id)
        attributes = produto.get("attributes")
        categoria = attributes.get("categoria", "")
        return categoria.strip(" ")

    def to_dict(self):
        """
        high level support for turn into dictionary
        """
        produto = vars(self).copy()
        return produto
