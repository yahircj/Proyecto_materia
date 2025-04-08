from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from modelsPydantic import modeloDetallePedido
from DB.conexion import Session
from models.modelsDB import DetallesPedidos

routerDetallePedidos = APIRouter()

# Obtener todos los detalles
@routerDetallePedidos.get("/detallepedidos", response_model=list[modeloDetallePedido], tags=["DetallesPedidos"])
def obtener_detalles():
    db = Session()
    try:
        resultados = db.query(DetallesPedidos).all()
        return JSONResponse(content=jsonable_encoder(resultados))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al consultar detalles", "excepción": str(e)})
    finally:
        db.close()

# Obtener detalle por ID
@routerDetallePedidos.get("/detallepedidos/{id}", response_model=modeloDetallePedido, tags=["DetallesPedidos"])
def obtener_detalle(id: int):
    db = Session()
    try:
        detalle = db.query(DetallesPedidos).filter(DetallesPedidos.id == id).first()
        if not detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        return detalle
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al buscar detalle", "excepción": str(e)})
    finally:
        db.close()

# Crear detalle
@routerDetallePedidos.post("/detallepedidos", response_model=modeloDetallePedido, tags=["DetallesPedidos"])
def agregar_detalle(detalle: modeloDetallePedido):
    db = Session()
    try:
        nuevo_detalle = DetallesPedidos(**detalle.model_dump())
        db.add(nuevo_detalle)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Detalle guardado correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al guardar detalle", "excepción": str(e)})
    finally:
        db.close()

# Actualizar detalle
@routerDetallePedidos.put("/detallepedidos/{id}", response_model=modeloDetallePedido, tags=["DetallesPedidos"])
def actualizar_detalle(id: int, detalle_actualizado: modeloDetallePedido):
    db = Session()
    try:
        detalle = db.query(DetallesPedidos).filter(DetallesPedidos.id == id).first()
        if not detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")

        for key, value in detalle_actualizado.model_dump().items():
            setattr(detalle, key, value)

        db.commit()
        db.refresh(detalle)
        return detalle
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al actualizar detalle", "excepción": str(e)})
    finally:
        db.close()

# Eliminar detalle
@routerDetallePedidos.delete("/detallepedidos/{id}", tags=["DetallesPedidos"])
def eliminar_detalle(id: int):
    db = Session()
    try:
        detalle = db.query(DetallesPedidos).filter(DetallesPedidos.id == id).first()
        if not detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")

        db.delete(detalle)
        db.commit()
        return JSONResponse(content={"message": "Detalle eliminado correctamente"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al eliminar detalle", "excepción": str(e)})
    finally:
        db.close()