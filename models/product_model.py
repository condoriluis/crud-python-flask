from db import get_db_connection
import os

class Product:
    def __init__(self, id=None, nombre=None, descripcion=None, cantidad=None, precio=None, categoria=None, foto=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio = precio
        self.categoria = categoria
        self.foto = foto

    @staticmethod
    def mdl_allProductos():
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria, foto FROM productos ORDER BY id DESC")
            products = cursor.fetchall()
        connection.close()

        productos = []
        for product in products:
            producto = {
                'id': product[0],
                'nombre': product[1],
                'descripcion': product[2],
                'cantidad': product[3],
                'precio': product[4],
                'categoria': product[5],
                'foto': product[6]
            }
            productos.append(producto)

        return productos

    @staticmethod
    def mdl_obtenerProductoId(producto_id):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria, foto FROM productos WHERE id = %s", (producto_id,))
            product = cursor.fetchone()
        connection.close()

        if product:
            producto = {
                'id': product[0],
                'nombre': product[1],
                'descripcion': product[2],
                'cantidad': product[3],
                'precio': product[4],
                'categoria': product[5],
                'foto': product[6]
            }
            return producto
        else:
            return None

    @staticmethod
    def mdl_agregarProducto(nombre, descripcion, cantidad, precio, categoria, foto):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria, foto) VALUES (%s, %s, %s, %s, %s, %s)", (nombre.upper(), descripcion, cantidad, precio, categoria, foto))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error al agregar el producto: {e}")
            return False
        finally:
            connection.close()

    @staticmethod
    def mdl_actualizarProducto(id, nombre, descripcion, cantidad, precio, categoria, foto):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE productos SET nombre = %s, descripcion = %s, cantidad = %s, precio = %s, categoria = %s, foto = %s WHERE id = %s", (nombre.upper(), descripcion, cantidad, precio, categoria, foto, id))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar el producto: {e}")
            return False
        finally:
            connection.close()
        
    @staticmethod
    def mdl_eliminarProducto(id):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT foto FROM productos WHERE id = %s", (id,))
            foto = cursor.fetchone()
            cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
        connection.commit()
        connection.close()
        if foto:
            foto_path = foto[0]
            if os.path.exists(foto_path):
                os.remove(foto_path)