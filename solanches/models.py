from . connect2db import db
import json
import hashlib

class Produto:

    def __init__(self, titulo, descricao, preco, categoria):
        self.titulo = titulo
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria

    def id(self):
        id_fields = vars(self)
        serialized = json.dumps(id_fields, separators=(',', ':'), sort_keys=True, ensure_ascii=False)
        self._id = self.id
        return hashlib.sha1(serialized.encode('utf-8')).hexdigest()
    
    def save(self):
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
        self._id = cnpj
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.horarios = horarios
        self.link_imagem = link_imagem
        self.tags = tags
        self.redes_sociais = redes_sociais

    def save(self):
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

