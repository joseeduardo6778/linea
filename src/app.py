from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import *
from bson.objectid import ObjectId
from tarea import Tarea
from comentario import Comentario
from registro import Registro
from perfil import Perfil
from proyecto import Proyecto
from datetime import date
from datetime import datetime
from flask import Flask, session

# Resto de la configuración de Flask-Login y definición de UserMixin, UserLoader, etc.


#conexion a al base de datos
con_bd = conexion()

app = Flask(__name__)



app.secret_key = 'Julian09'



#abre la pagina inicial
@app.route('/')
def index():
    return render_template('index.html')

#Abre el HTML del formulario tarea para crear una nueva     
@app.route('/tarea') 
def tarea():
    return render_template('tarea.html')

#Sirve para crea un tarea y guardarla en la base de datos
@app.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():
    Agregar_tarea = con_bd['Tarea']
    nombre_tarea = request.form['nombre_tarea']
    descripcion = request.form['descripcion']
    fecha_vencimiento = request.form['fecha_vencimiento']
    estado = request.form['estado']
    tiempo_dedicado = request.form['tiempo_dedicado']

    if nombre_tarea and descripcion and fecha_vencimiento and estado and tiempo_dedicado:
        tarea = Tarea(nombre_tarea, descripcion, fecha_vencimiento, estado, tiempo_dedicado)
        Agregar_tarea.insert_one(tarea.formato_doc())
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Sirve para abrir el HTML del formulario comentario
@app.route('/comentario/<string:nombreUsuario>')
def comentario(nombreUsuario):
    
    return render_template('comentario.html', nombreUsuario=nombreUsuario)

#Sirve para crea un comentario y guardarla en la base de datos
@app.route('/agregar_comentario', methods=['POST'])
def agregar_comentario():

    today = date.today()
    now = datetime.now()

    agregar_comentario = con_bd['Comentario']

    nombre_usuario = session.get('nombre_usuario')
    nombre_proyecto = request.form['nombre_proyecto']
    comentario = request.form['comentario']
    

    if nombre_usuario and comentario and now and nombre_proyecto:
        comen = Comentario(nombre_usuario, comentario, now, nombre_proyecto)
        agregar_comentario.insert_one(comen.formato_doc())
        return redirect(url_for('listaProyectos'))
    else:
        return redirect(url_for('index'))

@app.route('/editar_comentario/<string:comentario_id>', methods=['POST'])
def editar_comentario(comentario_id):
    agregar_comentario = con_bd['Comentario']
    if request.method == 'POST':
        nuevo_comentario = request.form.get('nuevo_comentario')
        agregar_comentario.update_one(
            {"_id": ObjectId(comentario_id)},
            {"$set": {"comentario": nuevo_comentario}}
        )
        return redirect(url_for('listaProyectos'))  # Redirige a la página principal después de editar
    
@app.route('/eliminar_comentario/<string:id_comentario>')
def eliminar(id_comentario):
    _id = ObjectId(id_comentario)
    proyecto_id = session.get('proyecto_id')
    comentarios= con_bd["Comentario"]
    comentarios.delete_one({'_id': _id})
    return redirect(url_for('detalle_proyecto', proyecto_id = proyecto_id))

@app.route('/eliminar_proyecto/<string:id_proyecto>')
def eliminar_proyecto(id_proyecto):
    _id = ObjectId(id_proyecto)
    proyecto_id = session.get('proyecto_id')
    proyectos= con_bd["Proyectos"]
    proyectos.delete_one({'_id': _id})
    return redirect(url_for('listaProyectos', proyectos = proyecto_id))


@app.route('/editar_proyecto/<string:proyecto_id>', methods=['GET', 'POST'])
def editar_proyecto(proyecto_id):
    agregar_proyectos = con_bd['Proyectos']
    # Recupera los detalles del proyecto según el proyecto_id
    proyecto = agregar_proyectos.find_one({"_id": proyecto_id})

    if request.method == 'POST':
        nuevo_nombre_proyecto = request.form.get('nombreProyecto')
        nueva_descripcion = request.form.get('descripcion')
        nueva_fecha_inicio = request.form.get('fecha_inicio')
        nueva_fecha_final = request.form.get('fecha_final')
        
        # Actualiza los detalles del proyecto en la base de datos
        agregar_proyectos.update_one(
            {"_id": ObjectId(proyecto_id)},
            {"$set": {
                "nombreProyecto": nuevo_nombre_proyecto,
                "descripcion": nueva_descripcion,
                "fecha_inicio": nueva_fecha_inicio,
                "fecha_final": nueva_fecha_final
            }}
        )
        return redirect(url_for('listaProyectos'))  # Redirige a la página principal después de editar

    return render_template('editar_proyectos.html', proyecto=proyecto)

@app.route('/detalles_proyecto/<string:proyecto_id>')
def detalles_proyecto(proyecto_id):
    agregar_comentario = con_bd['Comentario']
    proyecto = agregar_comentario.find_one({"_id": ObjectId(proyecto_id)})
    comentarios = agregar_comentario.find({"comentario": proyecto_id})

    return render_template('detalles_proyecto.html', proyecto=proyecto, comentarios=comentarios)
#Sirve para abrir el HTML del login
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/iniciar', methods=['GET','POST'])
def iniciar():
    logiar = con_bd['Usuario']
    nombre = request.form['nombre']
    password = request.form['password']
    usuario_encontrado = logiar.find_one({'nombre': nombre})
    if usuario_encontrado and usuario_encontrado['password'] == password:
        # Almacena el nombre de usuario en la sesión
        session['nombre_usuario'] = nombre
        return redirect(url_for('index'))
    else:
        return 'Credenciales incorrectas. Inténtalo de nuevo.'

#Abre el HTML donde esta el formulario de registro
@app.route('/registrar')
def registrar():
    return render_template('registrar.html')

#Sirve para el registro de usuarios y guardarla en la base de datos
@app.route('/registro', methods=['POST'])
def registro():
    registrar = con_bd['Usuario']
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    edad = request.form['edad']
    password = request.form['password']

    if nombre and password and telefono and edad:
        registro = Registro(nombre, password, telefono, edad)
        registrar.insert_one(registro.formato_doc())
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Registrar un nuevo perfil en la base de datos Perfil
@app.route('/crear_perfil', methods=['POST'])
def crearPerfil():
    perfiles = con_bd['Perfil']
    nombre_usuario = request.form['nombre_usuario']
    cargo = request.form['cargo']
    habilidades = request.form.getlist('habilidades[]')

    if nombre_usuario and cargo and habilidades:
        perfil = Perfil(nombre_usuario, cargo, habilidades)
        perfiles.insert_one(perfil.formato_doc())
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#Renderizar HTML     
@app.route('/crearUsuario')
def crearUsuario():
    return render_template('perfil.html')


@app.route('/crear_proyecto', methods=['POST'])
def crearProyecto():
    proyectos = con_bd['Proyectos']
    nombreProyecto = request.form['nombreProyecto']
    descripcion = request.form['descripcion']
    fecha_inicio = request.form['fecha_inicio']
    fecha_final = request.form['fecha_final']
    miembros_equipo = request.form.getlist('miembros_equipo[]')
    tareas = request.form.getlist('tareas[]')

    if nombreProyecto and fecha_inicio and fecha_final and miembros_equipo and tareas:
        proyecto = Proyecto(nombreProyecto, descripcion, fecha_inicio, fecha_final, miembros_equipo, tareas)
        proyectos.insert_one(proyecto.formato_doc())
        return redirect(url_for('index'))
    else:
       return redirect(url_for('index'))
    
@app.route('/crearProyecto')
def crearCrearProyecto():
    coneTarea= con_bd['Tarea']
    coneUser =con_bd['Perfil']
    documentosTarea = coneTarea.find()
    documentosuser = coneUser.find()
    return render_template('proyectos.html', tarea = documentosTarea, usuario = documentosuser)

@app.route('/lista_proyectos')
def listaProyectos():
    proyectos = con_bd['Proyectos'].find()
    return render_template('lista_proyectos.html', proyectos=proyectos)

@app.route('/lista_perfiles')
def listaPerfiles():
    perfiles = con_bd['Perfil'].find()
    return render_template('lista_perfiles.html', perfil =perfiles)

@app.route('/proyecto/<proyecto_id>')
def detalle_proyecto(proyecto_id):
    nombre_usuario = session.get('nombre_usuario')
    proyecto = con_bd['Proyectos'].find_one({'_id': ObjectId(proyecto_id)})
    session['proyecto_id']=proyecto_id
    comentarios = con_bd['Comentario'].find({'nombre proyecto': proyecto['nombreProyecto']})
    if proyecto:
        return render_template('detalle_proyecto.html', proyecto=proyecto, nombre_usuario=nombre_usuario, comentarios=comentarios)
    else:
        # Manejar el caso en que el proyecto no existe
        return redirect(url_for('listaProyectos'))







if __name__ == '__main__':
    app.run(debug=True)