from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, send_from_directory
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from .forms import *
from .classes import Criptografador
from flask_mysqldb import MySQL
from .db_interface import foundanies
from .usuario import Usuario
import os

from app import app

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'foundanies'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
db = foundanies(app)


# Index
@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()
    return render_template("login.html", form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        session['user_login'] = form.login.data
        senha = form.senha.data
        senhaHash = Criptografador.gerar_hash(senha, '')
        ans = db.verifica_login(login=form.login.data, senha=senhaHash)
        if ans:
            if (not db.verifica_logado(login=form.login.data)):
                db.set_logado_true(login=form.login.data)
                return redirect(url_for('admin_home'))
            return redirect(url_for('admin_home'))
        else:
            flash("Nome de usuário ou senha incorretos")
    else:
        flash_errors(form)

    return render_template('login.html', form=form)

@app.route("/up")
def up():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
    if (session['user_login'] == ""):
        return redirect(url_for('index'))
    usuarios = db.get_usuarios_logados()

    # return send_from_directory("images", filename, as_attachment=True)
    return redirect(url_for('admin_home'))

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/logout/')
def logout():
    session.pop('username', None)
    user_login = session.get('user_login', None)
    session['user_login'] = ''
    db.set_logado_false(user_login)
    return redirect(url_for('index'))


@app.route('/admin_home')
def admin_home():
    form = CadastraUsuarioForm()
    usuarios = db.get_usuarios_logados()
    if(session['user_login'] == ""):
        return redirect(url_for('index'))
    image_names = os.listdir('./app/images')
    return render_template('admin_home.html', usuarios=usuarios,image_names=image_names)


@app.route('/usuario')
def usuario_listar():
    usuarios = db.get_usuarios()
    if (session['user_login'] == ""):
        return redirect(url_for('index'))
    return render_template('usuario_listar.html', usuarios=usuarios)


@app.route('/cadastrar', methods=['GET', 'POST'])
def usuario_criar():
    form = CadastraUsuarioForm()
    if form.validate_on_submit():

        usuario = Usuario(
    nome=form.usuario_nome.data,
    login=form.usuario_login.data,
    senha=Criptografador.gerar_hash(
        form.usuario_senha.data,
        ''))

        db.cadastra_usuario(usuario)

        return redirect(url_for('index'))
    else:
        flash_errors(form)
        return render_template('usuario_criar.html', form=form)


@app.route('/usuario/<user_id>', methods=['GET', 'POST'])
def usuario_editar(user_id):
    form = AtualizaUsuarioForm()

    usuario = Usuario()

    if form.validate_on_submit():
        usuario.login = form.usuario_login.data
        usuario.id = form.usuario_id.data
        usuario.senha = Criptografador.gerar_hash(form.usuario_senha.data, '')
       # usuario.nome = form.usuario_nome.data

        db.edita_usuario(usuario)

        return redirect(url_for('usuario_listar'))
    else:

        usuario = db.get_usuario(user_id)

        if usuario is not None:
            form.process()

            form.usuario_login.data = usuario.login
            form.usuario_id.data = user_id

        else:
            return redirect(url_for('usuario_listar'))

        flash_errors(form)

    return render_template('usuario_editar.html', form=form)

@app.route('/usuario/remover', methods=['GET', 'POST'])
def usuario_remover():
    form = RemoveUsuarioForm()
    if request.method == 'POST':

        ids = request.form.getlist("ids[]")

        if request.form['origem'] == 'propria':

            # Percorre a lista de ids do FieldList
            for item in ids:
                # do qual pegamos o primeiro e único elemento
                db.deleta_usuario(item)

        # Se o form é inválido e a página foi acessada por POST
        else:
            usuarios = []

            if ids is not None and len(ids) > 0:

                # Lista os dados de cada funcionário na lista de ids[]
                for user_id in ids:
                    usuario = db.get_usuario(user_id)

                    if usuario is not None:
                        usuarios.append(usuario)

                return render_template('usuario_remover.html', form=request.form, usuarios=usuarios)

    """Se o método foi GET ou o form deu erro de submissão, redireciona pra página de listagem"""
    return redirect(url_for('usuario_listar'))


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error))
