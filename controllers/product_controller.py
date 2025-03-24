import os
import random
import string
from werkzeug.datastructures import FileStorage
from models.product_model import Product

def ctr_obtenerProductoId(producto_id):
    return Product.mdl_obtenerProductoId(producto_id)

def ctr_allProductos():
    return Product.mdl_allProductos()

def ctr_agregarProducto(nombre, descripcion, cantidad, precio, categoria, foto):
    Product.mdl_agregarProducto(nombre, descripcion, cantidad, precio, categoria, foto)
    return True
    
def ctr_guardarFoto(foto, upload_folder):
    if isinstance(foto, FileStorage) and foto.filename != '':
        nombre_archivo = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        extension = foto.filename.rsplit('.', 1)[1].lower()
        if extension in ['jpg', 'jpeg', 'png']:
            ruta_foto = os.path.join(upload_folder, f"{nombre_archivo}.{extension}")
            foto.save(ruta_foto)
            ruta_relativa = f"productos/{nombre_archivo}.{extension}"
            return ruta_relativa
    return None

def ctr_actualizarProducto(producto_id, nombre, descripcion, cantidad, precio, categoria, foto):
    Product.mdl_actualizarProducto(producto_id, nombre, descripcion, cantidad, precio, categoria, foto)
    return True 

def ctr_eliminarProducto(producto_id):
    Product.mdl_eliminarProducto(producto_id)
    return True
