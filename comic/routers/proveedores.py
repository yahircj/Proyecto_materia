from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from modelsPydantic import modeloProveedor
from DB.conexion import Session
from models.modelsDB import Proveedores

routerProveedores = APIRouter()

# Obtener todos los proveedores
@routerProveedores.get("/proveedores", response_model=list[modeloProveedor], tags=["Proveedores"])
def obtener_proveedores():
    db = Session()
    try:
        resultados = db.query(Proveedores).all()
        return JSONResponse(content=jsonable_encoder(resultados))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al consultar proveedores", "excepción": str(e)})
    finally:
        db.close()

# Obtener proveedor por ID
@routerProveedores.get("/proveedores/{id}", response_model=modeloProveedor, tags=["Proveedores"])
def obtener_proveedor(id: int):
    db = Session()
    try:
        proveedor = db.query(Proveedores).filter(Proveedores.id == id).first()
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
        return proveedor
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al buscar proveedor", "excepción": str(e)})
    finally:
        db.close()

# Agregar proveedor
@routerProveedores.post("/proveedores", response_model=modeloProveedor, tags=["Proveedores"])
def agregar_proveedor(proveedor: modeloProveedor):
    db = Session()
    try:
        nuevo_proveedor = Proveedores(**proveedor.model_dump())
        db.add(nuevo_proveedor)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Proveedor guardado correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al guardar proveedor", "excepción": str(e)})
    finally:
        db.close()

# Actualizar proveedor
@routerProveedores.put("/proveedores/{id}", response_model=modeloProveedor, tags=["Proveedores"])
def actualizar_proveedor(id: int, proveedor_actualizado: modeloProveedor):
    db = Session()
    try:
        proveedor = db.query(Proveedores).filter(Proveedores.id == id).first()
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")

        for key, value in proveedor_actualizado.model_dump().items():
            setattr(proveedor, key, value)

        db.commit()
        db.refresh(proveedor)
        return proveedor
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al actualizar proveedor", "excepción": str(e)})
    finally:
        db.close()

# Eliminar proveedor
@routerProveedores.delete("/proveedores/{id}", tags=["Proveedores"])
def eliminar_proveedor(id: int):
    db = Session()
    try:
        proveedor = db.query(Proveedores).filter(Proveedores.id == id).first()
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")

        db.delete(proveedor)
        db.commit()
        return JSONResponse(content={"message": "Proveedor eliminado correctamente"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al eliminar proveedor", "excepción": str(e)})
    finally:
        db.close()