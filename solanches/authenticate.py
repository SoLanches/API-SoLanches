from functools import wraps
import jwt

from flask import current_app
from flask import request

from solanches.errors import *
from . import controller
from .models import BlockList


def _assert(condition, message, SolanchesError=SolanchesBadRequestError):
    if condition:
        return
    raise SolanchesError(message)


def jwt_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        token = None

        if 'authorization' in request.headers:
            token = request.headers['authorization']

        token_in_block_list = BlockList.contains(token)

        _assert(token and not token_in_block_list, "Error: Você não tem permissão para acessar essa rota.", SolanchesNotAuthorizedError)

        try:
            decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = controller.get_comercio_by_id(decoded.get("id"))
        except:
            _assert(False, "Error: Token inválido ou expirado.")

        return function(current_user=current_user, *args, **kwargs)

    return wrapper
