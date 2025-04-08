from fastapi import APIRouter, HTTPException, Depends
from middlewares import BearerJWT  
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from modelsPydantic import modeloPedido
from DB.conexion import Session
from models.modelsDB import Pedidos

routerPedidos = APIRouter(
    dependencies=[Depends(BearerJWT())],  
)

# Obtener todos los pedidos
@routerPedidos.get("/pedidos", response_model=list[modeloPedido], tags=["Pedidos"])
def obtener_pedidos():
    db = Session()
    try:
        resultados = db.query(Pedidos).all()
        return JSONResponse(content=jsonable_encoder(resultados))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al consultar pedidos", "excepción": str(e)})
    finally:
        db.close()

# Obtener un pedido por ID
@routerPedidos.get("/pedidos/{id}", response_model=modeloPedido, tags=["Pedidos"])
def obtener_pedido(id: int):
    db = Session()
    try:
        pedido = db.query(Pedidos).filter(Pedidos.id == id).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return pedido
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al buscar pedido", "excepción": str(e)})
    finally:
        db.close()

# Crear un pedido
@routerPedidos.post("/pedidos", response_model=modeloPedido, tags=["Pedidos"])
def agregar_pedido(pedido: modeloPedido):
    db = Session()
    try:
        nuevo_pedido = Pedidos(**pedido.model_dump())
        db.add(nuevo_pedido)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Pedido guardado correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al guardar pedido", "excepción": str(e)})
    finally:
        db.close()

# Actualizar pedido
@routerPedidos.put("/pedidos/{id}", response_model=modeloPedido, tags=["Pedidos"])
def actualizar_pedido(id: int, pedido_actualizado: modeloPedido):
    db = Session()
    try:
        pedido = db.query(Pedidos).filter(Pedidos.id == id).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        for key, value in pedido_actualizado.model_dump().items():
            setattr(pedido, key, value)

        db.commit()
        db.refresh(pedido)
        return pedido
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al actualizar pedido", "excepción": str(e)})
    finally:
        db.close()

# Eliminar pedido
@routerPedidos.delete("/pedidos/{id}", tags=["Pedidos"])
def eliminar_pedido(id: int):
    db = Session()
    try:
        pedido = db.query(Pedidos).filter(Pedidos.id == id).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        db.delete(pedido)
        db.commit()
        return JSONResponse(content={"message": "Pedido eliminado correctamente"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al eliminar pedido", "excepción": str(e)})
    finally:
        db.close()