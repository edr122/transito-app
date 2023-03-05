from flask import Blueprint, Flask, jsonify, json, request, render_template, redirect ,url_for,flash, Response
from db import mysql

persona = Blueprint('persona', __name__, template_folder='templates')

# CONSTANTE
RESPONSE_OK = {'status': 'OK'}
RESPONSE_ERROR = {'status': 'ERROR', 'message' :''}


#SERVICIOS DE PERSONA

@persona.route('/persona_view')
def Persona():
    return render_template('persona.html')

@persona.route('/persona', methods=['POST'])
def add_persona():
    nombre = request.form['nombre']
    correo = request.form['correo']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO persona (nombre, correo) VALUES(%s,%s)", (nombre, correo))
    mysql.connection.commit()
    return jsonify(RESPONSE_OK)


@persona.route('/persona', methods=['PUT'])
def edit_persona():
    id = request.form['id']
    nombre = request.form['nombre']
    correo = request.form['correo']
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE persona
            SET nombre = %s,
                correo = %s
            WHERE id = %s"""
                , (nombre, correo, id))
    mysql.connection.commit()
    return jsonify(RESPONSE_OK)

@persona.route('/persona/<string:id>', methods=['GET'])
def get_persona(id):
    cur =mysql.connection.cursor()
    cur.execute("SELECT * FROM persona WHERE id = {0}".format(id))
    row_headers=[x[0] for x in cur.description]
    data = cur.fetchall()
    json_data={}
    for result in data:
        json_data = dict(zip(row_headers,result))
    return jsonify(json_data)

@persona.route('/personas', methods=['GET'])
def get_all_persona():
    cur =mysql.connection.cursor()
    cur.execute("SELECT * FROM persona order by id asc")
    row_headers=[x[0] for x in cur.description]
    data = cur.fetchall()
    json_data=[]
    for result in data:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)
    
@persona.route('/persona/<string:id>', methods=['DELETE'])
def delete_persona(id):
    cur =mysql.connection.cursor()
    try:
        cur.execute('DELETE FROM persona WHERE id = {0}'.format(id))
        mysql.connection.commit()
        return jsonify(RESPONSE_OK)
    except Exception as e:
        return jsonify({'status': 'ERROR', 'message' :e.args[1]}), 400