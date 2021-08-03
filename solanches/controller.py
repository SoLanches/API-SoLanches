from . models import Produto, Comercio, Cardapio


def cadastra_produto(nome, descricao, imagem, preco, categoria, nome_comercio):
    assert nome and type(nome) is str, "Erro: nome inválido!"
    assert descricao and type(descricao) is str, "Erro: descricao inválida!"
    assert imagem and type(imagem) is str, "Erro: imagem inválida!"
    assert preco and type(preco) is float, "Erro: preco inválido!"
    assert categoria and type(categoria) is str, "Erro: categoria inválida!"
    assert nome_comercio and type(nome_comercio) is str, "Erro: nome de comercio invalido"

    novo_produto = Produto(nome, descricao, preco, categoria, imagem)
    novo_produto.save(nome_comercio)

    return novo_produto.to_dict()


def get_produto(produto_id):
    assert produto_id and type(produto_id) is str, "Erro: produto com id inválido!"

    produto = Produto.get_by_id(produto_id)
    assert produto, "Erro: produto com id não cadastrado!"

    return produto


def get_produtos():
    produtos = Produto.get_all()

    return produtos
 

def get_comercios():
    return Comercio.get_all()


def get_comercio(comercio_id):
    assert comercio_id and type(comercio_id) is str, f'Erro: comercio com id {comercio_id} inválido!'

    comercio = Comercio.get_by_id(comercio_id)
    assert comercio, f'Erro: comercio com id {comercio_id} não cadastrado!'

    return comercio


def cadastra_comercio(nome, attributes):
    assert nome and type(nome) is str, "Erro: nome inválido!"
    assert attributes and type(attributes) is dict, "Erro: campo attributes inválidos!"
    assert "telefone" in attributes, "Erro: Telefone não informado"
    
    novo_comercio = Comercio(nome, attributes)
    novo_comercio.save()

    return novo_comercio.to_dict()


def get_comercio_by_name(comercio_nome):
    assert comercio_nome and type(comercio_nome) is str, f'Erro: nome de comercio inválido!'
    
    comercio = Comercio.get_by_name(comercio_nome)
    assert comercio, f'Erro: comercio com nome {comercio_nome} nao cadastrado!'

    return comercio


def get_cardapio(comercio_nome):
    assert comercio_nome and type(comercio_nome) is str, f'Erro: nome de comercio inválido!'

    cardapio = Comercio.get_cardapio(comercio_nome)
    assert cardapio, f'Erro: cardapio não encontrado!'

    return cardapio
