import time

from flask import Flask
from flask import jsonify
from flask import request
from . import controller

app = Flask(__name__)


started_at = time.time()


@app.route("/status", methods=["GET"])
def status():
    status = {
        "status": "operacional",
        "service": "api-solanches",
        "started_at": started_at,
        "timestamp": time.time()
    }
    return status, 200


@app.route("/produto", methods=['POST'])
def cadastra_produto():
    req = request.get_json()
    
    assert req, "Erro: json inválido!"
    assert "nome" in req, "Erro: nome não informado!"
    assert "descricao" in req, "Erro: descricao não informada!"
    assert "imagem" in req, "Erro: imagem não informada!"
    assert "preco" in req, "Erro: preco não informado!"
    assert "categoria" in req, "Erro: categoria não informada!"

    nome = req.get("nome")
    descricao = req.get("descricao")
    imagem = req.get("imagem")
    preco = req.get("preco")
    categoria = req.get("categoria")

    try:
        produto_id = controller.cadastra_produto(nome, descricao, imagem, preco, categoria)
    except:
        raise

    return jsonify(produto_id), 201


@app.route("/produto/<produto_id>", methods=['GET'])
def get_produto(produto_id):
    try:
        produto = controller.get_produto(produto_id)
    except:
        raise

    return jsonify(produto), 200

@app.route("/produtos", methods=['GET'])
def get_produtos():
    try:
        produtos = controller.get_produtos()
    except:
        raise

    return jsonify(produtos), 200 


@app.route("/comercios", methods=['GET'])
def get_comercios():
    try:
        comercios = controller.get_comercios()
    except:
        raise

    return jsonify(comercios), 200 


@app.route("/comercio", methods=['GET'])
def get_comercio():
    comercio_id = request.args.get('id')
    assert comercio_id, "Erro: id do comercio não informado!"
    try:
        comercio = controller.get_comercio(comercio_id)
    except:
        raise

    return jsonify(comercio), 200


@app.route("/comercio", methods=['POST'])
def cadastra_comercio():
    req = request.get_json()
    
    
    assert req, "Erro: json inválido!"
    assert "nome" in req, "Erro: nome não informado!"
    assert "endereco" in req, "Erro: endereco não informado!"
    assert "telefone" in req, "Erro: telefone não informado!"
    assert "email" in req, "Erro: email não informado!"
    assert "cnpj" in req, "Erro: cnpj não informado!"
    assert "horarios" in req, "Erro: horarios não informados!"
    assert "link_imagem" in req, "Erro: link da imagem não informado!"
    assert "tags" in req, "Erro: tags não informadas!"
    assert "redes_sociais" in req, "Erro: redes sociais não informadas!"

    nome = req.get("nome")
    endereco = req.get("endereco")
    telefone = req.get("telefone")
    email = req.get("email")
    cnpj = req.get("cnpj")
    horarios = req.get("horarios")
    link_imagem = req.get("link_imagem")
    tags = req.get("tags")
    redes_sociais = req.get("redes_sociais")

    try:
        comercio_id = controller.cadastra_comercio(nome, endereco, telefone, email, cnpj, horarios, link_imagem, tags, redes_sociais)
    except:
        raise

    return jsonify(comercio_id), 201


@app.route("/comercio/<comercio_nome>", methods=['GET'])
def get_comercio_by_name(comercio_nome):
    try:
        comercio = controller.get_comercio_by_name(comercio_nome)
    except:
        raise

    return jsonify(comercio), 200
    