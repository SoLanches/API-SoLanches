from connect2db import db


def inserir_produto(titulo, descricao, preco, categoria):
    
    id = db.produto.insert_one({
        "titulo": titulo,
        "descricao": descricao,
        "preco": preco,
        "categoria": categoria
    })

    return id