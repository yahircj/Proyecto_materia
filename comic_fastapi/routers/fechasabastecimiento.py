from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from modelsPydantic import modeloFechaAbastecimiento
from DB.conexion import Session
from models.modelsDB import FechasAbastecimiento

routerFechasAbastecimiento = APIRouter()

# Obtener todas las fechas
@routerFechasAbastecimiento.get("/fechasabastecimiento", response_model=list[modeloFechaAbastecimiento], tags=["FechasAbastecimiento"])
def obtener_fechas():
    db = Session()
    try:
        resultados = db.query(FechasAbastecimiento).all()
        return JSONResponse(content=jsonable_encoder(resultados))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al consultar fechas", "excepción": str(e)})
    finally:
        db.close()

# Agregar una nueva fecha
@routerFechasAbastecimiento.post("/fechasabastecimiento", response_model=modeloFechaAbastecimiento, tags=["FechasAbastecimiento"])
def agregar_fecha(fecha: modeloFechaAbastecimiento):
    db = Session()
    try:
        nueva_fecha = FechasAbastecimiento(**fecha.model_dump())
        db.add(nueva_fecha)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Fecha registrada correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al guardar la fecha", "excepción": str(e)})
    finally:
        db.close()