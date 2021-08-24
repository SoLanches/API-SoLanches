import hashlib
import time
import json

from . connect2db import DB


class Comercio:

    def __init__(self, nome, attributes):
        self.nome = nome
        self.attributes = attributes

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
        return comercio

    @staticmethod
    def get_all():
        comercios = DB.comercio.find()
        return list(comercios)

    @staticmethod
    def update(comercio_id, attributes):
        DB.comercio.update_one({"_id": comercio_id}, {"$set": {"attributes": attributes}})
        
    @staticmethod
    def get_by_name(name):
        query = {"nome": name}
        comercio = DB.comercio.find_one(query)
        return comercio

    @staticmethod
    def get_cardapio(comercio_nome):
        comercio = Comercio.get_by_name(comercio_nome)
        return Cardapio.get_by_id(comercio.get("cardapio"))

    @staticmethod
    def add_produto(produto, nome_comercio):
        produto_id = produto.save()
        comercio = Comercio.get_cardapio(nome_comercio)
        comercio_id = comercio.get("_id")
        Cardapio.add_produtos(comercio_id, produto_id)
        return produto_id
    
    @staticmethod
    def get_produtos(comercio_nome):
        comercio = Comercio.get_by_name(comercio_nome)
        cardapio_id = comercio.get("cardapio")
        produtos = Cardapio.get_produtos(cardapio_id)
        return produtos
    
    @staticmethod
    def get_destaques(comercio_nome):
        comercio = Comercio.get_by_name(comercio_nome)
        cardapio_id = comercio.get("cardapio")
        destaques = Cardapio.get_destaques(cardapio_id)
        return destaques

    @staticmethod
    def add_destaques(comercio_nome, destaques):
        comercio = Comercio.get_by_name(comercio_nome)
        Cardapio.add_destaques(comercio.get("cardapio"), destaques)

    @staticmethod
    def remove_comercio(comercio_nome):
        cardapio_id = Comercio.id(comercio_nome)
        Cardapio.remove_cardapio(cardapio_id)
        query = {"nome": comercio_nome}
        comercio_deletado = DB.comercio.delete_one(query)
        return comercio_deletado.deleted_count
        
    def remove_produto(comercio_nome, produto_id):
        comercio = Comercio.get_by_name(comercio_nome)
        cardapio_id = comercio.get("cardapio")
        Cardapio.remove_produto(cardapio_id, produto_id)

    def to_dict(self):
        comercio = vars(self).copy()
        return comercio


class Cardapio:

    def __init__(self, cardapio_id):
        self._id = cardapio_id
        self.produtos = []
        self.destaques = []

    def save(self):
        self.created_at = time.time()
        DB.cardapio.update_one({"_id": self._id}, {"$set": vars(self)}, upsert=True)
        return self._id

    @staticmethod
    def get_by_id(id):
        query = {"_id": id}
        cardapio = DB.cardapio.find_one(query)
        return cardapio
    
    @staticmethod
    def get_all():
        cardapios = DB.cardapio.find()
        return list(cardapios)

    @staticmethod
    def add_produtos(cardapio_id, produtos):
        query = {"_id": cardapio_id}
        cardapio = Cardapio.get_by_id(cardapio_id)
        new_produtos = cardapio.get("produtos")
        new_produtos += produtos if type(produtos) is list else [produtos]
        new_values = {"$set": {"produtos": new_produtos}}
        DB.cardapio.update_one(query, new_values)

    @staticmethod
    def remove_cardapio(cardapio_id):
      produtos = Cardapio.get_produtos(cardapio_id)
      query = {"_id": cardapio_id}
      DB.cardapio.remove(query) 
      Produto.remove_produtos(produtos)

    @staticmethod
    def add_destaques(cardapio_id, destaques):
        query = {"_id": cardapio_id}
        cardapio = Cardapio.get_by_id(cardapio_id)
        new_destaques = cardapio.get("destaques")
        new_destaques += destaques if type(destaques) is list else [destaques]
        new_values = {"$set": {"destaques": new_destaques}}
        DB.cardapio.update_one(query, new_values)  
  
    @staticmethod
    def get_produtos(cardapio_id):
        cardapio = Cardapio.get_by_id(cardapio_id)
        return cardapio.get("produtos")
    
    @staticmethod
    def get_destaques(cardapio_id):
        cardapio = Cardapio.get_by_id(cardapio_id)
        return cardapio.get("destaques")

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
    
    def to_dict(self):
        cardapio = vars(self).copy()
        return cardapio


class Produto:

    def __init__(self, nome, attributes={}):
        self.nome = nome
        self.attributes = attributes
    
    @staticmethod
    def id(nome, timestamp):
        id_fields = {"nome": nome, "timestamp": timestamp}
        serialized = json.dumps(id_fields, separators=(',', ':'), sort_keys=True, ensure_ascii=False)
        return hashlib.sha1(serialized.encode('utf-8')).hexdigest()  

    def save(self):
        self.created_at = time.time()
        self._id = Produto.id(self.nome, self.created_at)
        DB.produto.insert_one(vars(self))
        return self._id

    @staticmethod
    def update(produto_id, attributes):
        DB.produto.update_one({"_id": produto_id}, {"$set": {"attributes": attributes}})

    @staticmethod
    def get_by_id(id):
        query = {"_id": id}
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

        
    def to_dict(self):
        produto = vars(self).copy()
        return produto
