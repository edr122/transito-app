from jwt import encode, decode
from jwt import exceptions
from datetime import datetime, timedelta
from flask import jsonify,request
from functools import wraps
from werkzeug.datastructures import ImmutableMultiDict

def expire_date(days: int):
    now = datetime.now()
    new_date = now + timedelta(days)
    return new_date


def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(1)},
                   key="CHALLENGER_KEY_JWT", algorithm="HS256")
    return token.encode("UTF-8")


def validate_token(token, output=False):
    try:
        if output:
            return decode(token, key="CHALLENGER_KEY_JWT", algorithms=["HS256"])
        decode(token, key="CHALLENGER_KEY_JWT", algorithms=["HS256"])
    except exceptions.DecodeError:
        response = jsonify({"status":"ERROR", "message": "Token inválido"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"status":"ERROR", "message": "Token expirado"})
        response.status_code = 401
        return
    

def token_required():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                token = request.headers['Authorization']
            except:
                response = jsonify({"status":"ERROR", "message": "Token inválido"})
                response.status_code = 401
                return response
            
            token = token.split(" ")[1]

            try:
                data_token = decode(token, key="CHALLENGER_KEY_JWT", algorithms=["HS256"])
                http_args = request.args.to_dict()
                http_args ['usuario_app'] = data_token["usuario_app"]
                request.args = ImmutableMultiDict(http_args)
            except exceptions.DecodeError:
                response = jsonify({"status":"ERROR", "message": "Token inválido"})
                response.status_code = 401
                return response
            except exceptions.ExpiredSignatureError:
                response = jsonify({"status":"ERROR", "message": "Token expirado"})
                response.status_code = 401
                return response
            
            return f(*args, **kwargs)
        return decorated

    return decorator