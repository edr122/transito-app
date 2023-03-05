from re import split
from flask import Blueprint, request, jsonify
from auth.config_jwt import write_token, validate_token
from db import mysql


routes_auth = Blueprint("routes_auth", __name__)


@routes_auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    cur =mysql.connection.cursor()
    cur.execute("SELECT * FROM oficial WHERE usuario_app = %s",[data['usuario_app']])
    datafetch = cur.fetchall()
    if len(datafetch) > 0:
        return write_token(data=request.get_json())
    else:
        response = jsonify({"status":"ERROR","message": "Usuario no encontrado"})
        response.status_code = 404
        return response

@routes_auth.route("/verificar/token")
def verify():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=True)