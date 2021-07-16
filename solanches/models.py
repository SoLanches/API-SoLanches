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
