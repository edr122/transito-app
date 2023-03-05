
from flask import Blueprint, Flask, jsonify, json, request, render_template, redirect ,url_for,flash, Response
from db import mysql

index = Blueprint('index', __name__, template_folder='templates')

# CONSTANTE
RESPONSE_OK = {'status': 'OK'}
RESPONSE_ERROR = {'status': 'ERROR', 'message' :''}

@index.route('/')
def Index():
    return render_template('index.html')

@index.route('/infracciones', methods=['GET'])
def get_infracciones():
    cur =mysql.connection.cursor()
    cur.execute("""
            SELECT inf.id, inf.comentarios, inf.fecha_creacion, ofi.nombre as oficial, ve.placa_patente as placa_vehiculo 
            FROM infraccion inf
            inner join oficial ofi on inf.id_oficial = ofi.id
            inner join vehiculo ve on inf.id_vehiculo = ve.id
    """)
    row_headers=[x[0] for x in cur.description]
    data = cur.fetchall()
    json_data=[]
    for result in data:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)