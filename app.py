from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from urllib.parse import quote_plus
from bson import ObjectId


app = Flask(__name__)

# Reemplaza 'miUsuario' y 'miContraseña' con tus credenciales
username = quote_plus('n3ohck')  # Escapar el nombre de usuario
password = quote_plus('Kvm82645699@@')  # Escapar la contraseña
cluster_url = 'n3ohck.2bnezap.mongodb.net'
db_name = 'agenda'

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
        return jsonify({"mensaje": "El contacto ya existe."}), 400  # Código de error 400 para solicitud incorrecta

    nuevo_contacto = {
        "nombre": nombre,
        "telefono": telefono
    }
    contactos_collection.insert_one(nuevo_contacto)
    return jsonify({"mensaje": "Contacto agregado con éxito!"}), 201

if __name__ == '__main__':
    app.run(debug=True)
