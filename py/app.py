from flask import Flask, request, jsonify, session
from flask_cors import CORS
import bcrypt
from datetime import timedelta
import mysql.connector as sql
import bcrypt
from datetime import datetime
import string
import random
#enviar correo
from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT', 3306)
}

#crear base de datos
def crear_base_de_datos():
    try:
        conn = sql.connect(**DB_CONFIG)

        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS GestionProyectosIUB")

        conn.close()
        print("Base de datos creada correctamente.")
    except Exception as e:
        print("Error al crear la base de datos:", e)

#Insertar datos en la base de datos
def InsertInTable_U(datos, correo):
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()
              
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id int not null auto_increment, 
                nombre varchar(255) not null,
                correo varchar(200) not null unique,
                programa varchar(255) not null,
                usuario varchar(30),
                contraseña text not null,
                foto_perfil longtext,
                fecha timestamp not null default current_timestamp(),
                primary key(id)
            )
        """)      
        cursor.execute("""
            INSERT INTO usuarios (nombre, correo, programa, contraseña) 
            VALUES (%s, %s, %s, %s)
        """, datos)   
        conn.commit()
        conn.close()
        print("Datos insertados correctamente.")
        if CrearRoll(correo, "estudiante"):
            return True
        else:
            return False
    except Exception as e:
        print("Error al insertar datos:", e)
        return False

#asignarle el roll al usuario
def CrearRoll(correo, cargo):
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()
              
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Roll (
                id int not null auto_increment,
                correo varchar(80) not null unique,
                cargo varchar(15) not null,
                fecha timestamp not null default current_timestamp(),
                primary key(id)
            )
        """)      
        cursor.execute("""
            INSERT INTO Roll (correo, cargo) 
            VALUES (%s, %s)
        """, (correo, cargo))   
        conn.commit()
        conn.close()
        print("Datos insertados correctamente.")
        return True
    except Exception as e:
        print("Error al insertar datos:", e)
        return False

#Verificar que el correo no exista en la base de datos
def VerificarExistencia_u(correo):
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT correo FROM usuarios WHERE correo = %s", (correo,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return True
        else:
            return False
    except Exception as e:
        print("Error al verificar la existencia del correo:", e)
        return False

#verificar si el usuario existe LOGIN
def VerificarRegistros_u(email, password):
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("SELECT correo, contraseña FROM usuarios WHERE correo = %s", (email,))
        user = cursor.fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            # Obtener el rol del usuario
            cursor.execute("SELECT cargo FROM Roll WHERE correo = %s", (email,))
            role = cursor.fetchone()
            
            conn.close()
            
            if role:
                session['email'] = email
                return role[0]  # Devolvemos el rol del usuario
            else:
                return None
        else:
            conn.close()
            return None
    except Exception as e:
        print("Error al verificar los registros:", e)
        return None


#Registrar los proyectos en la base de datos
def registrar_proyecto(datos):
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proyectos (
                id int not null auto_increment,
                titulo varchar(150) not null unique,
                resumen text not null,
                facultad varchar(120) not null,
                programa varchar(120) not null,
                tipo text not null,
                palabras_clave text not null,
                estado varchar(35) not null,
                estudiantes text not null,
                docente text not null,
                registrado text not null,
                fecha timestamp not null default current_timestamp(),
                primary key(id)
            )
        """)
        
        cursor.execute("""
            INSERT INTO proyectos (titulo, resumen, facultad, programa, tipo, palabras_clave, estado, estudiantes, docente, registrado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, datos)
        
        conn.commit()
        conn.close()
        print("Datos insertados correctamente.")
        return True
    except Exception as e:
        print("Error al insertar datos:", e)
        return False

#obtener nombre del que registra el proyecto
def Obtener_u(correo):
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM usuarios WHERE correo = %s", (correo,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return user[0]
        else:
            return False
    except Exception as e:
        print("Error al verificar la existencia del correo:", e)
        return False



#enviar correo de recuperacion a estudiante
def generar_contraseña_aleatoria(longitud=6):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def actualizar_contraseña_en_bd(email, nueva_contraseña):
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Encriptar la nueva contraseña
        hashed_password = bcrypt.hashpw(nueva_contraseña.encode('utf-8'), bcrypt.gensalt())
        
        # Actualizar la contraseña en la base de datos
        cursor.execute("UPDATE usuarios SET contraseña = %s WHERE correo = %s", (hashed_password, email))
        conn.commit()

        conn.close()
        return True
    except Exception as e:
        print(f"Error al actualizar la contraseña: {e}")
        return False

def enviar_correo(correo):
    # Generar nueva contraseña
    nueva_contraseña = generar_contraseña_aleatoria()
    
    # Actualizar la contraseña en la base de datos
    if actualizar_contraseña_en_bd(correo, nueva_contraseña):
        # Credenciales
        remitente = "gestionproyectoiub3@outlook.com"
        password = "fsdprzjzpaoxoxhn" 

        destinatario = correo
        mensaje = f"""
            Mensaje de recuperación de contraseña
            
            Su nueva contraseña es: {nueva_contraseña}
            
            Por favor, cambie esta contraseña después de iniciar sesión.
        """

        email = EmailMessage()
        email["From"] = remitente
        email["To"] = destinatario
        email["Subject"] = "Recuperación de Contraseña"
        email.set_content(mensaje)

        try:
            smtp = smtplib.SMTP("smtp.office365.com", port=587)
            smtp.starttls()
            smtp.login(remitente, password)
            smtp.sendmail(remitente, destinatario, email.as_string())
            smtp.quit()
            print("Correo enviado exitosamente")
            return True
        except Exception as e:
            print(f"Error al enviar correo: {e}")
            return False
    else:
        print("No se pudo actualizar la contraseña en la base de datos")
        return False

#mostrtrar proyectos a los usuarios
def obtener_proyectos():
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Seleccionar proyectos en orden descendente por fecha de registro
        cursor.execute("SELECT * FROM proyectos")
        proyectos = cursor.fetchall()
        print("proyectos: ",proyectos)
        conn.close()
        return jsonify(success=True, proyectos=proyectos)
    except Exception as e:
        print("Error al obtener proyectos:", e)
        return jsonify(success=False, message="Error al obtener proyectos.", error=str(e))


#mostrar informacion del proyectos
def detallesProyecto(id):
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proyectos WHERE id = %s", (id,))
        proyecto = cursor.fetchone()
        cursor.execute("SELECT * FROM documento WHERE id_proyecto = %s", (id,))
        documento=cursor.fetchone()
        conn.close()

        if proyecto:
            proyecto_dict = {
                'id': proyecto[0],
                'titulo': proyecto[1],
                'resumen': proyecto[2],
                'facultad': proyecto[3],
                'programa': proyecto[4],
                'tipo': proyecto[5],
                'palabras_clave': proyecto[6],
                'estado': proyecto[7],
                'estudiantes': proyecto[8],
                'docente': proyecto[9],
                'registrado': proyecto[10],
                'fecha': proyecto[11]
            }
            if documento:
                doc={
                    'titulo': documento[2],
                    'archivo': documento[3]
                }

                try:
                    if isinstance(proyecto_dict['fecha'], str):
                        proyecto_dict['fecha'] = datetime.strptime(proyecto_dict['fecha'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                    elif isinstance(proyecto_dict['fecha'], datetime):
                        proyecto_dict['fecha'] = proyecto_dict['fecha'].strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    # Manejar el caso donde la fecha no es válida
                    proyecto_dict['fecha'] = 'Fecha inválida'

                return jsonify(success=True, proyecto=proyecto_dict, doc=doc)

            else:
                # Intentar convertir la fecha a datetime si es una cadena válida
                try:
                    if isinstance(proyecto_dict['fecha'], str):
                        proyecto_dict['fecha'] = datetime.strptime(proyecto_dict['fecha'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                    elif isinstance(proyecto_dict['fecha'], datetime):
                        proyecto_dict['fecha'] = proyecto_dict['fecha'].strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    # Manejar el caso donde la fecha no es válida
                    proyecto_dict['fecha'] = 'Fecha inválida'
                return jsonify(success=True, proyecto=proyecto_dict)
        else:
            return jsonify(success=False, message="Proyecto no encontrado"), 404

    except Exception as e:
        print("Error al obtener el proyecto:", e)
        return jsonify(success=False, message="Error interno del servidor.", error=str(e)), 500

#mostrar informacion del usuario
def detallesusuario(correo):
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        datos = cursor.fetchone()
        conn.close()

        if datos:
            datos_user={
                'nombre': datos[1],
                'correo': datos[2],
                'programa': datos[3],
                'usuario':datos[4],
                'foto': datos[6],
                'fecha': datos[7]

            }
            return jsonify(success=True, datos=datos_user)
        else:
            return jsonify(success=False, message="Usuario no Encontrado"), 404
    except Exception as ex:
        print(ex)
        return ex

#obtener proyectos registradospor un usuario especifico
def obtener_proyectos_user(nombre):
    #poner inner join para unir tablas de proyectos y usuario para ver los proyectos que tiene el usuario
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        #cursor.execute("SELECT * FROM usuarios INNER JOIN proyectos ON usuarios.nombre=preoyectos.nombre=%s",(nombre,))
        cursor.execute("SELECT * FROM proyectos WHERE registrado = %s", (nombre,))
        proyectos = cursor.fetchall()
        
        conn.close()
        return proyectos
    except Exception as e:
        print("Error al obtener proyectos:", e)
        return jsonify(success=False, message="Error al obtener proyectos.", error=str(e))


#contra numero de proyectos por facultad
def Contar_Facultad():
    facultades = ["Facultad de Ciencias, Educación, Artes y Humanidades", 
                  "Facultad de Ciencias Económicas y Administrativas", 
                  "Facultad de Ingenierías"]
    res = []
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        for facultad in facultades:
            cursor.execute("SELECT COUNT(*) FROM proyectos WHERE facultad = %s", (facultad,))
            resultado = cursor.fetchone()
            res.append(resultado[0])
        conn.close()
        return jsonify(success=True, facultades=facultades, conteos=res)
    except Exception as e:
        print(e)
        return e


def Contar_Estado():
    estado = ["en-curso", 
                  "completado", 
                  "suspendido"]
    res = []
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        for facultad in estado:
            cursor.execute("SELECT COUNT(*) FROM proyectos WHERE facultad = %s", (facultad,))
            resultado = cursor.fetchone()
            res.append(resultado[0])
        conn.close()
        return jsonify(success=True, estado=estado, conteos=res)
    except Exception as e:
        print(e)
        return e

#contar informacion basica
def contar_info_B():
    facultades = ["Facultad de Ciencias, Educación, Artes y Humanidades", 
                  "Facultad de Ciencias Económicas y Administrativas", 
                  "Facultad de Ingenierías"]
    estados = ["en-curso", "completado", "suspendido"]
    resF = []
    resE = []
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Contar proyectos por facultad
        for facultad in facultades:
            cursor.execute("SELECT COUNT(*) FROM proyectos WHERE facultad = %s", (facultad,))
            resultado = cursor.fetchone()
            resF.append(resultado[0])
        # Contar proyectos por estado
        for estado in estados:
            cursor.execute("SELECT COUNT(*) FROM proyectos WHERE estado = %s", (estado,))
            resultado = cursor.fetchone()
            resE.append(resultado[0])
        conn.close()
        print(facultades, resF, estados, resE)
        return jsonify(success=True, facultades=facultades, conteosF=resF, estados=estados, conteosE=resE)
    except Exception as e:
        print(e)
        return jsonify(success=False, error=str(e))

#obtener el id del usuario
def obtener_id_por_correo(correo):
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (correo,))
        user_id = cursor.fetchone()
        conn.close()
        return user_id[0] if user_id else None
    except Exception as e:
        print(e)
        return None

#realizar proceso de actualizacion de contraseña
def actualizar_contra(correo, contraV, ContraN):
    user_id = obtener_id_por_correo(correo)
    if user_id is None:
        return {"success": False, "message": "Correo no encontrado"}
    
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Verificar si la contraseña actual es correcta
        cursor.execute("SELECT contraseña FROM usuarios WHERE id = %s", (user_id,))
        current_password = cursor.fetchone()

        if current_password and bcrypt.checkpw(contraV.encode('utf-8'), current_password[0].encode('utf-8')):
            # Encriptar la nueva contraseña
            hashed_contraN = bcrypt.hashpw(ContraN.encode('utf-8'), bcrypt.gensalt())

            # Actualizar la contraseña
            cursor.execute("UPDATE usuarios SET contraseña = %s WHERE id = %s", (hashed_contraN, user_id))
            conn.commit()
            conn.close()
            return {"success": True, "message": "Contraseña actualizada exitosamente"}
        else:
            conn.close()
            return {"success": False, "message": "Contraseña actual incorrecta"}

    except Exception as e:
        print(e)
        return {"success": False, "message": "Error al actualizar la contraseña"}
    

def obtener_proyectos(facultad=None, programa=None, estado=None):
    query = "SELECT * FROM proyectos WHERE 1=1"
    params = []

    if facultad and facultad != 'null':
        query += " AND facultad = %s"
        params.append(facultad)

    if programa and programa != 'null':
        query += " AND programa = %s"
        params.append(programa)

    if estado and estado != 'null':
        query += " AND estado = %s"
        params.append(estado)

    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        proyectos = cursor.fetchall()
        conn.close()
        return jsonify(success=True, proyectos=proyectos)
    except Exception as e:
        print("Error al obtener proyectos:", e)
        return jsonify(success=False, message="Error al obtener proyectos.", error=str(e))


def actualizar_datos(usuario, correo):
    try:
        user_id = obtener_id_por_correo(correo)
        if user_id is None:
            return jsonify(success=False, message="Usuario no encontrado")

        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Actualizar el nombre de usuario
        cursor.execute("UPDATE usuarios SET usuario = %s WHERE id = %s", (usuario, user_id))
        conn.commit()  # Confirmar la transacción

        # Verificar si la actualización se realizó correctamente
        cursor.execute("SELECT usuario FROM usuarios WHERE id = %s", (user_id,))
        current_usuario = cursor.fetchone()

        conn.close()
        if current_usuario and current_usuario[0] == usuario:
            return jsonify(success=True, message="Datos actualizados exitosamente")
        else:
            return jsonify(success=False, message="Error al actualizar los datos")
    except Exception as e:
        print(e)
        return jsonify(success=False, message="Ocurrió un error al actualizar los datos")
            

def montarfoto(foto, correo):
    if not correo or not foto:
        return jsonify(success=False, message="Correo o foto no proporcionados"), 400

    try:
        user_id = obtener_id_por_correo(correo)
        if not user_id:
            return jsonify(success=False, message="Usuario no encontrado"), 404

        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET foto_perfil = %s WHERE id = %s", (foto, user_id))
        conn.commit()
        conn.close()
        return jsonify(success=True, message="Foto de perfil actualizada exitosamente")
    except Exception as e:
        print(e)
        return jsonify(success=False, message="Error al actualizar la foto de perfil: " + str(e)), 500


def obtenerusuario(nombre):
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        if nombre:
            cursor.execute("SELECT id, nombre, correo, programa, usuario, fecha FROM usuarios WHERE nombre LIKE %s", ('%' + nombre + '%',))
        else:
            cursor.execute("SELECT id, nombre, correo, programa, usuario, fecha FROM usuarios")

        usuarios = cursor.fetchall()
        conn.close()

        usuarios_list = []
        for usuario in usuarios:
            usuarios_list.append({
                'id': usuario[0],
                'nombre': usuario[1],
                'correo': usuario[2],
                'programa': usuario[3],
                'usuario': usuario[4],
                'fecha': usuario[5]
            })

        return jsonify({'success': True, 'usuarios': usuarios_list})
    except Exception as e:
        print("Error al obtener usuarios:", e)
        return jsonify(success=False, message="Error al obtener usuarios.", error=str(e))
    

def datallesuser(id):
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        datos = cursor.fetchone()
        conn.close()

        if datos:
            usuario={
                'id': datos[0],
                'nombre': datos[1],
                'correo': datos[2],
                'programa': datos[3],
                'usuario':datos[4],
                'foto': datos[6],
                'fecha': datos[7]

            }
            return jsonify(success=True, usuario=usuario)
        else:
            return jsonify(success=False, message="Usuario no Encontrado"), 404
    except Exception as ex:
        print(ex)
        return ex



def montardocumento(datos):
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documento (
                id int NOT NULL AUTO_INCREMENT, 
                id_proyecto int NOT NULL UNIQUE,
                titulo varchar(255) NOT NULL,
                archivo longtext NOT NULL,
                fecha timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                PRIMARY KEY(id)
            )
        """)
        
        cursor.execute("""
            INSERT INTO documento (id_proyecto, titulo, archivo) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                titulo = VALUES(titulo), 
                archivo = VALUES(archivo),
                fecha = CURRENT_TIMESTAMP()
        """, datos)
        
        conn.commit()
        conn.close()
        print("Datos insertados/actualizados correctamente.")
        return True
    except Exception as e:
        print("Error al insertar/actualizar datos:", e)
        return False


def actualizar_user(datos):
    user_id, nombre, correo, programa, usuario = datos

    try:
        # Conectar a la base de datos
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Actualizar el usuario en la base de datos
        query = '''
        UPDATE usuarios
        SET nombre = %s, correo = %s, programa = %s, usuario = %s
        WHERE id = %s
        '''
        cursor.execute(query, (nombre, correo, programa, usuario, user_id))
        conn.commit()

        # Verificar si la actualización fue exitosa
        if cursor.rowcount == 0:
            return jsonify(success=False, message='Usuario no encontrado'), 404

        return jsonify(success=True, message='Usuario actualizado exitosamente')

    except sql.connect.Error as err:
        return jsonify(success=False, message=str(err)), 500

    finally:
        cursor.close()
        conn.close()

def registrar_usuario_a(datos):
    pass


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
