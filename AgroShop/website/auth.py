from re import L
import sqlite3
from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from sqlalchemy import null
from website import views
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Carrinho, Cliente, Produtor, Produto
from . import db
from datetime import date

auth = Blueprint('auth', __name__)

@auth.route('/entrar', methods = ['GET', 'POST'])
def login():
    loginCliente = session.get('contaCliente', None)
    loginProdutor = session.get('conta', None)
    if loginCliente != None:
        return redirect(url_for('auth.home_cliente'))
    if loginProdutor != None:
        return redirect(url_for('auth.home_prod'))

    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('password')
        usuario = Cliente.query.filter_by(email=email).first()
        if usuario:
            if check_password_hash(usuario.senha, senha):
                flash('Login efetuado com Sucesso!', category='error')
                session['contaCliente'] = usuario.id
                return redirect(url_for('auth.home_cliente'))
            else:
                flash('Senha Incorreta', category='error')
        else:
            usuario = Produtor.query.filter_by(email=email).first()
            if usuario:
                if check_password_hash(usuario.senha, senha):
                    flash('Login efetuado com Sucesso!', category='error')
                    session['conta'] = usuario.id
                    return redirect(url_for('auth.home_prod'))
                else:
                    flash('Senha Incorreta', category='error')
            else:
                flash('E-mail não cadastrado', category='error') 
        
    return render_template("login.html")

@auth.route('/logout')
def logout():
    session['conta'] = None
    session['contaCliente'] = None
    return redirect(url_for('views.home'))

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
            flash('Account created!', category='error')
            #return redirect(url_for('auth.home_cliente'))

    return render_template("sign-up-client.html")

@auth.route('/cadastrar/produtor', methods = ['GET', 'POST'])
def sign_up_prod():
    
    if request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        senha1 = request.form.get('senha1')
        senha2 = request.form.get('senha2')

        usuario = Produtor.query.filter_by(email=email).first()
        if usuario:
            flash('Email já cadastrado', category='error')
        elif len(email) < 4:
            flash('O email deve conter pelo menos 5 caracteres.', category='error')
        elif len(nome) < 2:
            flash('O nome deve conter pelo menos 3 caracteres.', category='error')
        elif senha1 != senha2:
            flash('Senhas não são iguais.', category='error')
        elif len(senha1) < 7:
            flash('A senha deve ter pelo menos 8 caracteres.', category='error')
        else:
            new_user = Produtor(email=email, senha=generate_password_hash(senha1, method='sha256'), nome=nome)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='error')
            return redirect(url_for('views.home'))
    
    return render_template("sign-up-prod.html")

@auth.route('/HomeProd', methods = ['GET', 'POST'])
def home_prod():
    return render_template("home-prod.html")

@auth.route('/NovoProduto', methods = ['GET', 'POST'])
def novo_produto():
    loginProdutor = session.get('conta', None)
    if loginProdutor == None:
        flash('Faça o login em uma conta de produtor', category='error')
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':    
        tipo = request.form.get('tipo')
        quantidade = request.form.get('quantidade')
        preco = request.form.get('preco')
        strColeta = request.form.get('data_coleta')
        coleta = date(int(strColeta[0:4]), int(strColeta[5:7]), int(strColeta[8:]))       
        strValidade = request.form.get('data_validade')
        validade = date(int(strValidade[0:4]), int(strValidade[5:7]), int(strValidade[8:]))
        idProd = session.get('conta', None)
        novo_produto = Produto(tipo=tipo, quantidade=quantidade, preco=preco, dataColeta = coleta, dataValidade = validade, idProd = idProd)
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto Registrado', category='error')
        return redirect(url_for('auth.home_prod'))
    return render_template("new-product.html")

@auth.route('/HomeCliente', methods = ['GET', 'POST'])
def home_cliente():
    queryProdutos = """SELECT Produto.Id, Produtor.Nome, Produto.tipo, Produto.preco, Produto.quantidade, Produto.dataColeta, Produto.dataValidade 
    FROM Produto INNER JOIN Produtor on Produto.idProd=Produtor.id"""
    con = sqlite3.connect('AgroShop\website\database.db')
    db2 = con.cursor()
    Produtos = db2.execute(queryProdutos)
    Produto=Produtos.fetchall()
    soma = int(0)
    PrecoTotal = 0
    if request.method== 'POST':
        i = 1
        while i < 100:
            quantidade = request.form.get('id ' + str(i))
            if quantidade == "" or quantidade == null or quantidade is None:
                pass
            else:
                PrecoProd = db2.execute(f"SELECT Produto.Preco FROM Produto WHERE Produto.Id = {i}")
                PrecoProdList = PrecoProd.fetchall()
                Preco = PrecoProdList[0][0]
                PrecoTotal += Preco * int(quantidade)
                soma = soma + int(quantidade)
                idProduto = i
                idProdutorv = db2.execute(f"SELECT idProd FROM Produto WHERE id = {i}")
                idProdutolist = idProdutorv.fetchall()
                idProdutor = idProdutolist[0][0]
                idCliente = session.get('contaCliente', None)
                compra = Carrinho(idProduto=idProduto,idProdutor=int(idProdutor),idCliente=int(idCliente),quantidade=int(quantidade))
                db.session.add(compra)
                db.session.commit()
            i = i + 1
        flash('Produto Adicionado ao Carrinho', category='success')
    con.close()
    return render_template("home-cliente.html",Produto=Produto,soma=soma,PrecoTotal=PrecoTotal)

@auth.route('/MeuCarrinho', methods = ['GET', 'POST'])
def meu_carrinho():
    return render_template("home-cliente.html")

@auth.route('/Mercado', methods = ['GET','POST'])
def mercado():
    loginCliente = session.get('contaCliente', None)
    if loginCliente != None:
        return redirect(url_for('auth.home_cliente'))

    queryProdutos = """SELECT Produto.Id, Produtor.Nome, Produto.tipo, Produto.preco, Produto.quantidade, Produto.dataColeta, Produto.dataValidade 
    FROM Produto INNER JOIN Produtor on Produto.idProd=Produtor.id"""
    con = sqlite3.connect('AgroShop\website\database.db')
    db = con.cursor()
    Produtos = db.execute(queryProdutos)
    Produto=Produtos.fetchall()
    con.close()
    return render_template("mercado.html",Produto=Produto)

@auth.route('/carrinho', methods = ['GET','POST'])
def carrinho():
    idCliente = session.get('contaCliente', None)
    queryCarrinho = f"""SELECT Produto.tipo, SUM(Carrinho.quantidade), ROUND(SUM(Produto.preco), 2) FROM Produto INNER JOIN Carrinho on Carrinho.idProduto = Produto.id WHERE Carrinho.idCliente = {idCliente} GROUP BY Carrinho.idProduto"""
    con = sqlite3.connect('AgroShop\website\database.db')
    db2 = con.cursor()
    Produtos = db2.execute(queryCarrinho)
    Produto=Produtos.fetchall()
    PrecoTotal = 0
    for i in Produto:
        PrecoTotal += i[2] * i[1]
    PrecoTotal = round(PrecoTotal, 2)
    """if request.method== 'POST':
        i = 1
        while i < 100:
            quantidade = request.form.get('id ' + str(i))
            if quantidade == "" or quantidade == null or quantidade is None:
                pass
            else:
                PrecoProd = db2.execute(f""""SELECT ROUND(SUM(Produto.preco), 2) FROM Produto INNER JOIN Carrinho on Carrinho.idProduto = Produto.id WHERE Carrinho.idCliente = {idCliente} GROUP BY Carrinho.idProduto"""")
                PrecoProdList = PrecoProd.fetchall()
                Preco = PrecoProdList[0][0]
                PrecoTotal += Preco
                idProduto = i
                idProdutorv = db2.execute(f"SELECT idProd FROM Produto WHERE id = {i}")
                idProdutolist = idProdutorv.fetchall()
                idProdutor = idProdutolist[0][0]
                idCliente = session.get('contaCliente', None)
                compra = Carrinho(idProduto=idProduto,idProdutor=int(idProdutor),idCliente=int(idCliente),quantidade=int(quantidade))
                db.session.add(compra)
                db.session.commit()
            i = i + 1"""
    return render_template("carrinho.html",Produto=Produto, PrecoTotal = PrecoTotal)
    

