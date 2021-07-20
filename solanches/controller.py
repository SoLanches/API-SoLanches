from . models import Produto, Comercio


def cadastra_produto(titulo, descricao, imagem, preco, categoria):
    assert(titulo and type(titulo) is str, "Erro: titulo inválido!")
    assert(descricao and type(descricao) is str, "Erro: descricao inválida!")
    #assert(imagem and type(imagem) is str, "Erro: imagem inválida!")
    assert(preco and type(preco) is float, "Erro: preco inválido!")
    assert(categoria and type(categoria) is str, "Erro: categoria inválida!")

    novo_produto = Produto(titulo, descricao, preco, categoria)
    produto_id = novo_produto.save()

    return produto_id


def get_produto(produto_id):
    assert(produto_id and type(produto_id) is str, "Erro: produto com id inválido!")

    produto = Produto.get_by_id(produto_id)
    assert(produto, "Erro: produto com id não cadastrado!")

    return produto


def get_produtos():
    produtos = Produto.get_all()

    return produtos
    
def get_comercios():
    return Comercio.get_all()

def get_comercio(comercio_id):
    assert(comercio_id and type(comercio_id) is str, f'Erro: comercio com id {comercio_id} inválido!')

    comercio = Comercio.get_by_id(comercio_id)
    assert(comercio, f'Erro: comercio com id {comercio_id} não cadastrado!')

    return comercio