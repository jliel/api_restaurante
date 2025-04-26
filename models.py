from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask import jsonify

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    nombre = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)
class Cliente(db.Model):
    __tablename__ = 'cliente'

    ID_Cliente = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(80))
    Ubicacion = db.Column(db.String(80))
    Telefono = db.Column(db.String(80))
    Horario_atencion = db.Column(db.String(80))

    @classmethod
    def create(cls, nombre, telefono, email, direccion):
        cliente = Cliente(Nombre=nombre, Telefono=telefono, Email=email, Direccion=direccion)
        exists = db.session.execute(db.select(Cliente).filter_by(Email=email))
        email = Cliente.query.filter_by(Email=email).first()
        if not email:
            return cliente.save()
        else:
            return None
    @classmethod
    def delete(cls, id):
        cliente = Cliente.query.filter_by(ID_Cliente=id).first()
        if cliente is None:
            return False
        db.session.delete(cliente)
        db.session.commit()
        return True
    
    def update(cls, id, nombre, telefono, email, direccion):
        cliente = Cliente.query.filter_by(ID_Cliente=id).first()
        cliente.Nombre = nombre
        cliente.Telefono = telefono
        cliente.Email = email
        cliente.Direccion = direccion
        cliente.save()
        db.session.add(cliente)
        db.session.commit()
        return cliente
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

            return self
        except:
            return False
    def json(self):
        return {
            'id': self.ID_Cliente,
            'nombre': self.Nombre,
            'telefono': self.Telefono,
            'email': self.Email,
            'direccion': self.Direccion
        }
    
class Restaurante(db.Model):
    __tablename__ = 'restaurante'

    ID_Restaurante = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(80))
    Ubicacion = db.Column(db.String(80))
    Telefono = db.Column(db.String(80))
    Horario_atencion = db.Column(db.String(80))

    @classmethod
    def create(cls, nombre, ubicacion, telefono, horario):
        restaurante = Restaurante(Nombre=nombre, Ubicacion=ubicacion, Telefono=telefono, Horario_atencion=horario)
        
        return restaurante.save()
    @classmethod
    def delete(cls, id):
        restaurante = Restaurante.query.filter_by(ID_Restaurante=id).first()
        if restaurante is None:
            return False
        db.session.delete(restaurante)
        db.session.commit()
        return True
    
    def update(cls, id, nombre, ubicacion, telefono, horario):
        restaurante = Restaurante.query.filter_by(ID_Restaurante=id).first()
        restaurante.Nombre = nombre
        restaurante.Telefono = telefono
        restaurante.Ubicacion = ubicacion
        restaurante.Horario_atencion = horario
        restaurante.save()
        db.session.add(restaurante)
        db.session.commit()
        return restaurante
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

            return self
        except:
            return False
    def json(self):
        return {
            'id': self.ID_Restaurante,
            'nombre': self.Nombre,
            'telefono': self.Telefono,
            'ubicacion': self.Ubicacion,
            'horario': self.Horario_atencion
        }