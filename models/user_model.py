from flask_login import UserMixin
from db import get_db_connection

class User(UserMixin):
    def __init__(self, user_id=None, nombre=None, email=None, password=None, estado=None, perfil=None, foto=None):
        self.id = user_id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.estado = estado
        self.perfil = perfil
        self.foto = foto

    @staticmethod
    def mdl_allUsuarios():
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, estado, nombre, email, perfil, foto FROM usuarios ORDER BY id DESC")
            users = cursor.fetchall()
        connection.close()

        usuarios = []
        for user in users:
            usuario = {
                'id': user[0],
                'estado': user[1],
                'nombre': user[2],
                'email': user[3],
                'perfil': user[4],
                'foto': user[5]
            }
            usuarios.append(usuario)

        return usuarios
    
    @staticmethod
    def mdl_obtenerUsuarioId(user_id):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre, email, password, estado, perfil, foto FROM usuarios WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
        connection.close()

        if user_data:
            usuario = User(*user_data)
            return usuario
        else:
            return None
    
    @staticmethod
    def mdl_obtenerUsuarioEmail(email):
        connection = get_db_connection()
        with connection.cursor(dictionary=True) as cursor: 
            cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
            user_data = cursor.fetchone()
        connection.close()
        if user_data:
            return User(user_data['id'], user_data['nombre'], user_data['email'], user_data['password'], user_data['estado'])
        else:
            return None
        
    @staticmethod
    def mdl_crearUsuario(nombre, email, password, perfil, foto):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO usuarios (nombre, email, password, estado, perfil, foto) VALUES (%s, %s, %s, 'active', %s, %s)", (nombre, email, password, perfil, foto))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return False
        finally:
            connection.close()

    @staticmethod
    def mdl_actualizarEstadoUsuario(id, estado):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE usuarios SET estado = %s WHERE id = %s", (estado, id))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error al cambiar el estado: {e}")
            return False
        finally:
            connection.close()

    @staticmethod
    def mdl_actualizarUsuario(id, nombre, email, password, perfil, foto):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE usuarios SET nombre = %s, email = %s, password = %s, perfil = %s, foto = %s WHERE id = %s", (nombre, email, password, perfil, foto, id))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar el usuario: {e}")
            return False
        finally:
            connection.close()
        
    @staticmethod
    def mdl_eliminarUsuario(id):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        connection.commit()
        connection.close()

    @staticmethod
    def mdl_contarUsuarios():
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM usuarios")
                count = cursor.fetchone()
            return count[0] if count else 0
        finally:
            connection.close()

