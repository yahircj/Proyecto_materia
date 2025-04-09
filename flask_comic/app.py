from flask import Flask, render_template, request, redirect, url_for, session
from utils.api_client import (
    # Clientes
    obtener_clientes, crear_cliente, obtener_cliente,
    actualizar_cliente, eliminar_cliente, 
    # Productos
    obtener_productos, 
    crear_producto, obtener_producto, 
    actualizar_producto, eliminar_producto,
    # Proveedores
    obtener_proveedores, crear_proveedor, obtener_proveedor,
    actualizar_proveedor, eliminar_proveedor,
    # Pedidos
    obtener_pedidos, crear_pedido, obtener_pedido,
    actualizar_pedido, eliminar_pedido,
    # Detalles de pedidos
    obtener_detalles_pedido, crear_detalle_pedido, obtener_detalle_pedido,
    # Estados de pedidos
    obtener_estados_pedido, obtener_estado_pedido,
    # Abastecimientos
    obtener_abastecimientos, crear_abastecimiento,
    # Promociones
    obtener_promociones
)

app = Flask(__name__)
app.secret_key = 'clave_secreta_admin_segura'  # Necesario para usar sesiones

# 🟢 LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Validación estática para un solo administrador
        if email == "admin@comic.com" and password == "admin123":
            session["usuario"] = email
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Correo o contraseña incorrectos")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

# 🟢 DASHBOARD
@app.route("/")
def home():
    productos = obtener_productos()
    productos_bajo_stock = [p for p in productos if p["stock"] <= 5]
    return render_template("home_admin.html", productos_bajo_stock=productos_bajo_stock)

# Clientes
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
    clientes = obtener_clientes()
    productos = obtener_productos()

    if request.method == "POST":
        cliente_id = int(request.form["cliente_id"])
        productos_ids = request.form.getlist("producto_id")
        cantidades = request.form.getlist("cantidad")

        total_pedido = 0
        detalles = []

        for producto_id, cantidad in zip(productos_ids, cantidades):
            cantidad = int(cantidad)
            if cantidad > 0:
                producto = obtener_producto(int(producto_id))
                subtotal = producto["precio"] * cantidad
                total_pedido += subtotal

                detalles.append({
                    "producto_id": int(producto_id),
                    "cantidad": cantidad,
                    "precio_unitario": producto["precio"],
                    "subtotal": subtotal
                })

        pedido_data = {
            "cliente_id": cliente_id,
            "estado_id": 1,
            "total": total_pedido
        }
        pedido = crear_pedido(pedido_data)

        for detalle in detalles:
            detalle_data = detalle.copy()
            detalle_data["pedido_id"] = pedido["id"]
            crear_detalle_pedido(detalle_data)

            producto = obtener_producto(detalle["producto_id"])
            producto["stock"] -= detalle["cantidad"]
            actualizar_producto(detalle["producto_id"], producto)

        return redirect(url_for("pedidos"))

    return render_template("pedido_form.html", pedido=None, clientes=clientes, productos=productos)

@app.route("/pedidos/detalle/<int:pedido_id>")
def detalle_pedido(pedido_id):
    pedido = obtener_pedido(pedido_id)
    todos_detalles = obtener_detalles_pedido()
    detalles_pedido = [detalle for detalle in todos_detalles if detalle.get("pedido_id") == pedido_id]
    productos = obtener_productos()
    productos_dict = {producto["id"]: producto for producto in productos}
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
        actualizar_pedido(pedido_id, pedido_actualizado)

    return render_template("pedido_estado_form.html", pedido=pedido, estados=estados)

@app.route("/pedidos/eliminar/<int:pedido_id>")
def eliminar_pedido_view(pedido_id):
    eliminar_pedido(pedido_id)
    return redirect(url_for("pedidos"))

# Abastecimientos
@app.route("/abastecimientos")
def listar_abastecimientos():
    abastecimientos = obtener_abastecimientos()
    productos = obtener_productos()
    proveedores = obtener_proveedores()

    productos_dict = {p["id"]: p["nombre"] for p in productos}
    proveedores_dict = {p["id"]: p["nombre"] for p in proveedores}

    return render_template("abastecimientos.html", 
        abastecimientos=abastecimientos,
        productos=productos_dict,
        proveedores=proveedores_dict
    )

@app.route("/abastecimientos/nuevo", methods=["GET", "POST"])
def nuevo_abastecimiento():
    proveedores = obtener_proveedores()
    productos = obtener_productos()

    if request.method == "POST":
        producto_id = int(request.form["producto_id"])
        proveedor_id = int(request.form["proveedor_id"])
        cantidad = int(request.form["cantidad"])
        fecha = request.form["fecha_abastecimiento"]

        data = {
            "producto_id": producto_id,
            "proveedor_id": proveedor_id,
            "fecha_abastecimiento": fecha
        }
        crear_abastecimiento(data)

        producto = obtener_producto(producto_id)
        producto["stock"] += cantidad
        actualizar_producto(producto_id, producto)

        return redirect(url_for("productos"))

    return render_template("abastecimiento_form.html", proveedores=proveedores, productos=productos)

# Promociones
@app.route("/promociones")
def promociones():
    clientes = obtener_clientes()
    promociones = obtener_promociones()
    clientes_frecuentes = [c for c in clientes if c.get("cliente_frecuente")]
    return render_template("promociones.html", promociones=promociones, clientes=clientes_frecuentes)

if __name__ == "__main__":
    app.run(debug=True)