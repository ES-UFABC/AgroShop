from flask import Flask
from flask_sqlalchemy import  SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Grupo _4'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Cliente, Produtor 

    criar_dataBase(app)

    return app

def criar_dataBase(app):
    if not path('website/' + DB_NAME):
        db.create_all(app=app)
        print('DataBase Criado!')
