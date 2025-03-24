import os
import random
import string
from werkzeug.datastructures import FileStorage
from models.user_model import User

def ctr_obtenerUsuarioEmail(email):
    return User.mdl_obtenerUsuarioEmail(email)

def ctr_obtenerUsuarioId(user_id):
    return User.mdl_obtenerUsuarioId(user_id)

def ctr_allUsuarios():
    return User.mdl_allUsuarios()

def ctr_crearUsuario(nombre, email, password, perfil, foto):
    User.mdl_crearUsuario(nombre, email, password, perfil, foto)
    return True

def ctr_guardarFotoUser(foto, upload_folder):
    if isinstance(foto, FileStorage) and foto.filename != '':
        nombre_archivo = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        extension = foto.filename.rsplit('.', 1)[1].lower()
        if extension in ['jpg', 'jpeg', 'png']:
            ruta_foto = os.path.join(upload_folder, f"{nombre_archivo}.{extension}")
            foto.save(ruta_foto)
            ruta_relativa = f"users/{nombre_archivo}.{extension}"
            return ruta_relativa
    return None

def ctr_actualizarEstadoUsuario(usuario_id, estado):
    User.mdl_actualizarEstadoUsuario(usuario_id, estado)
    return True

def ctr_actualizarUsuario(user_id, nombre, email, password, perfil, foto):
    User.mdl_actualizarUsuario(user_id, nombre, email, password, perfil, foto)
    return True 

def ctr_eliminarUsuario(user_id):
    User.mdl_eliminarUsuario(user_id)
    return True 

def ctr_contarUsuarios():
    return User.mdl_contarUsuarios() 
