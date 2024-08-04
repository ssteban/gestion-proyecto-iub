from flask import Flask, request, jsonify, session
from flask_cors import CORS
from main import *
import bcrypt
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=2)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
#login usuario
@app.route('/login-u', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        role = VerificarRegistros_u(email, password)
        
        if role:
            session['user_id'] = email
            print(session)
            print("Correo iniciado: " + email)
            return jsonify(success=True, message="Inicio de sesión exitoso.", role=role)
        else:
            return jsonify(success=False, message="Correo electrónico o contraseña incorrectos.")
    except Exception as e:
        return jsonify(success=False, message="Error interno del servidor.", error=str(e))



#registrar usuario
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        correo = data.get('email')
        programa = data.get('progra')
        contra = data.get('pass1')
        
        if VerificarExistencia_u(correo):
            return jsonify(success=False, message="Las credenciales usadas ya se encuentran registradas.")
        else:
            contraEn = bcrypt.hashpw(contra.encode('utf-8'), bcrypt.gensalt())
            datos = (nombre, correo, programa, contraEn)
            if InsertInTable_U(datos, correo):
                return jsonify(success=True, message="Se ha registrado de manera exitosa.")
            else:
                return jsonify(success=False, message="Ocurrió un error al registrar los datos.")
    except Exception as e:
        return jsonify(success=False, message="Error interno del servidor.", error=str(e))

#evitar inicio ilegal
#@app.route('/is_authenticated')    
#def is_authenticated():
#    if 'user_id' in session:
#        print(session)
#        return jsonify(authenticated=True)
#    else:
#        return jsonify(authenticated=False)


#cerrar sesion
#@app.route('/logout', methods=['POST'])
#def cerrar():
#   session.clear()  # Limpia la sesión del usuario
 #   return '', 204  # Devuelve una respuesta sin contenido


#Registrar Proyectos
@app.route('/register-p', methods=['POST'])
def registrarproyectos_en_DB():
    try:
        data = request.get_json()
        titulo = data.get('titulo')
        resumen = data.get('resumen')
        facultad = data.get('facultad')
        programa = data.get('programa')
        tipo = data.get('tipoProyecto')
        palabrasC = data.get('palabrasClaves')
        estado = data.get('estadoProyecto')
        estudiante = data.get('estudiantes')
        docente = data.get('docente')
        registrado= data.get('registrado')   
        reg=Obtener_u(registrado)

        datos = (titulo, resumen, facultad, programa, tipo, palabrasC, estado, estudiante, docente, reg)
        
        if registrar_proyecto(datos):
            return jsonify(success=True, message="Se ha registrado de manera exitosa.")
        else:
            return jsonify(success=False, message="Lo sentimos, no se pudo registrar el proyecto.")
    except Exception as e:
        print(str(e))
        return jsonify(success=False, message="Error interno del servidor.", error=str(e))


#enviar correo
@app.route('/send-mail', methods=['POST'])
def send_mail():
    data = request.json
    correo = data.get('correo')
    result = enviar_correo(correo)
    print(result)
    return jsonify(success=result)


#mostrar proyectos
@app.route('/ver_proyectos', methods=['POST'])
def proyectos():
    return obtener_proyectos()

#mostrar los detalles del proyectos
@app.route('/proyecto', methods=['POST'])
def obtener_proyecto():
    data = request.get_json()
    if 'id' not in data:
        return jsonify(success=False, message='ID del proyecto no proporcionado'), 400
    
    proyecto_id = data['id']
    return detallesProyecto(proyecto_id)

#mostrar informacion del usuario
@app.route('/datos-u', methods=['POST'])
def Datos_Usuario():
    data=request.get_json()
    print(data)
    if 'correo' not in data:
        return jsonify(success=False, message='Error en la transferencia de datos'), 400
    
    correo_u=data['correo']
    return detallesusuario(correo_u)

#mostrar proyectos guardados por usuario
@app.route('/mis-proyectos', methods=['POST'])
def mis_proyectos_user():
    try:
        data = request.get_json()
        correo = data.get('correo')
        
        if not correo:
            return jsonify(success=False, message="Correo no proporcionado"), 400
        
        nombre = Obtener_u(correo)
        print(nombre)
        if nombre is False:
            return jsonify(success=False, message="Usuario no encontrado"), 404
        
        # Aquí va la lógica para obtener los proyectos del usuario
        # Supongamos que tienes una función `obtener_proyectos_usuario` que devuelve una lista de proyectos
        proyectos = obtener_proyectos_user(nombre)
        
        return jsonify(success=True, proyectos=proyectos)
    except Exception as e:
        print(f"Error al obtener proyectos del usuario: {e}")
        return jsonify(success=False, message="Error interno del servidor."), 500


#mostrar tendencias de proyectos
@app.route('/tendencias', methods=['POST'])
def tendencias():
    try:
        return contar_info_B()
    except Exception as e:
        print(e)
        return e


#actualizar contraseña
@app.route('/actualizar_contra_p', methods=['POST'])
def actualizar_contra_route():
    data = request.get_json()
    correo = data.get('correo')
    contraV = data.get('oldPassword')
    ContraN = data.get('newPassword')
    
    resultado = actualizar_contra(correo, contraV, ContraN)
    return jsonify(resultado)

@app.route('/obtener_filtro', methods=['POST'])
def obtener():
    try:
        data=request.get_json()
        facultad=data.get('facultad')
        programa=data.get('programa')
        estado=data.get('estado')
        return obtener_proyectos(facultad, programa, estado)
    except Exception as e:
        print(e)
        return e


@app.route('/actualizar', methods=['POST'])
def actualizar():
    data=request.get_json()
    usuario=data.get('user')
    correo=data.get('correo')

    return actualizar_datos(usuario, correo)


@app.route('/fotoP', methods=['POST'])
def fotoP():
    data=request.get_json()
    foto=data.get('foto')
    correo=data.get('correo')
    montarfoto(foto, correo)

@app.route('/ver_usuarios', methods=['POST'])
def ver_usuarios():
    data = request.get_json()
    nombre = data.get('nombre', '')
    return obtenerusuario(nombre)

@app.route('/usuario', methods=['POST'])
def usuario():
    data=request.get_json()
    id=data.get('id')
    return datallesuser(id)


@app.route('/obtenerdocumento', methods=['POST'])
def obtenerdocumento():
    data=request.get_json()
    id_proyecto=data.get('proyecto_id')
    archivo=data.get('archivo')
    nombre_archivo=data.get('nombre_archivo')
    datos=id_proyecto, nombre_archivo, archivo
    respuesta=montardocumento(datos)
    if respuesta:
        return jsonify(success=True, message='correcto')
    else:
        return jsonify(success=False, message='lo sentimos no se pudo montar el documento. intentelo mas tarde')

@app.route('/actualizar_usuario', methods=['POST'])
def actualizar_usuario():
    data = request.json
    user_id = data.get('id')
    nombre = data.get('nombre')
    correo = data.get('correo')
    programa = data.get('programa')
    usuario = data.get('usuario')
    datos=user_id, nombre, correo, programa, usuario
    if not (user_id and nombre and correo and programa and usuario):
        return jsonify(success=False, message='Datos incompletos'), 400
    return actualizar_user(datos)

@app.route('/register_user', methods=['POST'])
def registrar_usuario():
    data=request.get_json()
    nombre=data.get('nombre')
    correo=data.get('email')
    programa=data.get('progra')
    datos=nombre, correo, programa
    registrar_usuario_a(datos)


    
















if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
