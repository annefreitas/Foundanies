from flask_mysqldb import MySQL
from .funcionario import Funcionario
from .setor import Setor
from .usuario import Usuario
from .lotacao import Lotacao


class Zelda:

    def __init__(self, app):
        self.mysql = MySQL(app)

    def execute_query(self, query, insert=False):
        cur = self.mysql.connection.cursor()
        cur.execute(query)
        if insert:
            self.mysql.connection.commit()
        else:
            data = cur.fetchall()
            cur.close()
            return data

    def verifica_login(self, login, senha):
        data = self.execute_query("select count(*) from usuario where usuario_login = '{}' and usuario_senha = '{}'".format(login, senha))
        return int(data[0]['count(*)']) > 0

    # função que verifica se o usuário está logado. Utilizado no login único.
    def verifica_logado(self, login):
        data = self.execute_query("select usuario_logado from  usuario where usuario_login = '{}'".format(login))
        if (data[0]['usuario_logado'] == 1):
            return False
        return True

    def set_logado_true(self, login):
        data = self.execute_query("select usuario_id from usuario where usuario_login = '{}'".format(login))
        self.execute_query("update usuario set usuario_logado = 0 where  usuario_id = '{}'".format(data[0]['usuario_id']), True)

    def set_logado_false(self, login):
        data = self.execute_query("select usuario_id from usuario where usuario_login = '{}'".format(login))
        self.execute_query("update usuario set usuario_logado = 1 where usuario_id = '{}'".format(data[0]['usuario_id']), True)

    def set_admin_true(self, login):
        data = self.execute_query("select usuario_id from usuario where usuario_login = '{}'".format(login))
        self.execute_query("update usuario set usuario_admin = 0 where usuario_id = '{}'".format(data[0]['usuario_id']), True)

    def get_usuario_senha(self, login):
        data = self.execute_query("select usuario_senha from usuario where usuario_login = '{}'".format(login))
        return data

    # CRUD - USUARIO
    def cadastra_usuario(self, usuario):
        self.execute_query("insert into usuario (usuario_login, usuario_senha, usuario_logado) values ('{}', '{}', '{}')".format(usuario.login, usuario.senha, usuario.logado), True)

    def get_usuarios(self):
        data = self.execute_query("select * from usuario")
        usuarios = []
        for u in data:
            usuario = Usuario(
                id=u["usuario_id"],
                login=u["usuario_login"],
                senha=u["usuario_senha"],
                logado=u["usuario_logado"],
                admin=u["usuario_admin"])
            usuarios.append(usuario)
        return usuarios

    def get_usuarios_logados(self):
        data = self.execute_query("select * from usuario\
            where usuario_logado = 1")
        usuarios = []
        for u in data:
            usuario = Usuario(
                id=u["usuario_id"],
                login=u["usuario_login"],
                senha=u["usuario_senha"],
                logado=u["usuario_logado"],
                admin=u["usuario_admin"])
            usuarios.append(usuario)
        return usuarios

    def get_usuarios_admin(self):
        data = self.execute_query("select * from usuario where usuario_admin = 1")
        usuarios = []
        for u in data:
            usuario = Usuario(
                id=u["usuario_id"],
                login=u["usuario_login"],
                senha=u["usuario_senha"],
                logado=u["usuario_logado"],
                admin=u["usuario_admin"])
            usuarios.append(usuario)
        return usuarios

    def edita_usuario(self, usuario):
        self.execute_query("update usuario set usuario_login = '{}', usuario_senha = '{}', usuario_admin = '{}' where usuario_id = '{}'".format(usuario.login, usuario.senha, usuario.admin, usuario.id), True)

    def deleta_usuario(self, usuario_id):
        self.execute_query("delete from usuario where usuario_id = '{}'".format(usuario_id), True)


    # CRUD - USUARIO

    def get_usuarios(self):
        data = self.execute_query('''select * from usuario''')
        usuarios = []
        for d in data:
            usuario = Usuario(
                          id=d["usuario_id"],
                          login=d["usuario_login"],
                          senha=d["usuario_senha"],
                          logado=d["usuario_logado"])
            usuarios.append(usuario)
        return usuarios

    def get_usuario(self, id):
        data = self.execute_query('''select * from usuario where usuario_id = {}'''.format(id))
        if len(data) < 1:
            return None
        usuarios = []
        for d in data:
            usuario = Usuario(
                id=d["usuario_id"],
                login=d["usuario_login"],
                senha=d["usuario_senha"],
                logado=d["usuario_logado"])
            usuarios.append(usuario)
        return usuarios[0]
