from functools import wraps

import jwt
from flask import request
from flask import current_app

from . import controller
from .models import BlockList
from solanches.errors import SolanchesBadRequestError, SolanchesNotAuthorizedError


def _assert(condition, message, SolanchesError=SolanchesBadRequestError):
    if condition: return
    raise SolanchesError(message)


def jwt_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        token = None

        if 'authorization' in request.headers:
            token = request.headers['authorization']

        token_in_block_list = BlockList.contains(token)

        _assert(token and not token_in_block_list, "Error: Você não tem permissão para acessar essa rota.", SolanchesNotAuthorizedError)
        _assert("comercio_nome" in kwargs, "Error: Nome do comércio não informado!")
        comercio_nome = kwargs.get("comercio_nome")

        try:
            decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = controller.get_comercio_by_id(decoded.get("id")).get("nome")
        except:
            _assert(False, "Error: Token inválido ou expirado.", SolanchesNotAuthorizedError)    

        _assert(current_user == comercio_nome, "Error: Token não referente a esse usuário.", SolanchesNotAuthorizedError)
        
        return function(*args, **kwargs)

    return wrapper
