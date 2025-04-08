from flask import Flask, render_template, request, redirect, url_for
from utils.api_client import (
    #clientes
    obtener_clientes, crear_cliente, obtener_cliente,
    actualizar_cliente, eliminar_cliente, 
    #productos
    obtener_productos, 
    crear_producto, obtener_producto, 
    actualizar_producto, eliminar_producto,
    # proveedores
    obtener_proveedores, crear_proveedor, obtener_proveedor,
    actualizar_proveedor, eliminar_proveedor,
        # Pedidos
    obtener_pedidos, crear_pedido, obtener_pedido,
    actualizar_pedido, eliminar_pedido,
    # Detalles de pedidos
    obtener_detalles_pedido, crear_detalle_pedido, obtener_detalle_pedido,
    # Estados de pedidos
    obtener_estados_pedido, obtener_estado_pedido
)


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home_admin.html")

#Clientes
@app.route("/clientes")
def clientes():
    lista_clientes = obtener_clientes()
    return render_template("clientes.html", clientes=lista_clientes)

@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():
    if request.method == "POST":
        data = {
            "nombre": request.form["nombre"],
            "email": request.form["email"],
            "telefono": request.form["telefono"],
            "direccion": request.form["direccion"],
            "cliente_frecuente": "cliente_frecuente" in request.form
        }
        crear_cliente(data)
        return redirect(url_for("clientes"))
    return render_template("cliente_form.html", cliente=None)

@app.route("/clientes/editar/<int:cliente_id>", methods=["GET", "POST"])
def editar_cliente(cliente_id):
    cliente = obtener_cliente(cliente_id)
    if request.method == "POST":
        data = {
            "nombre": request.form["nombre"],
            "email": request.form["email"],
            "telefono": request.form["telefono"],
            "direccion": request.form["direccion"],
            "cliente_frecuente": "cliente_frecuente" in request.form
        }
        actualizar_cliente(cliente_id, data)
        return redirect(url_for("clientes"))
    return render_template("cliente_form.html", cliente=cliente)


@app.route("/clientes/eliminar/<int:cliente_id>")
def eliminar_cliente_view(cliente_id):
    eliminar_cliente(cliente_id)
    return redirect(url_for("clientes"))

#productos
# Productos
@app.route("/productos")
def productos():
    lista_productos = obtener_productos()
    return render_template("productos.html", productos=lista_productos)

@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    if request.method == "POST":
        data = {
            "precio": float(request.form["precio"]),
            "categoria_id": int(request.form["categoria_id"]),
            "editorial_id": int(request.form["editorial_id"]),
            "nombre": request.form["nombre"],
            "descripcion": request.form["descripcion"],
            "stock": int(request.form["stock"]),
            "proveedor_id": int(request.form["proveedor_id"])
        }
        crear_producto(data)
        return redirect(url_for("productos"))
    return render_template("producto_form.html", producto=None)

@app.route("/productos/editar/<int:producto_id>", methods=["GET", "POST"])
def editar_producto(producto_id):
    producto = obtener_producto(producto_id)
    if request.method == "POST":
        data = {
            "precio": float(request.form["precio"]),
            "categoria_id": int(request.form["categoria_id"]),
            "editorial_id": int(request.form["editorial_id"]),
            "nombre": request.form["nombre"],
            "descripcion": request.form["descripcion"],
            "stock": int(request.form["stock"]),
            "proveedor_id": int(request.form["proveedor_id"])
        }
        actualizar_producto(producto_id, data)
        return redirect(url_for("productos"))
    return render_template("producto_form.html", producto=producto)

@app.route("/productos/eliminar/<int:producto_id>")
def eliminar_producto_view(producto_id):
    eliminar_producto(producto_id)
    return redirect(url_for("productos"))

# Proveedores
@app.route("/proveedores")
def proveedores():
    lista_proveedores = obtener_proveedores()
    return render_template("proveedores.html", proveedores=lista_proveedores)

@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():
    if request.method == "POST":
        data = {
            "nombre": request.form["nombre"],
            "contacto": request.form["contacto"],
            "telefono": request.form["telefono"],
            "direccion": request.form["direccion"],
        }
        crear_proveedor(data)
        return redirect(url_for("proveedores"))
    return render_template("proveedor_form.html", proveedor=None)

@app.route("/proveedores/editar/<int:proveedor_id>", methods=["GET", "POST"])
def editar_proveedor(proveedor_id):
    proveedor = obtener_proveedor(proveedor_id)
    if request.method == "POST":
        data = {
            "nombre": request.form["nombre"],
            "contacto": request.form["contacto"],
            "telefono": request.form["telefono"],
            "direccion": request.form["direccion"],
        }
        actualizar_proveedor(proveedor_id, data)
        return redirect(url_for("proveedores"))
    return render_template("proveedor_form.html", proveedor=proveedor)

@app.route("/proveedores/eliminar/<int:proveedor_id>")
def eliminar_proveedor_view(proveedor_id):
    eliminar_proveedor(proveedor_id)
    return redirect(url_for("proveedores"))

# Pedidos
@app.route("/pedidos")
def pedidos():
    lista_pedidos = obtener_pedidos()
    return render_template("pedidos.html", pedidos=lista_pedidos)

@app.route("/pedidos/nuevo", methods=["GET", "POST"])
def nuevo_pedido():
    if request.method == "POST":
        # Crear el pedido principal
        pedido_data = {
            "cliente_id": int(request.form["cliente_id"]),
            "fecha_pedido": request.form["fecha_pedido"],
            "estado_id": 1,  # Estado inicial (pendiente)
            "total": float(request.form["total"])
        }
        
        # Crear el pedido en la API
        exito = crear_pedido(pedido_data)
        
    
    # Para el formulario necesitamos la lista de clientes
    clientes = obtener_clientes()
    return render_template("pedido_form.html", pedido=None, clientes=clientes)

@app.route("/pedidos/detalle/<int:pedido_id>")
def detalle_pedido(pedido_id):
    pedido = obtener_pedido(pedido_id)
    # Obtener todos los detalles de pedidos y filtrar los que pertenecen a este pedido
    todos_detalles = obtener_detalles_pedido()
    detalles_pedido = [detalle for detalle in todos_detalles if detalle.get("pedido_id") == pedido_id]
    
    # Obtener información completa de productos para mostrar nombres
    productos = obtener_productos()
    productos_dict = {producto["id"]: producto for producto in productos}
    
    # Obtener información del estado
    estados = obtener_estados_pedido()
    estados_dict = {estado["id"]: estado for estado in estados}
    
    return render_template(
        "pedido_detalle.html", 
        pedido=pedido, 
        detalles=detalles_pedido,
        productos=productos_dict,
        estados=estados_dict
    )

@app.route("/pedidos/editar_estado/<int:pedido_id>", methods=["GET", "POST"])
def editar_estado_pedido(pedido_id):
    pedido = obtener_pedido(pedido_id)
    estados = obtener_estados_pedido()
    
    if request.method == "POST":
        nuevo_estado_id = int(request.form["estado_id"])
        pedido_actualizado = pedido.copy()
        pedido_actualizado["estado_id"] = nuevo_estado_id
        
        exito = actualizar_pedido(pedido_id, pedido_actualizado)

    
    return render_template("pedido_estado_form.html", pedido=pedido, estados=estados)

@app.route("/pedidos/agregar_producto/<int:pedido_id>", methods=["GET", "POST"])
def agregar_producto_pedido(pedido_id):
    pedido = obtener_pedido(pedido_id)
    productos = obtener_productos()
    
    if request.method == "POST":
        producto_id = int(request.form["producto_id"])
        cantidad = int(request.form["cantidad"])
        
        # Obtener el producto para calcular subtotal y verificar stock
        producto = obtener_producto(producto_id)
        
        if producto and producto["stock"] >= cantidad:
            subtotal = producto["precio"] * cantidad
            
            # Crear detalle de pedido
            detalle_data = {
                "pedido_id": pedido_id,
                "producto_id": producto_id,
                "cantidad": cantidad,
                "precio_unitario": producto["precio"],
                "subtotal": subtotal
            }
            
            exito_detalle = crear_detalle_pedido(detalle_data)
            
            if exito_detalle:
                # Actualizar el stock del producto
                producto_actualizado = producto.copy()
                producto_actualizado["stock"] = producto["stock"] - cantidad
                
                # Actualizar el total del pedido
                pedido_actualizado = pedido.copy()
                pedido_actualizado["total"] = pedido["total"] + subtotal
                
                exito_producto = actualizar_producto(producto_id, producto_actualizado)
                exito_pedido = actualizar_pedido(pedido_id, pedido_actualizado)
                
    
    # Filtrar productos con stock disponible
    productos_disponibles = [p for p in productos if p["stock"] > 0]
    
    return render_template(
        "pedido_agregar_producto.html", 
        pedido=pedido, 
        productos=productos_disponibles
    )

@app.route("/pedidos/eliminar/<int:pedido_id>")
def eliminar_pedido_view(pedido_id):
    eliminar_pedido(pedido_id)
    return redirect(url_for("pedidos"))

if __name__ == "__main__":
    app.run(debug=True)
