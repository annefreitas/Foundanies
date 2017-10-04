class Usuario:
    def __init__(self,
                 id=0,
                 login="none",
                 senha="none",
                 logado=1,
                 nome="paca"):
                   self.id = id
                   self.login = login
                   self.senha = senha
                   self.logado = logado
                   self.nome = nome


    def serializa(self):
        return {
                "id": self.id,
                "login": self.login,
                "senha": self.senha,
                "logado": self.logado,
                  "nome": self.nome,
                }
