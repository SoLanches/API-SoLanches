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
    
    assert(req, "Erro: json inválido!")
    assert("titulo" in req, "Erro: titulo não informado!")
    assert("descricao" in req, "Erro: descricao não informada!")
    assert("imagem" in req, "Erro: imagem não informada!")
    assert("preco" in req, "Erro: preco não informado!")
    assert("categoria" in req, "Erro: categoria não informada!")

    titulo = req.get("titulo")
    descricao = req.get("descricao")
    imagem = req.get("imagem")
    preco = req.get("preco")
    categoria = req.get("categoria")

    try:
        produto_id = controller.cadastra_produto(titulo, descricao, imagem, preco, categoria)
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
    