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
        id = db.comercio.insert_one(vars(self))
        return id
    
    @staticmethod
    def get_by_id(id):
        query = {"_id": id}
        comercio = db.comercio.find_one(query)
        return comercio

    @staticmethod
    def get_all():
        comercios = db.comercio.find()
        return list(comercios)
