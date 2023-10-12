class Comentario:
    def __init__(self, nombre_usuario, comentario, fecha, nombre_proyecto):
        self.nombre_usuario = nombre_usuario
        self.comentario = comentario
        self.fecha = fecha
        self.nombre_proyecto = nombre_proyecto

    def formato_doc(self):
        return{
            'nombre_usuario' :  self.nombre_usuario,
            'comentario': self.comentario,
            'fecha': self.fecha,
            'nombre proyecto': self.nombre_proyecto
        }

       