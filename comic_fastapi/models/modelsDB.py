from DB.conexion import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime

# Modelo: User (para login)
class User(Base):
    __tablename__ = 'tbUsers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    edad = Column(Integer)
    correo = Column(String)

# Modelo: Clientes
class Clientes(Base):
    __tablename__ = 'Clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    email = Column(String)
    telefono = Column(String)
    direccion = Column(String)
    fecha_registro = Column(DateTime)
    pedidos = Column(Integer)
    cliente_frecuente = Column(Boolean)

# Modelo: Productos
class Productos(Base):
    __tablename__ = 'Productos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    descripcion = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
    categoria_id = Column(Integer)
    proveedor_id = Column(Integer)
    editorial_id = Column(Integer)

# Modelo: Proveedores
class Proveedores(Base):
    __tablename__ = 'Proveedores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    contacto = Column(String)
    telefono = Column(String)
    direccion = Column(String)

# Modelo: Pedidos
class Pedidos(Base):
    __tablename__ = 'Pedidos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer)
    fecha = Column(DateTime)
    estado_id = Column(Integer)

# Modelo: DetallesPedidos 
class DetallesPedidos(Base):
    __tablename__ = 'DetallesPedidos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer)
    producto_id = Column(Integer)
    cantidad = Column(Integer)
    precio_unitario = Column(Float)

# Modelo: EstadosPedidos
class EstadosPedidos(Base):
    __tablename__ = 'EstadosPedidos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    estado = Column(String)

# Modelo: FechasAbastecimiento
class FechasAbastecimiento(Base):
    __tablename__ = 'FechasAbastecimiento'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer)
    fecha_abastecimiento = Column(DateTime)