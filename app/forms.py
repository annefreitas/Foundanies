from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_wtf import Form
from flask_mysqldb import MySQL
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SelectField, HiddenField, FieldList, RadioField
from passlib.hash import sha256_crypt
from functools import wraps
from wtforms.validators import DataRequired


# Cadastra Login
class LoginForm(Form):
    login = StringField('Nome de Usuário', validators=[DataRequired('Nome de Usuário é obrigatório')])
    senha = PasswordField('Senha', validators=[DataRequired('Senha é obrigatório')])

# Cadastra Usuario
class CadastraUsuarioForm(Form):
    usuario_nome = StringField('Nome Usuario', validators=[DataRequired('Nome de Usuário é obrigatório')])
    usuario_login = StringField('Login Usuario', validators=[DataRequired('Login do Usuario é obrigatório')])
    usuario_senha = PasswordField('Senha', validators=[DataRequired('Senha do Usuario é obrigatório')])


# Atualiza Usuário
class AtualizaUsuarioForm(Form):
    usuario_nome  = StringField('Nome do Usuário', validators=[])
    usuario_login = StringField('Login do Usuário', validators=[DataRequired('Login do Usuário é obrigatório')])
    usuario_id = HiddenField('ID Usuário', validators=[DataRequired('O ID do Usuário não pode ser indefinido')])
    usuario_senha = PasswordField('Senha do Usuário', validators=[DataRequired('A senha do Usuário é obrigatória')])

    
#Remover Usuário
class RemoveUsuarioForm(Form):
    # Implementa um campo em forma de lista, cujos elementos serão inputs do tipo HiddenField
    usuarios_ids = FieldList(HiddenField('IDs dos Usuários', validators=[DataRequired('Os IDs da lista não podem ser indefinidos')]), validators=[DataRequired('A lista de IDs não pode ser indefinida')])

