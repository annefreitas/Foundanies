class Usuario:
    def __init__(self,
                 id=0,
                 nome="paca",
                 login="none",
                 senha="none",
                 logado=1
                 ):
                   self.id = id
                   self.login = login
                   self.senha = senha
                   self.logado = logado
                   self.nome = nome


    def serializa(self):
        return {
                "id": self.id,
                "nome": self.nome,
                "login": self.login,
                "senha": self.senha,
                "logado": self.logado
                }
