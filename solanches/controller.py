from . models import Produto

def cadastra_produto(titulo, descricao, imagem, preco, categoria):
    assert(titulo and type(titulo) is str, "Erro: titulo inválido!")
    assert(descricao and type(descricao) is str, "Erro: descricao inválida!")
    #assert(imagem and type(imagem) is str, "Erro: imagem inválida!")
    assert(preco and type(preco) is float, "Erro: preco inválido!")
    assert(categoria and type(categoria) is float, "Erro: categoria inválida!")

    novo_produto = Produto(titulo, descricao, preco, categoria)
    produto_id = novo_produto.save()

    return produto_id