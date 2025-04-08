from datetime import datetime, timedelta
from DB.conexion import Session
from models.modelsDB import *

session = Session()

# Insertar EstadosPedidos
estados = [
    EstadosPedidos(estado="En proceso"),
    EstadosPedidos(estado="Enviado"),
    EstadosPedidos(estado="Entregado"),
    EstadosPedidos(estado="Cancelado"),
    EstadosPedidos(estado="Pendiente pago"),
    EstadosPedidos(estado="En preparación"),
    EstadosPedidos(estado="Devuelto"),
    EstadosPedidos(estado="Reembolsado"),
    EstadosPedidos(estado="En espera"),
    EstadosPedidos(estado="Completado")
]
session.add_all(estados)

# Insertar Proveedores
proveedores = [
    Proveedores(
        nombre=f"Proveedor {i}",
        contacto=f"Contacto {i}",
        telefono=f"+34 600 00 0{i}",
        direccion=f"Calle Proveedor {i}, Madrid"
    ) for i in range(10)
]
session.add_all(proveedores)

# Insertar Users
users = [
    User(
        nombre=f"Usuario {i}",
        edad=25 + i,
        correo=f"usuario{i}@ejemplo.com"
    ) for i in range(10)
]
session.add_all(users)

# Insertar Clientes
clientes = [
    Clientes(
        nombre=f"Cliente {i}",
        email=f"cliente{i}@empresa.com",
        telefono=f"+34 699 00 0{i}",
        direccion=f"Avenida Cliente {i}, Barcelona",
        fecha_registro=datetime.now() - timedelta(days=365 - i),
        pedidos=i * 3,
        cliente_frecuente=i > 4
    ) for i in range(10)
]
session.add_all(clientes)

# Insertar Productos
productos = [
    Productos(
        nombre=f"Producto {i}",
        descripcion=f"Descripción del producto {i}",
        precio=10.99 + i * 5,
        stock=100 - i * 10,
        categoria_id=i % 3 + 1,
        proveedor_id=i % 10 + 1,
        editorial_id=i % 4 + 1
    ) for i in range(10)
]
session.add_all(productos)

# Insertar Pedidos
pedidos = [
    Pedidos(
        cliente_id=i % 10 + 1,
        fecha=datetime.now() - timedelta(days=10 - i),
        estado_id=i % 10 + 1
    ) for i in range(10)
]
session.add_all(pedidos)

# Insertar DetallesPedidos
detalles = [
    DetallesPedidos(
        pedido_id=i % 10 + 1,
        producto_id=i % 10 + 1,
        cantidad=(i % 5) + 1,
        precio_unitario=10.99 + i * 5
    ) for i in range(10)
]
session.add_all(detalles)

# Insertar FechasAbastecimiento
fechas = [
    FechasAbastecimiento(
        producto_id=i % 10 + 1,
        fecha_abastecimiento=datetime.now() + timedelta(days=30 + i)
    ) for i in range(10)
]
session.add_all(fechas)

# Confirmar todos los cambios
session.commit()
session.close()

print("¡Datos de prueba insertados exitosamente!")