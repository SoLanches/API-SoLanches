import time

from flask import Flask
from flask import jsonify
from flask import request

from . import controller
from .authenticate import jwt_required
from .authenticate import revoke_token
from . errors import SolanchesBadRequestError
from . errors import SolanchesNotFoundError
from . errors import SolanchesInternalServerError
from . errors import SolanchesNotAuthorizedError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
started_at = time.time()


def _assert(condition, message, SolanchesError=SolanchesBadRequestError):
    if condition: return
    raise SolanchesError(message)


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
    _assert(req, "Erro: json inválido!")
    _assert("nome" in req, "Erro: campo nome não informado!")
    _assert("password" in req, "Erro: campo senha não informado!")
    _assert("attributes" in req, "Erro: campo attributes não informado!")

    nome = req.get("nome")
    password = req.get("password")
    attributes = req.get("attributes")

    novo_comercio = controller.cadastra_comercio(nome, password, attributes)
    return jsonify(novo_comercio), 201


@app.route("/comercios", methods=['GET'])
def get_comercios():
    categories = request.args.get("categories", "")
    has_categories = categories.lower() == "true"
    try:
        comercios = controller.get_comercios(has_categories)
    except Exception as erro_interno:
        raise Exception(erro_interno)

    return jsonify(comercios), 200


@app.route("/comercio", methods=['GET'])
def get_comercio_by_id():
    comercio_id = request.args.get('id')
    _assert(comercio_id, "Erro: id do comercio não informado!")
    comercio = controller.get_comercio_by_id(comercio_id)
    return jsonify(comercio), 200


@app.route("/comercio/<comercio_nome>", methods=['GET'])
def get_comercio_by_name(comercio_nome):
    comercio = controller.get_comercio_by_name(comercio_nome)
    return jsonify(comercio), 200


@app.route("/comercio/<comercio_nome>", methods=['PATCH'])
@jwt_required
def edita_comercio(comercio_nome):
    req = request.get_json()  
    _assert(req, "Erro: json inválido!")
    _assert("attributes" in req, "Erro: campo attributes inválido")
    attributes = req.get("attributes")

    comercio_atualizado = controller.atualiza_comercio(attributes, comercio_nome)
    return jsonify(comercio_atualizado), 200


@app.route("/comercio/<comercio_nome>", methods=['DELETE'])
@jwt_required
def remove_comercio(comercio_nome):
    controller.remove_comercio(comercio_nome)
    msg = {"message": f"comercio {comercio_nome} removido com sucesso"}
    return jsonify(msg), 200


@app.route("/comercio/<comercio_nome>/cardapio", methods=['GET'])
def get_cardapio(comercio_nome):
    cardapio = controller.get_cardapio(comercio_nome)
    return jsonify(cardapio), 200


@app.route("/comercio/<comercio_nome>/produto", methods=['POST'])
@jwt_required
def cadastra_produto(comercio_nome):
    req = request.get_json()
    _assert(req, "Erro: json inválido!")
    nome_produto = req.get("nome")
    _assert(nome_produto, "Erro: nome não informado!")
    attributes = req.get("attributes") if "attributes" in req else {}

    novo_produto = controller.cadastra_produto(comercio_nome, nome_produto, attributes)
    return jsonify(novo_produto), 201


@app.route("/comercio/<comercio_nome>/produto/<produto_id>", methods=['GET'])
def get_produto(comercio_nome, produto_id):
    produto = controller.get_produto(comercio_nome, produto_id)
    return jsonify(produto), 200


@app.route("/comercio/<comercio_nome>/produtos", methods=['GET'])
def get_produtos(comercio_nome):
    categories = request.args.get("categories", "")
    has_categories = categories.lower() == "true"
    produtos = controller.get_produtos(comercio_nome, has_categories)
    return jsonify(produtos), 200


@app.route("/comercio/<comercio_nome>/produtos/ids", methods=['GET'])
def get_produtos_ids(comercio_nome):
    produtos = controller.get_produtos_ids(comercio_nome)
    return jsonify(produtos), 200


@app.route("/comercio/<comercio_nome>/produto/<produto_id>", methods=['PATCH'])
@jwt_required
def edita_produto(comercio_nome, produto_id):
    req = request.get_json()
    _assert(req, "Erro: json inválido!")
    attributes = req.get("attributes") if "attributes" in req else {}
    nome = req.get("nome") if "nome" in req else ""
    produto = controller.edita_produto(produto_id, comercio_nome, attributes, nome)
    return jsonify(produto), 200


@app.route("/comercio/<comercio_nome>/produto/<produto_id>", methods=['DELETE'])
@jwt_required
def remove_produto(comercio_nome, produto_id):
    cardapio = controller.remove_produto(comercio_nome, produto_id)
    return jsonify(cardapio), 200


@app.route("/comercio/<comercio_nome>/destaques/<produto_id>", methods=['POST'])
@jwt_required
def adiciona_destaque(comercio_nome, produto_id):
    cardapio = controller.adiciona_destaque(comercio_nome, produto_id)
    return jsonify(cardapio), 201


@app.route("/comercio/<comercio_nome>/destaques/<produto_id>", methods=['DELETE'])
@jwt_required
def remove_produto_destaques(comercio_nome, produto_id):
    cardapio = controller.remove_produto_destaques(comercio_nome, produto_id)
    return jsonify(cardapio), 200


@app.route("/comercio/<comercio_nome>/categoria", methods=['POST'])
@jwt_required
def adiciona_categoria(comercio_nome):
    req = request.get_json()
    _assert(req, "Erro: json inválido!")
    categoria = req.get("categoria")
    _assert(categoria, "Erro: categoria não informada!")

    cardapio_atualizado = controller.adiciona_categoria(comercio_nome, categoria)
    return jsonify(cardapio_atualizado), 201


@app.route("/comercio/<comercio_nome>/categoria", methods=['DELETE'])
@jwt_required
def remove_categoria(comercio_nome):
    req = request.get_json()
    _assert(req, "Erro: json inválido!")
    categoria = req.get("categoria")
    _assert(categoria, "Erro: categoria não informada!")
    
    cardapio_atualizado = controller.remove_categoria(comercio_nome, categoria)
    return jsonify(cardapio_atualizado), 200


@app.route("/login", methods=["POST"])
def login():
    req = request.get_json()
    _assert(req, "Erro: json inválido!")
    _assert("nome" in req, "Erro: nome não informado!")
    _assert("password" in req, "Erro: senha não informada")

    nome = req.get('nome')
    password = req.get('password')

    token = controller.login(nome, password, app.config['SECRET_KEY'])
    return jsonify({'token': token})


@app.route("/logout", methods=["DELETE"])
@revoke_token
def logout(revoke):
    token = None
    if 'authorization' in request.headers:
        token = request.headers['authorization']

    if revoke:
        controller.logout(token)

    response = {
        "message": "Logout feito com sucesso", 
        "status_code": 200
    }
    
    return jsonify(response), 200


def _construct_error(error):
    data ={}
    data["error"] = error.__class__.__name__
    data["message"] = error.message
    data["status_code"] = error.status_code
    return data


@app.errorhandler(Exception)
def _error(error):
    data = {}
    data["error"]  = error.__class__.__name__
    data["message"] = str(error)
    data["status_code"] = 500
    return data, data["status_code"]


@app.errorhandler(SolanchesBadRequestError)
def bad_request_error_handler(error):
    error.status_code = 400
    return _construct_error(error), error.status_code


@app.errorhandler(SolanchesNotAuthorizedError)
def not_authorized_error_handler(error):
    error.status_code = 401
    return _construct_error(error), error.status_code


@app.errorhandler(SolanchesNotFoundError)
def not_found_error_handler(error):
    error.status_code = 404
    return _construct_error(error), error.status_code


@app.errorhandler(SolanchesInternalServerError)
def internal_server_error_handler(error):
    error.status_code = 500
    return _construct_error(error), error.status_code
