from fastapi import FastAPI
from DB.conexion import engine, Base

# Routers
from routers.usuario import routerUsuario
from routers.auth import routerAuth
from routers.clientes import routerClientes
from routers.productos import routerProductos 
from routers.proveedores import routerProveedores
from routers.pedidos import routerPedidos
from routers.detallepedidos import routerDetallePedidos
from routers.estadospedidos import routerEstadosPedidos
from routers.fechasabastecimiento import routerFechasAbastecimiento




app = FastAPI(
    title="API de Gestión de Clientes, Usuarios y Productos",
    description="API desarrollada con FastAPI y SQLAlchemy. Soporta autenticación JWT y operaciones CRUD.",
    version="1.0.0"
)

# Crear tablas automaticamente si no existen
Base.metadata.create_all(bind=engine)

# Ruta principal de prueba
@app.get("/", tags=["Inicio"])
def home():
    return {"mensaje": "¡Bienvenido a la API con FastAPI, SQLAlchemy y JWT!"}

#  todos los routers
app.include_router(routerUsuario)
app.include_router(routerAuth)
app.include_router(routerClientes)
app.include_router(routerProductos)  
app.include_router(routerProveedores)
app.include_router(routerPedidos)
app.include_router(routerDetallePedidos)
app.include_router(routerEstadosPedidos)
app.include_router(routerFechasAbastecimiento)