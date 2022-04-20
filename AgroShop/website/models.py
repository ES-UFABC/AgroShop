from sqlalchemy import ForeignKey
from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#Tabelas

class Cliente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique = True)#maximo 150 caracteres, email repetido nao vale(unique)
    senha = db.Column(db.String(150))
    nome = db.Column(db.String(150))
   
class Produtor(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique = True)
    senha = db.Column(db.String(150))
    nome = db.Column(db.String(150))

class Produto(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    idProd = db.Column(db.Integer)
    tipo = db.Column(db.String(25))
    preco = db.Column(db.Float)
    quantidade = db.Column(db.Integer)
    dataColeta = db.Column(db.Date)
    dataValidade = db.Column(db.Date)
