class Perfil:
    def __init__(self, nombre_usuario, cargo, habilidades):

        self.nombre_usuario = nombre_usuario
        self.cargo = cargo
        self.habilidades = habilidades
   


    def formato_doc(self):
        return{
            'nombre_usuario': self.nombre_usuario,
            'cargo': self.cargo,
            'habilidades': self.habilidades
        }