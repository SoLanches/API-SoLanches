import hashlib
import time
import json

from . connect2db import db

class Produto:

    def __init__(self, nome, descricao, preco, categoria, link_imagem=None):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria
        self.link_imagem = link_imagem
    
    @staticmethod
    def id(nome, timestamp):
        id_fields = {"nome": nome, "timestamp": timestamp}
        serialized = json.dumps(id_fields, separators=(',', ':'), sort_keys=True, ensure_ascii=False)
        return hashlib.sha1(serialized.encode('utf-8')).hexdigest()  

    def save(self):
        self.created_at = time.time()
        self._id = Produto.id(self.nome, self.created_at)
        id = db.produto.insert_one(vars(self))
        return id
      
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

    def __init__(self, nome, endereco, telefone, email, cnpj, horarios, link_imagem, tags, redes_sociais):
        self.cnpj = cnpj
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.horarios = horarios
        self.link_imagem = link_imagem
        self.tags = tags
        self.redes_sociais = redes_sociais

    @staticmethod
    def id(nome):
        id_fields = {"nome": nome}
        serialized = json.dumps(id_fields, separators=(',', ':'), sort_keys=True, ensure_ascii=False)
        return hashlib.sha1(serialized.encode('utf-8')).hexdigest() 

    def save(self):
        self.created_at = time.time()
        self._id = Comercio.id(self.nome)
        db.comercio.insert_one(vars(self))
    
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


class Cardapio:

    def __init__(self, comercio_id, produtos, destaques):
        self.comercio_id = comercio_id
        self.produtos = produtos
        self.destaques = destaques

    @staticmethod
    def id(comercio_id):
        id_fields = {"nome": comercio_id}
        serialized = json.dumps(id_fields, separators=(',', ':'), sort_keys=True, ensure_ascii=False)
        return hashlib.sha1(serialized.encode('utf-8')).hexdigest() 

    def save(self):
        self.created_at = time.time()
        self._id = self.comercio_id
        db.cardapio.insert_one(vars(self))
    
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