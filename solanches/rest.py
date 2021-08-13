import time
import logging

from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from flask import abort
from . import controller

app = Flask(__name__)


started_at = time.time()


def _assert(condition, status_code, message):
    if condition: return
    data = {
        "message": message,
        "status_code": status_code
    }
    response = make_response(jsonify(data), status_code)
    abort(response)


@app.route("/status", methods=["GET"])
def status():
    status = {
        "status": "operacional",
        "service": "api-solanches",
        "started_at": started_at,
        "timestamp": time.time()
    }
    return status, 200


@app.route("/comercio", methods=['POST'])
def cadastra_comercio():
    req = request.get_json()
    
    _assert(req, 400, "Erro: json inválido!")
    _assert("nome" in req, 400, "Erro: nome não informado!")
    _assert("attributes" in req, 400, "Erro: atributos não informado")

    nome = req.get("nome")
    attributes = req.get("attributes")

    try:
        comercio_id = controller.cadastra_comercio(nome, attributes)
    except Exception as error:
        _assert(False, 400, str(error))

    return jsonify(comercio_id), 201


@app.route("/comercios", methods=['GET'])
def get_comercios():
    try:
        comercios = controller.get_comercios()
    except Exception as error:
        _assert(False, 400, str(error))

    return jsonify(comercios), 200 


@app.route("/comercio", methods=['GET'])
def get_comercio():
    comercio_id = request.args.get('id')
    _assert(comercio_id, 400, "Erro: id do comercio não informado!")
    try:
        comercio = controller.get_comercio(comercio_id)
    except Exception as error:
        _assert(False, 400, str(error))

    return jsonify(comercio), 200


@app.route("/comercio/<comercio_nome>", methods=['GET'])
def get_comercio_by_name(comercio_nome):
    try:
        comercio = controller.get_comercio_by_name(comercio_nome)
    except Exception as error:
        _assert(False, 400, str(error))

    return jsonify(comercio), 200


@app.route("/comercio/<comercio_nome>/cardapio", methods=['GET'])
def get_cadapio(comercio_nome):
    try:
        cardapio = controller.get_cardapio(comercio_nome)
    except Exception as error:
        _assert(False, 400, str(error))
    return jsonify(cardapio), 200


@app.route("/comercio/<comercio_nome>/produto", methods=['POST'])
def cadastra_produto(comercio_nome):
    req = request.get_json()
    
    _assert(req, 400, "Erro: json inválido!")
    nome_produto = req.get("nome")
    _assert(nome_produto, 400, "Erro: nome não informado!")

    attributes = req.get("attributes") if "attributes" in req else {}

    try:
        produto_id = controller.cadastra_produto(comercio_nome, nome_produto, attributes)
        msg = {"message": f"Produto com o id {produto_id} adicionado"}
    except Exception as error:
        _assert(False, 400, str(error))

    return jsonify(msg), 201

 
@app.route("/comercio/<comercio_nome>/destaques", methods=['POST'])
def adiciona_destaques(comercio_nome):
    req = request.get_json()
    assert req, "Erro: json inválido!"
    assert "destaques" in req, "Erro: destaques não informados!"
    
    destaques = req.get("destaques")

    try:
        controller.adiciona_destaques(destaques, comercio_nome)
        msg = {"message": f"destaques adicionados"}
    except Exception as error:
        _assert(False, 400, str(error))

    return jsonify(msg), 201


#TODO: sumirá
@app.route("/produto/<produto_id>", methods=['GET'])
def get_produto(produto_id):
    try:
        produto = controller.get_produto(produto_id)
    except Exception as error:
        _assert(False, 400, str(error))

    return jsonify(produto), 200


#TODO: sumirá
@app.route("/produtos", methods=['GET'])
def get_produtos():
    try:
        produtos = controller.get_produtos()
    except Exception as error:
        _assert(False, 400, str(error))

    return jsonify(produtos), 200 


@app.errorhandler(Exception)
def _error(error):
    data = {}
    data["error"]  = error.__class__.__name__
    data["message"] = str(error)
    client_errors = ["BadRequest"]
    data["status_code"] = 400 if data["error"] in client_errors else 500
    return data, data["status_code"]


@app.route("/comercio/<comercio_nome>", methods=['PATCH'])
def update_comercio(comercio_nome):

    req = request.get_json()  
    assert req, "Erro: json inválido!"

    try:
        controller.atualiza_comercio(req, comercio_nome)
        msg = {"message": f"comercio atualizado"}
    except Exception as error:
        _assert(False, 400, str(error))

    return jsonify(msg), 201
   
    


