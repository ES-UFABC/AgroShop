from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/entrar', methods = ['GET', 'POST'])
def login():
    data = request.form
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

        if len(email) < 4:
            flash('O email deve conter pelo menos caracteres.', category='error')
        elif len(nome) < 2:
            flash('O nome deve conter pelo menos 3 caracteres.', category='error')
        elif senha1 != senha2:
            flash('Senhas não são iguais.', category='error')
        elif len(senha1) < 7:
            flash('A senha deve ter pelo menos 8 caracteres.', category='error')
        else:
            flash('Account created!', category='success')
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