from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelsPydantic import modeloPromociones
from sqlalchemy import select
from sqlalchemy.inspection import inspect


from db.conexion import Session
from models.modelsDB import Productos, Promociones, TiposPromociones

routerPromociones = APIRouter()

def as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

# Consultar promociones
@routerPromociones.get("/promociones", tags=["Promociones"])
def obtener_promociones():
    db = Session()
    try:
        query = select(Productos, Promociones, TiposPromociones.detalle_promocion).join(Promociones, Promociones.producto_id == Productos.id).join(TiposPromociones, Promociones.promocion_id == TiposPromociones.id)
        resultados = db.execute(query).all()
        data = [
            {
                "producto": as_dict(producto),
                "promocion": as_dict(promocion),
                "detalle_promocion": detalle
            }
            for producto, promocion, detalle in resultados
        ]
        return JSONResponse(content=jsonable_encoder(data))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al consultar promoción", "excepción": str(e)})
    finally:
        db.close()

# Agregar promocion
@routerPromociones.post("/promociones", tags=["Promociones"])
def agregar_promociones(promocion: modeloPromociones):
    db = Session()
    try:
        nueva_promocion = Promociones(**promocion.model_dump())
        db.add(nueva_promocion)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Promoción guardado correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al guardar promoción", "excepción": str(e)})
    finally:
        db.close()

# Actualizar promocion
@routerPromociones.put("/promociones/{id}", tags=["Promociones"])
def actualizar_promocion(id: int, promocion_actualizada: modeloPromociones):
    db = Session()
    try:
        promocion = db.query(Promociones).filter(Promociones.id == id).first()
        if not promocion:
            raise HTTPException(status_code=404, detail="Promoción no encontrado")

        for key, value in promocion_actualizada.model_dump().items():
            setattr(promocion, key, value)

        db.commit()
        db.refresh(promocion)
        return promocion
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al actualizar promoción", "excepción": str(e)})
    finally:
        db.close()

@routerPromociones.delete("/promociones/{id}", tags=["Promociones"])
def eliminar_promocion(id:int):
    db = Session()
    try:
        promocion = db.query(Promociones).filter(Promociones.id == id).first()
        if not promocion:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        db.delete(promocion)
        db.commit()
        return JSONResponse(content={"message": "Producto eliminado correctamente"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al eliminar promoción", "excepción": str(e)})
    finally:
        db.close()