from flask import Flask,render_template,request,redirect,url_for,flash
from flask_bootstrap import Bootstrap
from modelo.Dao import db,Categoria,Producto
from flask_login import login_required,login_user,logout_user,current_user,login_manager
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user_shopitesz:Shopit3sz.123@localhost/shopitesz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='Cl4v3'
@app.route("/")
def inicio():
    #return "Bienvenido a la tienda en linea Shopitesz"
    return render_template('principal.html')
@app.route('/validarSesion')
def validarSesion():
    return render_template('usuarios/login.html')

@app.route('/registrarCuenta')
def registrarCuenta():
    return render_template('usuarios/registrarCuenta.html')

@app.route("/login",methods=['POST'])
def login():
    correo=request.form['correo']
    return "Validando al usuario:"+correo

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
def nuevaCategoria():
    return render_template('categorias/agregar.html')

@app.route('/Categorias/agregar',methods=['post'])
def agregarCategoria():
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

@app.route('/Categorias/<int:id>')
def consultarCategoria(id):
    cat=Categoria()
    return render_template('categorias/editar.html',cat=cat.consultaIndividuall(id))

@app.route('/Categorias/editar',methods=['POST'])
def editarCategoria():
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
@app.route('/Categorias/eliminar/<int:id>')
def eliminarCategoria(id):
    try:
        categoria=Categoria()
        #categoria.eliminar(id)
        categoria.eliminacionLogica(id)
        flash('Categoria eliminada con exito')
    except:
        flash('Error al eliminar la categoria')
    return redirect(url_for('consultaCategorias'))


#Fin del crud de categorias
if __name__=='__main__':
    db.init_app(app)#Inicializar la BD - pasar la configuración de la url de la BD
    app.run(debug=True)

