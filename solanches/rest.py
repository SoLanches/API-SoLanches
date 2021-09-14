import time
import datetime

from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from flask import abort
import jwt

from . import controller
from .authenticate import jwt_required
from .models import BlockList

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
started_at = time.time()


def _assert(condition, status_code, message):
    if condition: return
    data = {
        "message": message,
        "status_code": status_code
    }
    response = make_response(jsonify(data), status_code)
    abort(response)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH')
    return response


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
    categories = request.args.get("categories", "")
    has_categories = categories.lower() == "true"
    try:
        comercios = controller.get_comercios(has_categories)
    except Exception as error:
        _assert(False, 400, str(error))
    return jsonify(comercios), 200 


@app.route("/comercio", methods=['GET'])
def get_comercio_by_id():
    comercio_id = request.args.get('id')
    _assert(comercio_id, 400, "Erro: id do comercio não informado!")
    try:
        comercio = controller.get_comercio_by_id(comercio_id)
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


@app.route("/comercio/<comercio_nome>", methods=['PATCH'])
#@jwt_required
def edita_comercio(comercio_nome):
    req = request.get_json()  
    _assert(req, 400, "Erro: json inválido!")

    attributes = req.get("attributes", {})
    _assert(type(attributes) is dict, 400, "Erro: campo attributes deve ser do tipo dict")

    try:
        comercio_atualizado = controller.atualiza_comercio(attributes, comercio_nome)
    except Exception as error:
        _assert(False, 400, str(error))

    return jsonify(comercio_atualizado), 200


@app.route("/comercio/<comercio_nome>", methods=['DELETE'])
def remove_comercio(comercio_nome):
    try:
        result = controller.remove_comercio(comercio_nome)
        msg = {"message": f"comercio {comercio_nome} removido com sucesso"} if result else {"erro": "não foi possível remover o comércio"}
    except Exception as error:
        _assert(False, 400, str(error))

    return jsonify(msg), 200


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


@app.route("/comercio/<comercio_nome>/produto/<produto_id>", methods=['GET'])
def get_produto(comercio_nome, produto_id):
    try:
        produto = controller.get_produto(comercio_nome, produto_id)
    except Exception as error:
        _assert(False, 400, str(error))

    return jsonify(produto), 200


@app.route("/comercio/<comercio_nome>/produtos", methods=['GET'])
def get_produtos(comercio_nome):
    categories = request.args.get("categories", "")
    has_categories = categories.lower() == "true"
    try:
        produtos = controller.get_produtos(comercio_nome, has_categories)
    except Exception as error:
        _assert(False, 400, str(error))

    return jsonify(produtos), 200


@app.route("/comercio/<comercio_nome>/produtos/ids", methods=['GET'])
def get_produtos_ids(comercio_nome):
    try:
        produtos = controller.get_produtos_ids(comercio_nome)
    except Exception as error:
        _assert(False, 400, str(error))

    return jsonify(produtos), 200


@app.route("/comercio/<comercio_nome>/produto/<produto_id>", methods=['PATCH'])
def edita_produto(comercio_nome, produto_id):
    req = request.get_json()
    _assert(req, 400, "Erro: json inválido!")
    attributes = req.get("attributes") if "attributes" in req else {}
    nome = req.get("nome") if "nome" in req else ""
    try:
        produto = controller.edita_produto(produto_id, comercio_nome, attributes, nome)
    except Exception as error:
        _assert(False, 400, str(error))
    return jsonify(produto), 200


@app.route("/comercio/<comercio_nome>/destaques/<produto_id>", methods=['POST'])
def adiciona_destaque(comercio_nome, produto_id):
    try:
        cardapio = controller.adiciona_destaque(comercio_nome, produto_id)
    except Exception as error:
        _assert(False, 400, str(error))

    return jsonify(cardapio), 201


@app.route("/comercio/<comercio_nome>/produto/<produto_id>", methods=['DELETE'])
def remove_produto(comercio_nome, produto_id):
    try:
        cardapio = controller.remove_produto(comercio_nome, produto_id)
    except Exception as error:
        _assert(False, 400, str(error))
    return jsonify(cardapio), 200


@app.route("/comercio/<comercio_nome>/destaques/<produto_id>", methods=['DELETE'])
def remove_produto_destaques(comercio_nome, produto_id):
    try:
        cardapio = controller.remove_produto_destaques(comercio_nome, produto_id)
    except Exception as error:
        _assert(False, 400, str(error))

    return jsonify(cardapio), 200
    

@app.errorhandler(Exception)
def _error(error):
    data = {}
    data["error"]  = error.__class__.__name__
    data["message"] = str(error)
    client_errors = ["BadRequest"]
    data["status_code"] = 400 if data["error"] in client_errors else 500
    return data, data["status_code"]


@app.route("/login", methods=["POST"])
def login():
    req = request.get_json()
    _assert(req, 400, "Erro: json inválido!")
    _assert("nome" in req, 400, "Erro: nome não informado!")
    _assert("password" in req, 400, "Erro: senha não informada")

    nome = req.get('nome')
    password = req.get('password')

    try:
        comercio = controller.get_by_credentials(nome, password)
    except Exception as error:
        _assert(False, 403, str(error))

    payload = {
        'id': comercio.get("_id"),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token})


@app.route("/logout", methods=["DELETE"])
@jwt_required
def logout(current_user):
    token = None

    if 'authorization' in request.headers:
        token = request.headers['authorization']

    _assert(token, 403, "Error: Você não está logado.")

    block_token = BlockList(token)
    block_token.save()

    return jsonify({"msg": "Access token revoked"}), 200
