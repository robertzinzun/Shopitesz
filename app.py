from datetime import timedelta

from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_bootstrap import Bootstrap
from modelo.Dao import db,Categoria,Producto,Usuario
from flask_login import login_required,login_user,logout_user,current_user,LoginManager
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user_shopitesz:Shopit3sz.123@localhost/shopitesz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='Cl4v3'
#Implementación de la gestion de usuarios con flask-login
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='mostrar_login'
login_manager.refresh_view="mostrar_login"
login_manager.needs_refresh_message=("Tu sesión ha expirado, por favor inicia nuevamente tu sesión")
login_manager.needs_refresh_message_category="info"


@app.before_request
def before_request():
    session.permanent=True
    app.permanent_session_lifetime=timedelta(minutes=1)

@app.route("/")
def inicio():
    #return "Bienvenido a la tienda en linea Shopitesz"
    return render_template('principal.html')

@app.route('/Usuarios/iniciarSesion')
def mostrar_login():
    if current_user.is_authenticated:
        return render_template('principal.html')
    else:
        return render_template('usuarios/login.html')

@login_manager.user_loader
def cargar_usuario(id):
    return Usuario.query.get(int(id))

@app.route('/Usuarios/nuevo')
def nuevoUsuario():
    if current_user.is_authenticated:
        return render_template('principal.html')
    else:
        return render_template('usuarios/registrarCuenta.html')

@app.route('/Usuarios/agregar',methods=['post'])
def agregarUsuario():
    try:
        usuario=Usuario()
        usuario.nombreCompleto=request.form['nombre']
        usuario.telefono=request.form['telefono']
        usuario.direccion=request.form['direccion']
        usuario.email=request.form['email']
        usuario.genero=request.form['genero']
        usuario.password=request.form['password']
        usuario.tipo=request.values.get("tipo","Comprador")
        usuario.estatus='Activo'
        usuario.agregar()
        flash('¡ Usuario registrado con exito')
    except:
        flash('¡ Error al agregar al usuario !')
    return render_template('usuarios/registrarCuenta.html')


@app.route("/Usuarios/validarSesion",methods=['POST'])
def login():
    correo=request.form['correo']
    password=request.form['password']
    usuario=Usuario()
    user=usuario.validar(correo,password)
    print('Credenciales:'+request.form['correo']+","+request.form['password'])
    if user!=None:
        login_user(user)
        return render_template('principal.html')
    else:
        flash('Nombre de usuario o contraseña incorrectos')
        return render_template('usuarios/login.html')

@app.route('/Usuarios/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for('mostrar_login'))

@app.route("/productos")
def consultarProductos():
    #return "Retorna la lista de productos"
    producto=Producto()
    return render_template("productos/consultaGeneral.html",productos=producto.consultaGeneral())

@app.route("/productos/agregar")
def agregarProducto():
    return "<b>agregando un producto</b><table><th>Prueba</th></table>"

@app.route("/productos/actualizar")
def actualizarProducto():
    return "actualizando un producto"
@app.route("/cesta")
def consultarCesta():
    return "consultando la cesta de compra"

@app.route("/productos/categoria/<int:id>")
def consultarProductosCategoria(id):
    return "consultando los productos de la cetogoria: "+str(id)

@app.route("/clientes/<string:nombre>")
def consultarCliente(nombre):
    return "consultando al cliente:"+nombre

@app.route("/productos/<float:precio>")
def consultarPorductosPorPrecio(precio):
    return "Hola"+str(precio)

#CRUD de Categorias
@app.route('/Categorias')
def consultaCategorias():
    cat=Categoria()
    return render_template('categorias/consultaGeneral.html',categorias=cat.consultaGeneral())

@app.route('/Categorias/consultarImagen/<int:id>')
def consultarImagenCategoria(id):
    cat=Categoria()
    return cat.consultarImagen(id)


@app.route('/Categorias/nueva')
@login_required
def nuevaCategoria():
    if current_user.is_authenticated and current_user.is_admin():
        return render_template('categorias/agregar.html')
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Categorias/agregar',methods=['post'])
@login_required
def agregarCategoria():
    if current_user.is_authenticated and current_user.is_admin():
        try:
            cat=Categoria()
            cat.nombre=request.form['nombre']
            cat.imagen=request.files['imagen'].stream.read()
            cat.estatus='Activa'
            cat.agregar()
            flash('¡ Categoria agregada con exito !')
        except:
            flash('¡ Error al agregar la categoria !')
        return redirect(url_for('consultaCategorias'))
    else:
        return redirect(url_for('mostrar_login'))


@app.route('/Categorias/<int:id>')
@login_required
def consultarCategoria(id):
    if current_user.is_authenticated and current_user.is_admin():
        cat=Categoria()
        return render_template('categorias/editar.html',cat=cat.consultaIndividuall(id))
    else:
        return redirect(url_for('mostrar_login'))


@app.route('/Categorias/editar',methods=['POST'])
@login_required
def editarCategoria():
    if current_user.is_authenticated and current_user.is_admin():
        try:
            cat=Categoria()
            cat.idCategoria=request.form['id']
            cat.nombre=request.form['nombre']
            imagen=request.files['imagen'].stream.read()
            if imagen:
                cat.imagen=imagen
            cat.estatus=request.values.get("estatus","Inactiva")
            cat.editar()
            flash('¡ Categoria editada con exito !')
        except:
            flash('¡ Error al editar la categoria !')

        return redirect(url_for('consultaCategorias'))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Categorias/eliminar/<int:id>')
@login_required
def eliminarCategoria(id):
    if current_user.is_authenticated and current_user.is_admin():
        try:
            categoria=Categoria()
            #categoria.eliminar(id)
            categoria.eliminacionLogica(id)
            flash('Categoria eliminada con exito')
        except:
            flash('Error al eliminar la categoria')
        return redirect(url_for('consultaCategorias'))
    else:
        return redirect(url_for('mostrar_login'))

#Fin del crud de categorias
if __name__=='__main__':
    db.init_app(app)#Inicializar la BD - pasar la configuración de la url de la BD
    app.run(debug=True)

