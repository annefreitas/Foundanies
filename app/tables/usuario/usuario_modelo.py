class Usuario:
    def __init__(self,
                 id=0,
                 login="none",
                 senha="none",
                 logado=0,
                 email="none",
                 status=0):
                    self.id = id
                    self.login = login
                    self.senha = senha
                    self.logado = logado
                    self.email = email
                    self.status = status
                    

    def serializa(self):
        return {
                "id": self.id,
                "login": self.login,
                "senha": self.senha,
                "logado": self.logado,
                "email": self.email ,
                "status": self.status ,
                }
