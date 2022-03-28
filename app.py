
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config
from datetime import datetime



app = Flask(__name__)

conexion = MySQL(app)

@app.route('/ingresarpersona', methods=['POST'])
def ingresar_persona():
    cursor = conexion.connection.cursor()
    sql = """INSERT INTO persona (rut, nombre, apellido) 
    VALUES ('{0}', '{1}', '{2}')""".format(request.json['rut'], request.json['nombre'], request.json['apellido'])
    cursor.execute(sql)
    conexion.connection.commit()  
    return jsonify({'mensaje': "Persona Ingresada.", 'exito': True})

@app.route('/ingresarvehiculo', methods=['POST'])
def ingresar_vehiculo():
    cursor = conexion.connection.cursor()
    sql = """INSERT INTO vehiculo (marca, modelo, patente, annio, persona_id) 
    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', (SELECT persona_id WHERE rut = '{5}'))""".format(request.json['marca'], request.json['modelo'], request.json['patente'], request.json['annio'], request.json['rut'],)
    cursor.execute(sql)
    conexion.connection.commit()  
    return jsonify({'mensaje': "Vehiculo ingresado.", 'exito': True})

@app.route('/inspeccion/<tipo_revision>', methods=['POST'])
def ingresar_inspeccion(tipo_revision):
    cursor = conexion.connection.cursor()
    sql = """INSERT INTO inspeccion (tipo_inspeccion, observaciones, estado, revision_id, persona_id) 
    VALUES ('{0}', '{1}', '{2}', '{3}', (SELECT tipo_revision_id FROM tipo_revision WHERE nombre_tipo_revision = '{4}'), (SELECT persona_id WHERE rut = '{5}'))""".format(request.json['tipo_inspeccion'], request.json['observaciones'], request.json['estado'], request.json['tipo_revision'], request.json['rut'])
    cursor.execute(sql)
    conexion.connection.commit()
    return jsonify({'mensaje': "Vehiculo inspeccionado.", 'exito': True})

@app.route('/revision', methods=['POST'])
def revision():
    cursor = conexion.connection.cursor()
    fecha_actual = datetime.today().strftime('%Y-%m-%d %H:%M')
    sql ="""INSERT INTO revision (aprobado, observaciones, fecha_revision, vehiculo_id, persona_id)  
    VALUES ('{0}', '{1}', '{2}', (SELECT vehiculo_id FROM vehiculo WHERE patente = '{3}'), (SELECT persona_id WHERE rut = '{4}'))""".format(request.json['aprobado'], request.json['observaciones'], fecha_actual, request.json['patente'], request.json['rut'])
    cursor.execute(sql)
    conexion.connection.commit()
    aprobado = request.json['aprobado']
    if aprobado == True:
        return jsonify({'mensaje': "Revisión aprobada.", 'exito': True})
    else:
        return jsonify({'mensaje': "Revisión rechazada. Reparación externa necesaria", 'exito': True})

@app.route('/borrarinspeccion/<inspeccion_id>', methods=['POST'])
def borrar_inspeccion(inspeccion_id):
    cursor = conexion.connection.cursor()
    sql = """DELETE FROM inspeccion WHERE inspeccion_id = '{0}'""".format(request.json['inspeccion_id'])
    cursor.execute(sql)
    conexion.connection.commit()
    return jsonify({'mensaje': "Inspeccion eliminada", 'exito': True})

@app.route('/obtenerhistorial/<patente>', methods=['GET'])
def historial_revision  (patente):
    cursor = conexion.connection.cursor()
    sql = """SELECT fecha_revision, persona_id, observaciones, aprobado FROM revision r
    JOIN persona p ON r.persona_id = p.persona_id JOIN vehiculo v ON v.vehiculo_id = r.vehiculo_id
    WHERE v.patente ='{0}' ORDER BY fecha_revision ASC""".format(request.json['patente'])
    cursor.execute(sql)
    result = cursor.fetchall()
    datos = []
    for fila in result:
        dato = {'fecha_revision': fila[0], 'persona_id': fila[1], 'observaciones': fila[2], 'aprobado': fila[3]}
        datos.append(dato)
    return jsonify({'cursos': datos, 'mensaje': "Historial listado.", 'exito': True})



def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
