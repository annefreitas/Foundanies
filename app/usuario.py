class Usuario:
    def __init__(self,
                 id=0,
                 login="none",
                 senha="none",
                 nome="none",
                 logado=1):
                   self.nome = nome
                   self.id = id
                   self.login = login
                   self.senha = senha
                   self.logado = logado


    def serializa(self):
        return {
                "nome":self.nome,
                "id": self.id,
                "login": self.login,
                "senha": self.senha,
                "logado": self.logado,
                }
