from solanches.custom_erros import SolanchesComercioNaoEncontrado, SolanchesDuplicateKey, SolanchesProdutoNaoEncontrado, SolanchesProdutoNaoEstaNoCardapio
import time

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
    except SolanchesDuplicateKey as erro_chave:
        raise SolanchesDuplicateKey(erro_chave.message)
    except Exception as erro_interno:
        raise Exception(erro_interno)

    return jsonify(comercio_id), 201


@app.route("/comercios", methods=['GET'])
def get_comercios():
    try:
        comercios = controller.get_comercios()
    except Exception as erro_interno:
        raise Exception(erro_interno)

    return jsonify(comercios), 200


@app.route("/comercio", methods=['GET'])
def get_comercio():
    comercio_id = request.args.get('id')
    _assert(comercio_id, 400, "Erro: id do comercio não informado!")
    try:
        comercio = controller.get_comercio(comercio_id)
    except SolanchesComercioNaoEncontrado as erro_comercio:
        raise(SolanchesComercioNaoEncontrado(erro_comercio.message))
    except Exception as erro_interno:
        raise Exception(erro_interno)

    return jsonify(comercio), 200


@app.route("/comercio/<comercio_nome>", methods=['GET'])
def get_comercio_by_name(comercio_nome):
    try:
        comercio = controller.get_comercio_by_name(comercio_nome)
    except SolanchesComercioNaoEncontrado as erro_comercio:
        raise(SolanchesComercioNaoEncontrado(erro_comercio.message))
    except Exception as erro_interno:
        raise Exception(erro_interno)

    return jsonify(comercio), 200


@app.route("/comercio/<comercio_nome>", methods=['PATCH'])
def edita_comercio(comercio_nome):
    req = request.get_json()  
    _assert(req, 400, "Erro: json inválido!")

    attributes = req.get("attributes", {})
    _assert(type(attributes) is dict, 400, "Erro: campo attributes deve ser do tipo dict")

    try:
        comercio_atualizado = controller.atualiza_comercio(attributes, comercio_nome)
    except SolanchesComercioNaoEncontrado as erro_comercio:
        raise SolanchesComercioNaoEncontrado(erro_comercio.message)
    except Exception as erro_interno:
        raise Exception(erro_interno)

    return jsonify(comercio_atualizado), 200


@app.route("/comercio/<comercio_nome>", methods=['DELETE'])
def remove_comercio(comercio_nome):
    try:
        result = controller.remove_comercio(comercio_nome)
        msg = {"message": f"comercio {comercio_nome} removido com sucesso", "status_code": 200} if result else {"erro": "não foi possível remover o comércio", "status_code": 500}
    except SolanchesComercioNaoEncontrado as erro_comercio:
        raise SolanchesComercioNaoEncontrado(erro_comercio.message)
    except Exception as erro_interno:
        raise Exception(erro_interno)

    return jsonify(msg), msg["status_code"]


@app.route("/comercio/<comercio_nome>/cardapio", methods=['GET'])
def get_cardapio(comercio_nome):
    try:
        cardapio = controller.get_cardapio(comercio_nome)
    except SolanchesComercioNaoEncontrado as erro_comercio:
        raise SolanchesComercioNaoEncontrado(erro_comercio.message)
    except Exception as erro_interno:
        raise Exception(erro_interno)

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
    except SolanchesComercioNaoEncontrado as erro_comercio:
        raise SolanchesComercioNaoEncontrado(erro_comercio.message)
    except Exception as erro_interno:
        raise Exception(erro_interno)

    return jsonify(msg), 201


#TODO: será adaptado
@app.route("/produto/<produto_id>", methods=['GET'])
def get_produto(produto_id):
    try:
        produto = controller.get_produto(produto_id)
    except SolanchesProdutoNaoEncontrado as erro_produto:
        raise SolanchesProdutoNaoEncontrado(erro_produto.message)

    return jsonify(produto), 200


@app.route("/comercio/<comercio_nome>/produtos", methods=['GET'])
def get_produtos(comercio_nome):
    categories = request.args.get("categories", "")
    has_categories = categories.lower() == "true"
    try:
        produtos = controller.get_produtos(comercio_nome, has_categories)
    except SolanchesComercioNaoEncontrado as erro_comercio:
        raise SolanchesComercioNaoEncontrado(erro_comercio.message)
    except Exception as erro_interno:
        raise Exception(erro_interno)   

    return jsonify(produtos), 200


@app.route("/comercio/<comercio_nome>/produto/<produto_id>", methods=['PATCH'])
def edita_produto(comercio_nome, produto_id):
    req = request.get_json()
    _assert(req, 400, "Erro: json inválido!")
    
    attributes = req.get("attributes") if "attributes" in req else {}

    try:
        produto = controller.edita_produto(produto_id, comercio_nome, attributes)
    except SolanchesComercioNaoEncontrado as erro_comercio:
        raise SolanchesComercioNaoEncontrado(erro_comercio.message)
    except SolanchesProdutoNaoEncontrado as erro_produto:
        raise SolanchesProdutoNaoEncontrado(erro_produto.message)
    except Exception as erro_interno:
        raise Exception(erro_interno)

    return jsonify(produto), 200
        
 
@app.route("/comercio/<comercio_nome>/destaques", methods=['POST'])
def adiciona_destaques(comercio_nome):
    req = request.get_json()
    assert req, "Erro: json inválido!"
    assert "destaques" in req, "Erro: destaques não informados!"
    
    destaques = req.get("destaques")

    try:
        controller.adiciona_destaques(destaques, comercio_nome)
        msg = {"message": f"destaques adicionados"}
    except SolanchesComercioNaoEncontrado as erro_comerico:
        raise SolanchesComercioNaoEncontrado(erro_comerico.message)
    except SolanchesProdutoNaoEstaNoCardapio as erro_produto:
        raise SolanchesProdutoNaoEncontrado(erro_produto.message)
    except Exception as erro_interno:
        raise Exception(erro_interno)

    return jsonify(msg), 201


@app.route("/comercio/<comercio_nome>/produto/<produto_id>", methods=['DELETE'])
def remove_produto(comercio_nome, produto_id):
    try:
        cardapio = controller.remove_produto(comercio_nome, produto_id)
    except SolanchesComercioNaoEncontrado as erro_comercio:
        raise SolanchesComercioNaoEncontrado(erro_comercio.message)
    except SolanchesProdutoNaoEstaNoCardapio as erro_produto:
        raise SolanchesProdutoNaoEncontrado(erro_produto.message)
    except Exception as erro_interno:
        raise Exception(erro_interno)

    return jsonify(cardapio), 200


@app.errorhandler(SolanchesDuplicateKey)
def handle_duplicate_key(error):
    error.status_code = 400
    return construct_error(error), error.status_code


@app.errorhandler(SolanchesComercioNaoEncontrado)
def handle_comercio_nao_encontrado(error):
    error.status_code = 404
    return construct_error(error), error.status_code


@app.errorhandler(SolanchesProdutoNaoEncontrado)
def handle_produto_nao_encontrado(error):
    error.status_code = 404
    return construct_error(error), error.status_code

@app.errorhandler(SolanchesProdutoNaoEstaNoCardapio)
def handle_produto_nao_esta_no_cardapio(error):
    error.status_code = 404
    return construct_error(error), error.status_code


@app.errorhandler(Exception)
def _error(error):
    data = {}
    data["error"]  = error.__class__.__name__
    data["message"] = str(error)
    data["status_code"] = 500
    return data, data["status_code"]


def construct_error(error):
    data ={}
    data["error"] = error.__class__.__name__
    data["message"] = error.message
    data["status_code"] = error.status_code
    return data