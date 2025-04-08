from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from modelsPydantic import modeloEstadoPedido
from DB.conexion import Session
from models.modelsDB import EstadosPedidos

routerEstadosPedidos = APIRouter()

# Obtener todos los estados de pedido
@routerEstadosPedidos.get("/estadospedidos", response_model=list[modeloEstadoPedido], tags=["EstadosPedidos"])
def obtener_estados():
    db = Session()
    try:
        resultados = db.query(EstadosPedidos).all()
        return JSONResponse(content=jsonable_encoder(resultados))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al consultar estados", "excepción": str(e)})
    finally:
        db.close()

# Obtener un estado por ID
@routerEstadosPedidos.get("/estadospedidos/{id}", response_model=modeloEstadoPedido, tags=["EstadosPedidos"])
def obtener_estado(id: int):
    db = Session()
    try:
        estado = db.query(EstadosPedidos).filter(EstadosPedidos.id == id).first()
        if not estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado")
        return estado
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al consultar estado", "excepción": str(e)})
    finally:
        db.close()