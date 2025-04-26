from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config

from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps

import os

from models import db, Cliente, Restaurante, Usuario

def create_app(environment):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(environment)
    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app


environment = config['development']
app = create_app(environment)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Usuario.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator

@app.route('/registrar', methods=['GET', 'POST'])
def signup_user():  
    data = request.get_json()  

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    
    new_user = Usuario(public_id=str(uuid.uuid4()), nombre=data['nombre'], password=hashed_password, admin=False) 
    db.session.add(new_user)  
    db.session.commit()    

    return jsonify({'message': 'registered successfully'})

@app.route('/login', methods=['GET', 'POST'])  
def login_user(): 
    print("HOLA")
    auth = request.authorization
    print(auth)   

    if not auth or not auth.username or not auth.password:  
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

    user = Usuario.query.filter_by(nombre=auth.username).first()
    
        
    if check_password_hash(user.password, auth.password):  
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
        return jsonify({'token' : token}) 

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/clientes', methods=['GET'])
@token_required
def clientes():
    if request.method == 'GET':
        clientes = [ cliente.json() for cliente in Cliente.query.all() ] 
    return jsonify({'Clientes': clientes })

@app.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    cliente = Cliente.query.filter_by(ID_Cliente=id).first()
    if cliente is None:
        return jsonify({'Error': "El cliente no se encuentra en la base de datos" }), 404
    return jsonify({'cliente': cliente.json() }), 200

@app.route('/clientes', methods=['POST'])
def crear_cliente():
    data = request.get_json()
    print(data)
    
    cliente = Cliente.create(data.get('nombre'), data.get('telefono'), data.get('email'), data.get('direccion'))
    if cliente is None:
        return jsonify({'Error': "El correo usado ya se encuentra en la base de datos" }), 400
    return jsonify({'Cliente creado': cliente.json() }), 201

@app.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = Cliente.query.filter_by(ID_Cliente=id).first()
    if cliente is None:
        return jsonify({'Error': "El cliente no se encuentra en la base de datos" }), 404
    cliente.delete(id)
    return jsonify({'message': "Cliente eliminado correctamente" }), 200

@app.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    cliente = Cliente.query.filter_by(ID_Cliente=id).first()
    if cliente is None:
        return jsonify({'Error': "El cliente no se encuentra en la base de datos" }), 404
    data = request.get_json()
    cliente = cliente.update(id, data.get('nombre'),data.get('telefono'), data.get('email'), data.get('direccion'))
    return jsonify({'message': "Cliente actualizado correctament" }), 200

@app.route('/restaurantes', methods=['GET'])
def restaurantes():
    if request.method == 'GET':
        restaurantes = [ restaurante.json() for restaurante in Restaurante.query.all() ] 
    return jsonify({'restaurantes': restaurantes })

@app.route('/restaurantes/<int:id>', methods=['GET'])
def get_restaurante(id):
    restaurante = Restaurante.query.filter_by(ID_Restaurante=id).first()
    if restaurante is None:
        return jsonify({'Error': "El restaurante no se encuentra en la base de datos" }), 404
    return jsonify({'restaurante': restaurante.json() }), 200

@app.route('/restaurantes', methods=['POST'])
def crear_restaurante():
    data = request.get_json()
    
    restaurante = Restaurante.create(data.get('nombre'), data.get('ubicacion'), data.get('telefono'), data.get('horario'))
    if restaurante is None:
        return jsonify({'Error': "Eror al crear el restaurante" }), 400
    return jsonify({'restaurante creado': restaurante.json() }), 201

@app.route('/restaurantes/<int:id>', methods=['DELETE'])
def delete_restaurante(id):
    restaurante = Restaurante.query.filter_by(ID_Restaurante=id).first()
    if restaurante is None:
        return jsonify({'Error': "El restaurante no se encuentra en la base de datos" }), 404
    restaurante.delete(id)
    return jsonify({'message': "restaurante eliminado correctamente" }), 200

@app.route('/restaurantes/<int:id>', methods=['PUT'])
def update_restaurante(id):
    restaurante = Restaurante.query.filter_by(ID_Restaurante=id).first()
    if restaurante is None:
        return jsonify({'Error': "El restaurante no se encuentra en la base de datos" }), 404
    data = request.get_json()
    restaurante = restaurante.update(id, data.get('nombre'),data.get('ubicacion'), data.get('telefono'), data.get('horario'))
    return jsonify({'message': "restaurante actualizado correctament" }), 200


if __name__ == '__main__':
    app.run(debug=True)