from db.conexion import Base
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Text, ForeignKey

# Modelo: User (para login)
class User(Base):
    __tablename__ = 'Usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    edad = Column(Integer)
    correo = Column(String(100))

# Modelo: Clientes
class Clientes(Base):
    __tablename__ = 'Clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    email = Column(String(100))
    telefono = Column(String(15))
    direccion = Column(String(255))
    fecha_registro = Column(DateTime)
    pedidos = Column(Integer)
    cliente_frecuente = Column(Boolean)

# Modelo: Productos
class Productos(Base):
    __tablename__ = 'Productos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    descripcion = Column(Text)
    precio = Column(Numeric(10,2))
    stock = Column(Integer)
    categoria_id = Column(Integer)
    proveedor_id = Column(Integer)
    editorial_id = Column(Integer)

# Modelo: Proveedores
class Proveedores(Base):
    __tablename__ = 'Proveedores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    contacto = Column(String(100))
    telefono = Column(String(15))
    direccion = Column(String(255))

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
    precio_unitario = Column(Numeric(10,2))

# Modelo: EstadosPedidos
class EstadosPedidos(Base):
    __tablename__ = 'EstadosPedidos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    estado = Column(String(50))

# Modelo: FechasAbastecimiento
class FechasAbastecimiento(Base):
    __tablename__ = 'FechasAbastecimiento'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer)
    fecha_abastecimiento = Column(DateTime)

# Modelo: TiposPromociones
class TiposPromociones(Base):
    __tablename__ = 'TiposPromociones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    detalle_promocion = Column(String(10))

# Modelo: Promociones
class Promociones(Base):
    __tablename__ = 'Promociones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey('Productos.id'))
    promocion_id = Column(Integer, ForeignKey('TiposPromociones.id'))
    