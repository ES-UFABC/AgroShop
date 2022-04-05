from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#Tabelas

class Cliente(db.Model, UserMixin):
    #Colunas
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique = True)#maximo 150 caracteres, email repetido nao vale(unique)
    senha = db.Column(db.String(150))
    nome = db.Column(db.String(150))
   
class Produtor(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique = True)
    senha = db.Column(db.String(150))
    nome = db.Column(db.String(150))
