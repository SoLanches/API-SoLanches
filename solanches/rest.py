import time
import logging

from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
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
    assert "attributes" in req, "Erro: atributos não informado"

    nome = req.get("nome")
    attributes = req.get("attributes")

    try:
        produto_id = controller.cadastra_produto(nome, attributes)
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
    assert "attributes" in req, "Erro: atributos não informado"

    nome = req.get("nome")
    attributes = req.get("attributes")

    try:
        comercio_id = controller.cadastra_comercio(nome, attributes)
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


@app.route("/comercio/<comercio_nome>/cardapio", methods=['GET'])
def get_cadapio(comercio_nome):
    try:
        cardapio = controller.get_cardapio(comercio_nome)
    except:
        raise

    return jsonify(cardapio), 200

@app.errorhandler(404)
def page_not_found(e):
    msg_erro = {"name": e.nome, "description": e.description, "code": e.code,
    "timestamp": time.time()}

    return jsonify(msg_erro), 404


@app.errorhandler(400)
def page_not_found(e):
    msg_erro = {"name": e.nome, "description": e.description, "code": e.code,
    "timestamp": time.time()}

    return jsonify(msg_erro), 400
