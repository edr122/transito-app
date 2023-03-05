from flask import Blueprint, Flask, jsonify, json, request, render_template, redirect ,url_for,flash, Response
from db import mysql

oficial = Blueprint('oficial', __name__, template_folder='templates')

# CONSTANTE
RESPONSE_OK = {'status': 'OK'}
RESPONSE_ERROR = {'status': 'ERROR', 'message' :''}

#SERVICIOS DE OFICIAL

@oficial.route('/oficial_view')
def Oficial():
    return render_template('oficial.html')

@oficial.route('/oficial', methods=['POST'])
def add_oficial():
    nombre = request.form['nombre']
    usuario_app = request.form['usuario_app']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO oficial (nombre, usuario_app) VALUES(%s,%s)", (nombre, usuario_app))
    mysql.connection.commit()
    return jsonify(RESPONSE_OK)


@oficial.route('/oficial', methods=['PUT'])
def edit_oficial():
    id = request.form['id']
    nombre = request.form['nombre']
    usuario_app = request.form['usuario_app']
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE oficial
            SET nombre = %s,
                usuario_app = %s
            WHERE id = %s"""
                , (nombre, usuario_app, id))
    mysql.connection.commit()
    return jsonify(RESPONSE_OK)

@oficial.route('/oficial/<string:id>', methods=['GET'])
def get_oficial(id):
    cur =mysql.connection.cursor()
    cur.execute("SELECT * FROM oficial WHERE id = {0}".format(id))
    row_headers=[x[0] for x in cur.description]
    data = cur.fetchall()
    json_data={}
    for result in data:
        json_data = dict(zip(row_headers,result))
    return jsonify(json_data)

@oficial.route('/oficiales', methods=['GET'])
def get_all_oficial():
    cur =mysql.connection.cursor()
    cur.execute("SELECT * FROM oficial order by id asc")
    row_headers=[x[0] for x in cur.description]
    data = cur.fetchall()
    json_data=[]
    for result in data:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)
    
@oficial.route('/oficial/<string:id>', methods=['DELETE'])
def delete_oficial(id):
    cur =mysql.connection.cursor()
    try:
        cur.execute('DELETE FROM oficial WHERE id = {0}'.format(id))
        mysql.connection.commit()
        return jsonify(RESPONSE_OK)
    except Exception as e:
        return jsonify({'status': 'ERROR', 'message' :e.args[1]}), 400