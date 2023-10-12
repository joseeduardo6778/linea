class Proyecto:
    def __init__(self, nombreProyecto, descripcion, fecha_inicio, fecha_final, miembros_equipo,tareas ):

        self.nombreProyecto = nombreProyecto
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_final = fecha_final
        self.miembros_equipo = miembros_equipo
        self.tareas = tareas


    def formato_doc(self):
        return{
            'nombreProyecto': self.nombreProyecto,
            'descripcion': self.descripcion,
            'fecha_inicio': self.fecha_inicio,
            'fecha_final': self.fecha_final,
            'miembros_equipo': self.miembros_equipo,
            'tareas': self.tareas
        }