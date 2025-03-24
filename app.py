import os
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash, generate_password_hash
from controllers.user_controller import ctr_contarUsuarios, ctr_obtenerUsuarioEmail, ctr_obtenerUsuarioId, ctr_allUsuarios, ctr_crearUsuario, ctr_guardarFotoUser, ctr_actualizarEstadoUsuario, ctr_actualizarUsuario, ctr_eliminarUsuario
from controllers.product_controller import ctr_allProductos, ctr_agregarProducto, ctr_obtenerProductoId, ctr_guardarFoto, ctr_actualizarProducto, ctr_eliminarProducto
from controllers.category_controller import ctr_allCategorias, ctr_agregarCategoria, ctr_actualizarEstadoCategoria, ctr_obtenerCategoriaId, ctr_actualizarCategoria, ctr_eliminarCategoria

app = Flask(__name__, template_folder='views')
app.config['SECRET_KEY'] = 'dev_killer'
app.config['PRODUCT_UPLOAD_FOLDER'] = 'static/img/productos'
app.config['USER_UPLOAD_FOLDER'] = 'static/img/users'

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('views/assets/', filename)

@login_manager.user_loader
def load_user(user_id):
    return ctr_obtenerUsuarioId(user_id)

@app.route('/')
def redirect_to_auth():
    usuarios_count = ctr_contarUsuarios()
    
    if usuarios_count == 0:
        return redirect(url_for('register'))
    
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        perfil = 'admin'
        password = generate_password_hash(request.form['password'])
        
        if ctr_crearUsuario(nombre, email, password, perfil, ''):
            flash('Usuario registrado correctamente. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error al registrar el usuario.', 'danger')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = ctr_obtenerUsuarioEmail(email)
        if user and check_password_hash(user.password, password):
            if user.estado == 'active':
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Su cuenta no está activa. Por favor, comuníquese con el administrador del sistema.', 'danger')
        else:
            flash('Credenciales incorrectas. Por favor, intenta de nuevo.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has Cerrado la sesión exitosamente', 'success')
    return redirect(url_for('login'))

@app.route('/inicio')
@login_required
def index():
    user = current_user
    categorias = ctr_allCategorias()
    productos = ctr_allProductos()
    usuarios = ctr_allUsuarios()
    return render_template('index.html', user=user, productos=productos ,categorias=categorias, usuarios=usuarios)


@app.route('/usuarios')
@login_required
def mostrar_usuarios():
    user = current_user
    usuarios = ctr_allUsuarios()
    return render_template('usuarios.html', user=user, usuarios=usuarios)

@app.route('/agregar_usuario', methods=['GET', 'POST'])
@login_required
def agregar_usuario():
    if request.method == 'POST':
       
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        perfil = request.form['perfil']
    
        password_hash = generate_password_hash(password)
        
        # Procesar la foto
        if 'foto' in request.files:
            foto = request.files['foto']
           
            if foto and foto.filename != '':
                ruta_foto = ctr_guardarFotoUser(foto, app.config['USER_UPLOAD_FOLDER'])
                if ruta_foto:
                    if ctr_crearUsuario(nombre, email, password_hash, perfil, ruta_foto):
                        flash('Usuario agregado correctamente', 'success')
                        return redirect(url_for('mostrar_usuarios'))
                    else:
                        flash('Error al agregar el usuario', 'danger')
                        return redirect(url_for('agregar_usuario'))
                else:
                    flash('Error al guardar la foto', 'danger')
                    return redirect(url_for('agregar_usuario'))
            else:
                flash('No se ha seleccionado ninguna foto', 'danger')
                return redirect(url_for('agregar_usuario'))
        else:
            flash('No se ha proporcionado ninguna foto', 'danger')
            return redirect(url_for('agregar_usuario'))
    else:
        usuarios = ctr_allUsuarios()
        user = current_user
        return render_template('agregar_usuario.html', user=user, usuarios=usuarios)
    
@app.route('/cambiar_status_us', methods=['POST'])
@login_required
def cambiar_status_user():
    if request.method == 'POST':
        categoria_id = request.form.get('id')
        estado = request.form.get('estado')
        if ctr_actualizarEstadoUsuario(categoria_id, estado):
            flash('Estado cambiado correctamente', 'success')
            return jsonify({"message": "Estado cambiado correctamente"}), 200
        else:
            flash('Error al cambiar el estado', 'danger')
            return jsonify({"error": "Error al cambiar el estado"}), 500
        
@app.route('/editar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(usuario_id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        perfil = request.form['perfil']
    
        usuario = ctr_obtenerUsuarioId(usuario_id)
        if not usuario:
            flash('El usuario no existe', 'danger')
            return redirect(url_for('mostrar_usuarios'))
        
        if not password:
            password_actualizado = usuario.password
        else:
            password_actualizado = generate_password_hash(password)
        
        nueva_foto = request.files['foto']
        if nueva_foto and nueva_foto.filename != '':
            ruta_foto = ctr_guardarFotoUser(nueva_foto, app.config['USER_UPLOAD_FOLDER'])
            if ruta_foto:
                eliminar_foto_anterior_user(usuario.foto)
                usuario.foto = ruta_foto
            else:
                flash('Error al guardar la nueva foto', 'danger')
                return redirect(url_for('editar_usuario', usuario_id=usuario_id))
        
        if ctr_actualizarUsuario(usuario_id, nombre, email, password_actualizado, perfil, usuario.foto):
            flash('Usuario actualizado correctamente', 'success')
        else:
            flash('Error al actualizar el usuario', 'danger')
        
        return redirect(url_for('mostrar_usuarios'))
    else:
        
        usuario = ctr_obtenerUsuarioId(usuario_id)
        if usuario:
            user = current_user
            return render_template('editar_usuario.html', user=user, usuario=usuario)
        else:
            flash('El usuario no existe', 'danger')
            return redirect(url_for('mostrar_usuarios'))

def eliminar_foto_anterior_user(ruta_foto):
    if ruta_foto:
        ruta_completa = os.path.join(app.config['USER_UPLOAD_FOLDER'], ruta_foto)
        if os.path.exists(ruta_completa):
            os.remove(ruta_completa)
    
@app.route('/eliminar_usuario/<int:usuario_id>', methods=['GET'])
@login_required
def eliminar_usuario(usuario_id):
    if ctr_eliminarUsuario(usuario_id):
        flash('Usuario eliminado correctamente', 'success')
    else:
        flash('Error al eliminar el usuario', 'danger')
    
    return redirect(url_for('mostrar_usuarios'))


@app.route('/productos')
@login_required
def mostrar_productos():
    user = current_user
    categorias = ctr_allCategorias()
    productos = ctr_allProductos()
    return render_template('productos.html', user=user, productos=productos ,categorias=categorias)

@app.route('/agregar_producto', methods=['GET', 'POST'])
@login_required
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        categoria = request.form['categoria']
        
        if 'foto' in request.files:
            foto = request.files['foto']
            if foto and foto.filename != '':
                ruta_foto = ctr_guardarFoto(foto, app.config['PRODUCT_UPLOAD_FOLDER'])
                if ruta_foto:
                    if ctr_agregarProducto(nombre, descripcion, cantidad, precio, categoria, ruta_foto):
                        flash('Producto agregado correctamente', 'success')
                        return redirect(url_for('mostrar_productos'))
                    else:
                        flash('Error al agregar el producto', 'danger')
                        return redirect(url_for('agregar_producto'))
                else:
                    flash('Error al guardar la foto', 'danger')
                    return redirect(url_for('agregar_producto'))
            else:
                flash('No se ha seleccionado ninguna foto', 'danger')
                return redirect(url_for('agregar_producto'))
        else:
            flash('No se ha proporcionado ninguna foto', 'danger')
            return redirect(url_for('agregar_producto'))
    else:
        categorias = ctr_allCategorias()
        user = current_user
        return render_template('agregar_producto.html', user=user, categorias=categorias)

@app.route('/editar_producto/<int:producto_id>', methods=['GET', 'POST'])
@login_required
def editar_producto(producto_id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        categoria = request.form['categoria']
    
        producto = ctr_obtenerProductoId(producto_id)
        if not producto:
            flash('El producto no existe', 'danger')
            return redirect(url_for('mostrar_productos'))
        
        nueva_foto = request.files['foto']
        if nueva_foto and nueva_foto.filename != '':
            ruta_foto = ctr_guardarFoto(nueva_foto, app.config['PRODUCT_UPLOAD_FOLDER'])
            if ruta_foto:
                eliminar_foto_anterior(producto.get('foto'))
                producto['foto'] = ruta_foto
            else:
                flash('Error al guardar la nueva foto', 'danger')
                return redirect(url_for('editar_producto', producto_id=producto_id))
        
        if ctr_actualizarProducto(producto_id, nombre, descripcion, cantidad, precio, categoria, producto.get('foto')):
            flash('Producto actualizado correctamente', 'success')
        else:
            flash('Error al actualizar el producto', 'danger')
        
        return redirect(url_for('mostrar_productos'))
    else:
        producto = ctr_obtenerProductoId(producto_id)
        if producto:
            user = current_user
            categorias = ctr_allCategorias()
            return render_template('editar_producto.html', user=user, producto=producto, categorias=categorias)
        else:
            flash('El producto no existe', 'danger')
            return redirect(url_for('mostrar_productos'))

def eliminar_foto_anterior(ruta_foto):
    if ruta_foto:
        ruta_completa = os.path.join(app.config['UPLOAD_FOLDER'], ruta_foto)
        if os.path.exists(ruta_completa):
            os.remove(ruta_completa)
            
@app.route('/eliminar_producto/<int:producto_id>', methods=['GET'])
@login_required
def eliminar_producto(producto_id):
    if ctr_eliminarProducto(producto_id):
        flash('Producto eliminado correctamente', 'success')
    else:
        flash('Error al eliminar el producto', 'danger')
    
    return redirect(url_for('mostrar_productos'))


@app.route('/categorias')
@login_required
def mostrar_categorias():
    user = current_user
    categorias = ctr_allCategorias()
    return render_template('categorias.html', user=user, categorias=categorias)

@app.route('/agregar_categoria', methods=['GET', 'POST'])
@login_required
def agregar_categoria():
    if request.method == 'POST':
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']

        if ctr_agregarCategoria(categoria, descripcion):
            flash('Categoría agregado correctamente', 'success')
            return redirect(url_for('mostrar_categorias'))
        else:
            flash('Error al agregar la categoría', 'danger')
            return redirect(url_for('agregar_categoria'))
    else:
        user = current_user
        return render_template('agregar_categoria.html', user=user)

@app.route('/cambiar_status', methods=['POST'])
@login_required
def cambiar_status():
    if request.method == 'POST':
        categoria_id = request.form.get('id')
        estado = request.form.get('estado')
        if ctr_actualizarEstadoCategoria(categoria_id, estado):
            flash('Estado cambiado correctamente', 'success')
            return jsonify({"message": "Estado cambiado correctamente"}), 200
        else:
            flash('Error al cambiar el estado', 'danger')
            return jsonify({"error": "Error al cambiar el estado"}), 500
        
@app.route('/editar_categoria/<int:categoria_id>', methods=['GET', 'POST'])
@login_required
def editar_categoria(categoria_id):
    if request.method == 'POST':
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']
        
        if ctr_actualizarCategoria(categoria_id, categoria, descripcion):
            flash('Categoría actualizado correctamente', 'success')
        else:
            flash('Error al actualizar la categoría', 'danger')
        
        return redirect(url_for('mostrar_categorias'))
    else:
        categoria = ctr_obtenerCategoriaId(categoria_id)
        if categoria:
            user = current_user
            return render_template('editar_categoria.html', user=user, categoria=categoria)
        else:
            flash('La categoría no existe', 'danger')
            return redirect(url_for('mostrar_categorias'))

@app.route('/eliminar_categoria/<int:categoria_id>', methods=['GET'])
@login_required
def eliminar_categoria(categoria_id):
    if ctr_eliminarCategoria(categoria_id):
        flash('Categoría eliminado correctamente', 'success')
    else:
        flash('Error al eliminar la categoría', 'danger')
    
    return redirect(url_for('mostrar_categorias'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)