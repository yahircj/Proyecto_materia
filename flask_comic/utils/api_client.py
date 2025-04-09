import requests

API_BASE_URL = "http://localhost:8000"

# TOKEN JWT ESTÁTICO (usa tu propio valor si cambia)
API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGNvbWljLmNvbSIsInBhc3N3IjoiMTIzNDU2NzgifQ.vg_OHti7bw0GYCwnEteK83iTNbMrS3qpjIA2gjOiQDM"
HEADERS_AUTH = {"Authorization": f"Bearer {API_TOKEN}"}

# --------------------------
# CLIENTES
# --------------------------

def obtener_clientes():
    response = requests.get(f"{API_BASE_URL}/clientes")
    if response.status_code == 200:
        return response.json()
    return []

def obtener_cliente(cliente_id):
    response = requests.get(f"{API_BASE_URL}/clientes/{cliente_id}")
    if response.status_code == 200:
        return response.json()
    return None

def crear_cliente(data):
    response = requests.post(f"{API_BASE_URL}/clientes", json=data)
    return response.ok

def actualizar_cliente(cliente_id, data):
    response = requests.put(f"{API_BASE_URL}/clientes/{cliente_id}", json=data)
    return response.ok

def eliminar_cliente(cliente_id):
    response = requests.delete(f"{API_BASE_URL}/clientes/{cliente_id}")
    return response.ok

# --------------------------
# PRODUCTOS
# --------------------------

def obtener_productos():
    response = requests.get(f"{API_BASE_URL}/productos")
    if response.status_code == 200:
        return response.json()
    return []

def obtener_producto(producto_id):
    response = requests.get(f"{API_BASE_URL}/productos/{producto_id}")
    if response.status_code == 200:
        return response.json()
    return None

def crear_producto(data):
    response = requests.post(f"{API_BASE_URL}/productos", json=data)
    return response.ok

def actualizar_producto(producto_id, data):
    response = requests.put(f"{API_BASE_URL}/productos/{producto_id}", json=data)
    return response.ok

def eliminar_producto(producto_id):
    response = requests.delete(f"{API_BASE_URL}/productos/{producto_id}")
    return response.ok

# --------------------------
# PROVEEDORES
# --------------------------

def obtener_proveedores():
    response = requests.get(f"{API_BASE_URL}/proveedores")
    if response.status_code == 200:
        return response.json()
    return []

def obtener_proveedor(proveedor_id):
    response = requests.get(f"{API_BASE_URL}/proveedores/{proveedor_id}")
    if response.status_code == 200:
        return response.json()
    return None

def crear_proveedor(data):
    response = requests.post(f"{API_BASE_URL}/proveedores", json=data)
    return response.ok

def actualizar_proveedor(proveedor_id, data):
    response = requests.put(f"{API_BASE_URL}/proveedores/{proveedor_id}", json=data)
    return response.ok

def eliminar_proveedor(proveedor_id):
    response = requests.delete(f"{API_BASE_URL}/proveedores/{proveedor_id}")
    return response.ok

# --------------------------
# PEDIDOS
# --------------------------

def obtener_pedidos():
    response = requests.get(f"{API_BASE_URL}/pedidos", headers=HEADERS_AUTH)
    if response.status_code == 200:
        return response.json()
    return []

def obtener_pedido(pedido_id):
    response = requests.get(f"{API_BASE_URL}/pedidos/{pedido_id}")
    if response.status_code == 200:
        return response.json()
    return None

def crear_pedido(data):
    response = requests.post(f"{API_BASE_URL}/pedidos", json=data, headers=HEADERS_AUTH)
    if response.status_code == 200:
        return response.json()  # Para obtener el ID del nuevo pedido
    return None

def actualizar_pedido(pedido_id, data):
    response = requests.put(f"{API_BASE_URL}/pedidos/{pedido_id}", json=data)
    return response.ok

def eliminar_pedido(pedido_id):
    response = requests.delete(f"{API_BASE_URL}/pedidos/{pedido_id}")
    return response.ok

# --------------------------
# DETALLES DE PEDIDOS
# --------------------------

def obtener_detalles_pedido():
    response = requests.get(f"{API_BASE_URL}/detallepedidos")
    if response.status_code == 200:
        return response.json()
    return []

def obtener_detalle_pedido(detalle_id):
    response = requests.get(f"{API_BASE_URL}/detallepedidos/{detalle_id}")
    if response.status_code == 200:
        return response.json()
    return None

def crear_detalle_pedido(data):
    response = requests.post(f"{API_BASE_URL}/detallepedidos", json=data)
    return response.ok

def actualizar_detalle_pedido(detalle_id, data):
    response = requests.put(f"{API_BASE_URL}/detallepedidos/{detalle_id}", json=data)
    return response.ok

def eliminar_detalle_pedido(detalle_id):
    response = requests.delete(f"{API_BASE_URL}/detallepedidos/{detalle_id}")
    return response.ok


# ESTADOS DE PEDIDOS


def obtener_estados_pedido():
    response = requests.get(f"{API_BASE_URL}/estadospedidos")
    if response.status_code == 200:
        return response.json()
    return []

def obtener_estado_pedido(estado_id):
    response = requests.get(f"{API_BASE_URL}/estadospedidos/{estado_id}")
    if response.status_code == 200:
        return response.json()
    return None


# ABASTECIMIENTOS (FechasAbastecimiento)


def obtener_abastecimientos():
    response = requests.get(f"{API_BASE_URL}/fechasabastecimiento")
    if response.status_code == 200:
        return response.json()
    return []

def crear_abastecimiento(data):
    response = requests.post(f"{API_BASE_URL}/fechasabastecimiento", json=data)
    return response.ok

def actualizar_abastecimiento(abastecimiento_id, data):
    response = requests.put(f"{API_BASE_URL}/fechasabastecimiento/{abastecimiento_id}", json=data)
    return response.ok

def eliminar_abastecimiento(abastecimiento_id):
    response = requests.delete(f"{API_BASE_URL}/fechasabastecimiento/{abastecimiento_id}")
    return response.ok

def obtener_promociones():
    response = requests.get(f"{API_BASE_URL}/promociones")
    if response.status_code == 200:
        return response.json()
    return []