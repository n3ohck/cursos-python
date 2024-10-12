import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from urllib.parse import quote_plus
from bson import ObjectId


load_dotenv()

app = Flask(__name__)

username = quote_plus(os.getenv('mongouser'))
password = quote_plus(os.getenv('mongopassword'))
cluster_url = os.getenv('mongocluster_url')
db_name = os.getenv('mongodb_name')

# Configuración de la conexión a MongoDB
connection_string = f'mongodb+srv://{username}:{password}@{cluster_url}/{db_name}?retryWrites=true&w=majority'
client = MongoClient(connection_string)
db = client[db_name]

contactos_collection = db['contactos']

def serialize_contacto(contacto):
    """Función para serializar el contacto"""
    contacto['_id'] = str(contacto['_id'])  # Convertir ObjectId a string
    return contacto

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['GET'])
def buscar_contacto():
    query = request.args.get('query', '')
    resultados = list(contactos_collection.find({"nombre": {"$regex": query, "$options": "i"}}))
    resultados_serializados = [serialize_contacto(contacto) for contacto in resultados]
    return jsonify(resultados_serializados)

@app.route('/agregar', methods=['POST'])
def agregar_contacto():
    nombre = request.form.get('nombre')
    telefono = request.form.get('telefono')

    if contactos_collection.find_one({"nombre": nombre}):
        return jsonify({"mensaje": "El contacto ya existe."}), 400

    nuevo_contacto = {
        "nombre": nombre,
        "telefono": telefono
    }
    contactos_collection.insert_one(nuevo_contacto)
    return jsonify({"mensaje": "Contacto agregado con éxito!"}), 201

@app.route('/editar/<contacto_id>', methods=['POST'])
def editar_contacto(contacto_id):
    nombre = request.form.get('nombre')
    telefono = request.form.get('telefono')

    contacto_existente = contactos_collection.find_one({"_id": ObjectId(contacto_id)})
    if not contacto_existente:
        return jsonify({"mensaje": "Contacto no encontrado."}), 404

    # Actualizar el contacto
    contactos_collection.update_one(
        {"_id": ObjectId(contacto_id)},
        {"$set": {"nombre": nombre, "telefono": telefono}}
    )

    return jsonify({"mensaje": "Contacto actualizado con éxito!"}), 200


@app.route('/eliminar/<contacto_id>', methods=['DELETE'])
def eliminar_contacto(contacto_id):
    try:
        contacto_existente = contactos_collection.find_one({"_id": ObjectId(contacto_id)})
        
        if not contacto_existente:
            return jsonify({"mensaje": "Contacto no encontrado."}), 404

        # Eliminar el contacto
        contactos_collection.delete_one({"_id": ObjectId(contacto_id)})
        return jsonify({"mensaje": "Contacto eliminado con éxito!"}), 200
    except Exception as e:
        return jsonify({"mensaje": f"Error al eliminar el contacto: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG'))
