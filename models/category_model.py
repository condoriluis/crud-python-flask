from db import get_db_connection

class Category:
    def __init__(self, id=None, categoria=None, descripcion=None):
        self.id = id
        self.categoria = categoria
        self.descripcion = descripcion

    @staticmethod
    def mdl_allCategorias():
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, estado, categoria, descripcion FROM categorias ORDER BY id DESC")
            categories = cursor.fetchall()
        connection.close()

        categorias = []
        for category in categories:
            categoria = {
                'id': category[0],
                'estado': category[1],
                'categoria': category[2],
                'descripcion': category[3]
            }
            categorias.append(categoria)

        return categorias

    @staticmethod
    def mdl_obtenerCategoriaId(categoria_id):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, categoria, descripcion FROM categorias WHERE id = %s", (categoria_id,))
            category = cursor.fetchone()
        connection.close()

        if category:
            categoria = {
                'id': category[0],
                'categoria': category[1],
                'descripcion': category[2]
            }
            return categoria
        else:
            return None

    @staticmethod
    def mdl_agregarCategoria(categoria, descripcion):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO categorias (estado, categoria, descripcion) VALUES ('Null', %s, %s)", (categoria.upper(), descripcion))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error al agregar la categoria: {e}")
            return False
        finally:
            connection.close()
            
    @staticmethod
    def mdl_actualizarEstadoCategoria(id, estado):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE categorias SET estado = %s WHERE id = %s", (estado, id))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error al cambiar el estado: {e}")
            return False
        finally:
            connection.close()

    @staticmethod
    def mdl_actualizarCategoria(id, categoria, descripcion):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE categorias SET categoria = %s, descripcion = %s WHERE id = %s", (categoria.upper(), descripcion, id))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar la categoria: {e}")
            return False
        finally:
            connection.close()
        
    @staticmethod
    def mdl_eliminarCategoria(id):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM categorias WHERE id = %s", (id,))
        connection.commit()
        connection.close()
        