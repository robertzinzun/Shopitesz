from datetime import timedelta

from flask import Flask,render_template,request,redirect,url_for,flash,session,abort
from flask_bootstrap import Bootstrap
from modelo.Dao import db,Categoria,Producto,Usuario,Carrito
from flask_login import login_required,login_user,logout_user,current_user,LoginManager
import json

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user_shopitesz:Shopit3sz.123@localhost/shopitesz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='Cl4v3'
#Implementación de la gestion de usuarios con flask-login
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='mostrar_login'
login_manager.login_message='¡ Tu sesión expiró !'
login_manager.login_message_category="info"

# Urls defininas para el control de usuario
@app.before_request
def before_request():
    session.permanent=True
    app.permanent_session_lifetime=timedelta(minutes=10)

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
    if current_user.is_authenticated and not current_user.is_admin():
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

@app.route('/Usuarios/verPerfil')
@login_required
def consultarUsuario():
    return render_template('usuarios/editar.html')
#fin del manejo de usuarios
#Manejo de las rutas de productos
@app.route("/productos")
def consultarProductos():
    producto=Producto()
    return render_template("productos/consultaGeneral.html",productos=producto.consultaGeneral())

@app.route("/productos/categorias")
def productosPorCategoria():
    categoria=Categoria()
    return render_template('productos/productosPorCategoria.html',categorias=categoria.consultaGeneral())

@app.route("/productos/categoria/<int:id>")
def consultarProductosPorCategoria(id):
    producto=Producto()
    if id==0:
        lista=producto.consultaGeneral()
    else:
        lista=producto.consultarProductosPorCategoria(id)
    #print(lista)
    listaProductos=[]
    #Generacion de un diccionario para convertir los datos a JSON
    for prod in lista:
        prod_dic={'idProducto':prod.idProducto,'nombre':prod.nombre,'descripcion':prod.descripcion,'precio':prod.precioVenta,'existencia':prod.existencia}
        listaProductos.append(prod_dic)
    #print(listaProductos)
    var_json=json.dumps(listaProductos)
    return var_json

@app.route('/producto/<int:id>')

def consultarProducto(id):
    if current_user.is_authenticated and  current_user.is_comprador():
        prod=Producto()
        prod=prod.consultaIndividual(id)
        dict_producto={"idProducto":prod.idProducto,"nombre":prod.nombre,"descripcion":prod.descripcion,"precio":prod.precioVenta,"existencia":prod.existencia}
        return json.dumps(dict_producto)
    else:
        msg={"estatus":"error","mensaje":"Debes iniciar sesion"}
        return json.dumps(msg)

@app.route('/productos/foto/<int:id>')
def consultarFotoPorducto(id):
    prod=Producto()
    return prod.consultarFoto(id)
@app.route("/productos/agregar")
def agregarProducto():
    return "<b>agregando un producto</b><table><th>Prueba</th></table>"

@app.route("/productos/actualizar")
def actualizarProducto():
    return "actualizando un producto"
#fin del manejo de las rutas de productos

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
        abort(404)

@app.route('/Categorias/agregar',methods=['post'])
@login_required
def agregarCategoria():
    try:
        if current_user.is_authenticated:
            if current_user.is_admin():
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
                abort(404)

        else:
            return redirect(url_for('mostrar_login'))
    except:
        abort(500)


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
# manejo de pedidos
@app.route('/Pedidos')
@login_required
def consultarPedidos():
    return "Pedidos del usuario:"+current_user.nombreCompleto+", tipo:"+current_user.tipo

# fin del manejo de pedidos
# Seccion para el carrito
@app.route('/carrito/agregar/<data>',methods=['get'])
def agregarProductoCarrito(data):
    msg=''
    if current_user.is_authenticated and current_user.is_comprador():
        datos=json.loads(data)
        carrito=Carrito()
        carrito.idProducto=datos['idProducto']
        carrito.idUsuario=current_user.idUsuario
        carrito.cantidad=datos['cantidad']
        carrito.agregar()
        msg={'estatus':'ok','mensaje':'Producto agregado a la cesta.'}
    else:
        msg = {"estatus": "error", "mensaje": "Debes iniciar sesion"}
    return json.dumps(msg)

@app.route("/carrito")
@login_required
def consultarCesta():
    if current_user.is_authenticated:
        carrito=Carrito()
        return render_template('carrito/consultaGeneral.html',cesta=carrito.consultaGeneral(current_user.idUsuario))
    else:
        return redirect(url_for('mostrar_login'))
# fin de la seccion del carrito
#manejo de errores
@app.errorhandler(404)
def error_404(e):
    return render_template('comunes/error_404.html'),404

@app.errorhandler(500)
def error_500(e):
    return render_template('comunes/error_500.html'),500
if __name__=='__main__':
    db.init_app(app)#Inicializar la BD - pasar la configuración de la url de la BD
    app.run(debug=True)

