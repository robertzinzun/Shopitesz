from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,BLOB,ForeignKey,Float
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
db=SQLAlchemy()

class Categoria(db.Model):
    __tablename__='Categorias'
    idCategoria=Column(Integer,primary_key=True)
    nombre=Column(String,unique=True)
    estatus=Column(String,nullable=False)
    imagen=Column(BLOB)

    def consultaGeneral(self):
        return self.query.all()
        #return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividuall(self,id):
        return Categoria.query.get(id)

    def consultarImagen(self,id):
        return self.consultaIndividuall(id).imagen

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        cat=self.consultaIndividuall(id)
        db.session.delete(cat)
        db.session.commit()

    def eliminacionLogica(self,id):
        cat = self.consultaIndividuall(id)
        cat.estatus='Inactiva'
        cat.editar()

class Producto(db.Model):
    __tablename__='Productos'
    idProducto=Column(Integer,primary_key=True)
    idCategoria=Column(Integer,ForeignKey('Categorias.idCategoria'))
    nombre=Column(String,nullable=False)
    descripcion=Column(String,nullable=True)
    precioVenta=Column(Float,nullable=False)
    existencia=Column(Integer,nullable=False)
    foto=Column(BLOB)
    especificaciones=Column(BLOB)
    estatus=Column(String,nullable=False)
    categoria=relationship('Categoria',backref='productos',lazy='select')

    def consultaGeneral(self):
        return self.query.all()
    
class Usuario(UserMixin,db.Model):
    __tablename__='Usuarios'
    idUsuario=Column(Integer,primary_key=True)
    nombreCompleto=Column(String,nullable=False)
    direccion=Column(String,nullable=False)
    telefono=Column(String,nullable=False)
    email=Column(String,unique=True)
    password_hash=Column(String(256),nullable=False)
    tipo=Column(String,nullable=False)
    estatus=Column(String,nullable=False)

    @property #Implementa el metodo Get (para acceder a un valor)
    def password(self):
        raise AttributeError('El password no tiene acceso de lectura')

    @password.setter #Definir el metodo set para el atributo passwor_hash
    def password(self,password):#Se informa el password en formato plano para hacer el cifrado
        self.password_hash=generate_password_hash(password)

    def validarPassword(self,password):
        return check_password_hash(self.password_hash,password)
