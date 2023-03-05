from flask import Blueprint, Flask, jsonify, json, request, render_template, redirect ,url_for,flash, Response
from db import mysql
from auth.config_jwt import token_required

infraccion = Blueprint('infraccion', __name__)


@infraccion.route('/cargar_infraccion', methods=['POST'])
@token_required()
def cargar_infraccion():
    try:
        usuario_app = request.args.get('usuario_app')
        data_body = request.get_json()
        placa_patente = data_body["placa_patente"]
        cur = mysql.connection.cursor()
        # Validar vehiculo
        cur.execute('SELECT * FROM vehiculo WHERE placa_patente = %s',[placa_patente])
        array_vehiculos = cur.fetchall()
        if len(array_vehiculos) <=0:
            return jsonify({"status":"ERROR","message":"Placa patente no encontrado"}), 404
        else:
            for row in array_vehiculos:
                id_vehiculo = row[0]
        # Validar oficial
        cur.execute('SELECT * FROM oficial WHERE usuario_app = %s',[usuario_app])
        array_oficiales = cur.fetchall()
        if len(array_oficiales) <=0:
            return jsonify({"status":"ERROR","message":"Oficial no encontrado"}), 404
        else:
            for row in array_oficiales:
                id_oficial = row[0]
        # Agregar infracción
        cur.execute("""INSERT INTO infraccion (comentarios, fecha_creacion, id_oficial, id_vehiculo) VALUES(%s,%s,%s,%s)""",
                    (data_body["comentarios"], data_body["timestamp"], id_oficial,id_vehiculo))
        mysql.connection.commit()
        return jsonify({"status":"OK","message":""})
    except Exception as e:
        return jsonify({'status': 'ERROR', 'message' :"Ha ocurrido un error en el proceso"}), 500



@infraccion.route('/generar_informe/<string:correo>', methods=['GET'])
def generar_informe_infraccion(correo):
    cur = mysql.connection.cursor()
    cur.execute("""
            SELECT inf.id, inf.comentarios, inf.fecha_creacion, ofi.nombre as oficial, ve.placa_patente as placa_vehiculo 
            FROM infraccion inf
            inner join oficial ofi on inf.id_oficial = ofi.id
            inner join vehiculo ve on inf.id_vehiculo = ve.id
            inner join persona pe on ve.id_persona = pe.id
            where pe.correo = %s;
    """, [correo])
    row_headers=[x[0] for x in cur.description]
    data = cur.fetchall()
    json_data=[]
    for result in data:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)