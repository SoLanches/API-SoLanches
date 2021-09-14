from datetime import datetime
from functools import wraps

import jwt
from flask import jsonify
from flask import request
from flask import abort
from flask import current_app
from flask import make_response

from . import controller
from .models import BlockList


def _assert(condition, status_code, message):
    if condition: return
    data = {
        "message": message,
        "status_code": status_code
    }
    response = make_response(jsonify(data), status_code)
    abort(response)


def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        if 'authorization' in request.headers:
            token = request.headers['authorization']

        token_in_block_list = BlockList.contains(token)

        _assert(token != None and not token_in_block_list, 403, "Error: Você não tem permissão para acessar essa rota.")
        
        try:
            decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = controller.get_comercio(decoded.get("id"))
        except:
            _assert(False, 403, "Error: Token inválido ou expirado.")    
        
        return f(current_user=current_user, *args, **kwargs)

    return wrapper
