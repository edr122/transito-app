from flask import Blueprint, Flask, jsonify, json, request, render_template, redirect ,url_for,flash, Response
from db import mysql

vehiculo = Blueprint('vehiculo', __name__, template_folder='templates')

# CONSTANTE
RESPONSE_OK = {'status': 'OK'}
RESPONSE_ERROR = {'status': 'ERROR', 'message' :''}


#SERVICIOS DE VEHICULO

@vehiculo.route('/vehiculo_view')
def Vehiculo():
    return render_template('vehiculo.html')

@vehiculo.route('/vehiculo/<string:id>', methods=['GET'])
def get_vehiculo(id):
    cur =mysql.connection.cursor()
    cur.execute("SELECT * FROM vehiculo WHERE id = {0}".format(id))
    row_headers=[x[0] for x in cur.description]
    data = cur.fetchall()
    json_data={}
    for result in data:
        json_data = dict(zip(row_headers,result))
    return jsonify(json_data)

@vehiculo.route('/vehiculos', methods=['GET'])
def get_all_vehiculo():
    cur =mysql.connection.cursor()
    cur.execute("""select ve.id, ve.placa_patente, ve.marca, ve.color, pe.nombre as persona
                    from vehiculo ve
                    inner join persona pe on ve.id_persona = pe.id order by ve.id asc""")
    row_headers=[x[0] for x in cur.description]
    data = cur.fetchall()
    json_data=[]
    for result in data:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)


@vehiculo.route('/vehiculo', methods=['POST'])
def add_vehiculo():
    placa_patente = request.form['placa_patente']
    marca = request.form['marca']
    color = request.form['color']
    id_persona = request.form['id_persona']
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO vehiculo (placa_patente, marca, color, id_persona) VALUES(%s,%s, %s,%s)", (placa_patente, marca,color, id_persona))
        mysql.connection.commit()
        return jsonify(RESPONSE_OK)
    except Exception as e:
        return jsonify({'status': 'ERROR', 'message' :e.args[1]}), 400


@vehiculo.route('/vehiculo', methods=['PUT'])
def edit_vehiculo():
    id = request.form['id']
    placa_patente = request.form['placa_patente']
    marca = request.form['marca']
    color = request.form['color']
    id_persona = request.form['id_persona']
    try:
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE vehiculo
                SET placa_patente = %s,
                    marca = %s,
                    color = %s,
                    id_persona = %s
                WHERE id = %s""",
                    (placa_patente, marca,color, id_persona, id))
        mysql.connection.commit()
        return jsonify(RESPONSE_OK)
    except Exception as e:
        return jsonify({'status': 'ERROR', 'message' :e.args[1]}), 400
    

@vehiculo.route('/vehiculo/<string:id>', methods=['DELETE'])
def delete_vehiculo(id):
    cur =mysql.connection.cursor()
    try:
        cur.execute('DELETE FROM vehiculo WHERE id = {0}'.format(id))
        mysql.connection.commit()
        return jsonify(RESPONSE_OK)
    except Exception as e:
        return jsonify({'status': 'ERROR', 'message' :e.args[1]}), 400