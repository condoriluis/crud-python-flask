from models.category_model import Category

def ctr_obtenerCategoriaId(categoria_id):
    return Category.mdl_obtenerCategoriaId(categoria_id)

def ctr_allCategorias():
    return Category.mdl_allCategorias()

def ctr_agregarCategoria(categoria, descripcion):
    Category.mdl_agregarCategoria(categoria, descripcion)
    return True

def ctr_actualizarEstadoCategoria(categoria_id, estado):
    Category.mdl_actualizarEstadoCategoria(categoria_id, estado)
    return True
    
def ctr_actualizarCategoria(categoria_id, categoria, descripcion):
    Category.mdl_actualizarCategoria(categoria_id, categoria, descripcion)
    return True 

def ctr_eliminarCategoria(categoria_id):
    Category.mdl_eliminarCategoria(categoria_id)
    return True
