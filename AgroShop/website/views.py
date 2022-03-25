from flask import Blueprint, redirect, render_template, request

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/cadastrar', methods = ['GET', 'POST'])
def tipocadastro():      
    return render_template("tipo-cadastro.html")