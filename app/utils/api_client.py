import requests

API_BASE_URL = "http://api:8000/"

# CLIENTES
def obtener_clientes():
    response = requests.get(f"{API_BASE_URL}/clientes")
    print("STATUS:", response.status_code)
    print("RESPUESTA:", response.text)
    if response.status_code == 200:
        return response.json()
    return []

def crear_cliente(data):
    response = requests.post(f"{API_BASE_URL}/clientes", json=data)
    return response.ok

def actualizar_cliente(cliente_id, data):
    response = requests.put(f"{API_BASE_URL}/clientes/{cliente_id}", json=data)
    return response.ok

def eliminar_cliente(cliente_id):
    response = requests.delete(f"{API_BASE_URL}/clientes/{cliente_id}")
    return response.ok

def obtener_cliente(cliente_id):
    response = requests.get(f"{API_BASE_URL}/clientes/{cliente_id}")
    if response.status_code == 200:
        return response.json()
    return None

import requests

API_BASE_URL = "http://localhost:8000"

# Productos
def obtener_productos():
    response = requests.get(f"{API_BASE_URL}/productos")
    print("STATUS:", response.status_code)
    print("RESPUESTA:", response.text)
    if response.status_code == 200:
        return response.json()
    return []

def crear_producto(data):
    response = requests.post(f"{API_BASE_URL}/productos", json=data)
    return response.ok

def actualizar_producto(producto_id, data):
    response = requests.put(f"{API_BASE_URL}/productos/{producto_id}", json=data)
    return response.ok

def eliminar_producto(producto_id):
    response = requests.delete(f"{API_BASE_URL}/productos/{producto_id}")
    return response.ok

def obtener_producto(producto_id):
    response = requests.get(f"{API_BASE_URL}/productos/{producto_id}")
    if response.status_code == 200:
        return response.json()
    return None

# Proveedores
def obtener_proveedores():
    response = requests.get(f"{API_BASE_URL}/proveedores")
    print("STATUS:", response.status_code)
    print("RESPUESTA:", response.text)
    if response.status_code == 200:
        return response.json()
    return []

def crear_proveedor(data):
    response = requests.post(f"{API_BASE_URL}/proveedores", json=data)
    return response.ok

def actualizar_proveedor(proveedor_id, data):
    response = requests.put(f"{API_BASE_URL}/proveedores/{proveedor_id}", json=data)
    return response.ok

def eliminar_proveedor(proveedor_id):
    response = requests.delete(f"{API_BASE_URL}/proveedores/{proveedor_id}")
    return response.ok

def obtener_proveedor(proveedor_id):
    response = requests.get(f"{API_BASE_URL}/proveedores/{proveedor_id}")
    if response.status_code == 200:
        return response.json()
    return None


# En utils/api_client.py

# Variable global para almacenar el token
API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGNvbWljLmNvbSIsInBhc3N3IjoiMTIzNDU2NzgifQ.vg_OHti7bw0GYCwnEteK83iTNbMrS3qpjIA2gjOiQDM"  # O cárgalo desde configuración o variable de entorno

# Pedidos
def obtener_pedidos():
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.get(f"{API_BASE_URL}/pedidos", headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def crear_pedido(data):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.post(f"{API_BASE_URL}/pedidos", json=data, headers=headers)
    return response.ok

def obtener_pedido(pedido_id):
    response = requests.get(f"{API_BASE_URL}/pedidos/{pedido_id}")
    if response.status_code == 200:
        return response.json()
    return None

def actualizar_pedido(pedido_id, data):
    response = requests.put(f"{API_BASE_URL}/pedidos/{pedido_id}", json=data)
    return response.ok

def eliminar_pedido(pedido_id):
    response = requests.delete(f"{API_BASE_URL}/pedidos/{pedido_id}")
    return response.ok

# Detalles de pedidos
def obtener_detalles_pedido():
    response = requests.get(f"{API_BASE_URL}/detallepedidos")
    if response.status_code == 200:
        return response.json()
    return []

def crear_detalle_pedido(data):
    response = requests.post(f"{API_BASE_URL}/detallepedidos", json=data)
    return response.ok

def obtener_detalle_pedido(detalle_id):
    response = requests.get(f"{API_BASE_URL}/detallepedidos/{detalle_id}")
    if response.status_code == 200:
        return response.json()
    return None

# Estados de pedidos
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