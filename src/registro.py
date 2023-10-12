class Registro:
    def __init__(self, nombre, password, telefono, edad):
        self.nombre = nombre
        self.password = password
        self.edad = edad
        self.telefono = telefono

    def formato_doc(self):
        return{
            'nombre' :  self.nombre,
            'password': self.password,
            'edad': self.edad,
            'telefono': self.telefono
        }

       