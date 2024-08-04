import mysql.connector as sql
from flask import session, jsonify
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
    try:
        conn = sql.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
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

