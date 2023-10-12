class Tarea:
    def __init__(self, nombre_tarea, descripcion, fecha_vencimiento, estado, tiempo_dedicado):
        self.nombre_tarea = nombre_tarea
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado
        self.tiempo_dedicado = tiempo_dedicado

    def formato_doc(self):
        return{
            'nombre_tarea' :  self.nombre_tarea,
            'descripcion': self.descripcion,
            'fecha_vencimiento': self.fecha_vencimiento,
            'estado': self.estado, 
            'tiempo_dedicado': self.tiempo_dedicado
        }

       