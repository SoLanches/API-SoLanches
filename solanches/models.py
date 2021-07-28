import hashlib
import time
import json

from . connect2db import db


class Produto:

    def __init__(self, nome, attributes):
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
        db.produto.update_one({"_id": self._id}, {"$set": vars(self)}, upsert=True)
        return self._id
      
    @staticmethod
    def get_by_id(id):
        query = {"_id": id}
        produto = db.produto.find_one(query)
        return produto

    @staticmethod
    def get_all():
        produtos = db.produto.find()
        return list(produtos)

    def to_dict(self):
        produto = vars(self).copy()
        return produto


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
        db.comercio.update_one({"_id": self._id}, {"$set": vars(self)}, upsert=True)
        return self._id
    
    @staticmethod
    def get_by_id(id):
        query = {"_id": id}
        comercio = db.comercio.find_one(query)
        return comercio

    @staticmethod
    def get_all():
        comercios = db.comercio.find()
        return list(comercios)

    def to_dict(self):
        comercio = vars(self).copy()
        return comercio
     
    @staticmethod
    def get_by_name(name):
        query = {"nome": name}
        comercio = db.comercio.find_one(query)
        return comercio


class Cardapio:

    def __init__(self, comercio_id, produtos=[], destaques=[]):
        self._id = comercio_id
        self.produtos = produtos
        self.destaques = destaques

    def save(self):
        self.created_at = time.time()
        db.cardapio.update_one({"_id": self._id}, {"$set": vars(self)}, upsert=True)

    @staticmethod
    def add_produtos(cardapio_id, produtos):
        query = {"_id": cardapio_id}
        cardapio = Cardapio.get_by_id(cardapio_id)
        new_produtos = cardapio.get("produtos")
        new_produtos += produtos if type(produtos) is list else [produtos]
        new_values = {"$set": {"produtos": new_produtos}}
        db.cardapio.update_one(query, new_values)

    @staticmethod
    def add_destaques(cardapio_id, destaques):
        query = {"_id": cardapio_id}
        cardapio = Cardapio.get_by_id(cardapio_id)
        new_destaques = cardapio.get("destaques")
        new_destaques += destaques if type(destaques) is list else [destaques]
        new_values = {"$set": {"destaques": new_destaques}}
        db.cardapio.update_one(query, new_values)  
    
    @staticmethod
    def get_by_id(id):
        query = {"_id": id}
        cardapio = db.cardapio.find_one(query)
        return cardapio
    
    @staticmethod
    def get_all():
        cardapios = db.cardapio.find()
        return list(cardapios)

    def to_dict(self):
        cardapio = vars(self).copy()
        return cardapio
  