from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

# Cliente
class modeloCliente(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del cliente")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    telefono: Optional[str] = Field(None, max_length=15)
    direccion: Optional[str] = Field(None, max_length=255)
    fecha_registro: Optional[datetime] = None
    pedidos: Optional[int] = 0
    cliente_frecuente: Optional[bool] = False

# Producto
class modeloProducto(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    stock: int
    categoria_id: int
    proveedor_id: int
    editorial_id: int

# Autenticación
class modeloAuth(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico válido", example="correo@example.com")
    passw: str = Field(..., min_length=8, strip_whitespace=True, description="Contraseña mínima de 8 caracteres")

# Proveedor
class modeloProveedor(BaseModel):
    nombre: str
    contacto: str
    telefono: str
    direccion: str

# Pedido
class modeloPedido(BaseModel):
    cliente_id: int
    fecha: datetime
    estado_id: int

# Detalle de pedido
class modeloDetallePedido(BaseModel):
    pedido_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float

# Estado de pedido
class modeloEstadoPedido(BaseModel):
    id: int
    estado: str

# Fechas de abastecimiento
class modeloFechaAbastecimiento(BaseModel):
    producto_id: int
    fecha_abastecimiento: datetime

# Usuario
class modeloUsuario(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=85)
    edad: int = Field(..., ge=1, le=120)
    correo: EmailStr