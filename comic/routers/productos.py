from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from modelsPydantic import modeloProducto
from DB.conexion import Session
from models.modelsDB import Productos

routerProductos = APIRouter()

# Obtener todos los productos
@routerProductos.get("/productos", response_model=list[modeloProducto], tags=["Productos"])
def obtener_productos():
    db = Session()
    try:
        resultados = db.query(Productos).all()
        return JSONResponse(content=jsonable_encoder(resultados))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al consultar productos", "excepción": str(e)})
    finally:
        db.close()

# Obtener producto por ID
@routerProductos.get("/productos/{id}", response_model=modeloProducto, tags=["Productos"])
def obtener_producto(id: int):
    db = Session()
    try:
        producto = db.query(Productos).filter(Productos.id == id).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al buscar producto", "excepción": str(e)})
    finally:
        db.close()

# Crear producto
@routerProductos.post("/productos", response_model=modeloProducto, tags=["Productos"])
def agregar_producto(producto: modeloProducto):
    db = Session()
    try:
        nuevo_producto = Productos(**producto.model_dump())
        db.add(nuevo_producto)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Producto guardado correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al guardar producto", "excepción": str(e)})
    finally:
        db.close()

# Actualizar producto
@routerProductos.put("/productos/{id}", response_model=modeloProducto, tags=["Productos"])
def actualizar_producto(id: int, producto_actualizado: modeloProducto):
    db = Session()
    try:
        producto = db.query(Productos).filter(Productos.id == id).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        for key, value in producto_actualizado.model_dump().items():
            setattr(producto, key, value)

        db.commit()
        db.refresh(producto)
        return producto
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al actualizar producto", "excepción": str(e)})
    finally:
        db.close()

# Eliminar producto
@routerProductos.delete("/productos/{id}", tags=["Productos"])
def eliminar_producto(id: int):
    db = Session()
    try:
        producto = db.query(Productos).filter(Productos.id == id).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        db.delete(producto)
        db.commit()
        return JSONResponse(content={"message": "Producto eliminado correctamente"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al eliminar producto", "excepción": str(e)})
    finally:
        db.close()
        