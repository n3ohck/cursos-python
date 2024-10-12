from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Lista de contactos (puedes reemplazar esto por una base de datos más adelante)
contactos = [
    {"nombre": "Juan Pérez", "telefono": "123456789"},
    {"nombre": "María García", "telefono": "987654321"},
    {"nombre": "Ana López", "telefono": "456123789"},
    {"nombre": "Kaleb Kirabelak", "telefono": "456123789"},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['GET'])
def buscar_contacto():
    query = request.args.get('query', '')
    resultados = [contacto for contacto in contactos if query.lower() in contacto['nombre'].lower()]
    return jsonify(resultados)

@app.route('/agregar', methods=['POST'])
def agregar_contacto():
    nuevo_contacto = {
        "nombre": request.form.get('nombre'),
        "telefono": request.form.get('telefono')
    }
    contactos.append(nuevo_contacto)
    return jsonify({"mensaje": "Contacto agregado con éxito!"}), 201

if __name__ == '__main__':
    app.run(debug=True)
