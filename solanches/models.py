from bson.objectid import ObjectId
from . connect2db import db

class Produto:

    def __init__(self, titulo, descricao, preco, categoria):
        self.titulo = titulo
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria
    
    def save(self):
        id = db.produto.insert_one({
            "titulo": self.titulo,
            "descricao": self.descricao,
            "preco": self.preco,
            "categoria": self.categoria
        })

        self._id = id
        return id

    @staticmethod
    def get_by_id(id):
        id = ObjectId(id)
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
        
        return list(comercios
