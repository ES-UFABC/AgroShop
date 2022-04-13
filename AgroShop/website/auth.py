from flask import Blueprint, render_template, request, flash, redirect, url_for
from website import views
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Cliente
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/entrar', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = Cliente.query.filter_by(email=email).first()
        if usuario:
            if check_password_hash(usuario.senha, senha):
                flash('Login efetuado com Sucesso!', category='success')
            else:
                flash('Senha Incorreta', category='error')
        else:
            flash('E-mail não cadastrado', category='error') 
        
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return("<p>Logout</p>")

@auth.route('/cadastrar/cliente', methods = ['GET', 'POST'])
def sign_up_client():
    if request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        senha1 = request.form.get('senha1')
        senha2 = request.form.get('senha2')

        usuario = Cliente.query.filter_by(email=email).first()
        if usuario:
            flash('Email já cadastrado', category='error')
        elif len(email) < 4:
            flash('O email deve conter pelo menos caracteres.', category='error')
        elif len(nome) < 2:
            flash('O nome deve conter pelo menos 3 caracteres.', category='error')
        elif senha1 != senha2:
            flash('Senhas não são iguais.', category='error')
        elif len(senha1) < 7:
            flash('A senha deve ter pelo menos 8 caracteres.', category='error')
        else:
            new_user = Cliente(email=email, senha=generate_password_hash(senha1, method='sha256'), nome=nome)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign-up-client.html")

@auth.route('/cadastrar/produtor', methods = ['GET', 'POST'])
def sign_up_prod():
    
    if request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        senha1 = request.form.get('senha1')
        senha2 = request.form.get('senha2')

        if len(email) < 4:
            flash('O email deve conter pelo menos 5 caracteres.', category='error')
        elif len(nome) < 2:
            flash('O nome deve conter pelo menos 3 caracteres.', category='error')
        elif senha1 != senha2:
            flash('Senhas não são iguais.', category='error')
        elif len(senha1) < 7:
            flash('A senha deve ter pelo menos 8 caracteres.', category='error')
        else:
            flash('Account created!', category='success')
    
    return render_template("sign-up-prod.html")