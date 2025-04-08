from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from modelsPydantic import modeloCliente
from DB.conexion import Session
from models.modelsDB import Clientes

routerClientes = APIRouter()

# Obtener todos los clientes
@routerClientes.get("/clientes", response_model=list[modeloCliente], tags=["Clientes"])
def obtener_clientes():
    db = Session()
    try:
        resultados = db.query(Clientes).all()
        return JSONResponse(content=jsonable_encoder(resultados))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al consultar clientes", "excepción": str(e)})
    finally:
        db.close()

# Obtener un cliente por ID
@routerClientes.get("/clientes/{id}", response_model=modeloCliente, tags=["Clientes"])
def obtener_cliente(id: int):
    db = Session()
    try:
        cliente = db.query(Clientes).filter(Clientes.id == id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return cliente
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al buscar cliente", "excepción": str(e)})
    finally:
        db.close()

# Agregar un nuevo cliente
@routerClientes.post("/clientes", response_model=modeloCliente, tags=["Clientes"])
def agregar_cliente(cliente: modeloCliente):
    db = Session()
    try:
        nuevo_cliente = Clientes(**cliente.model_dump())
        db.add(nuevo_cliente)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Cliente guardado correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al guardar cliente", "excepción": str(e)})
    finally:
        db.close()

# Actualizar un cliente
@routerClientes.put("/clientes/{id}", response_model=modeloCliente, tags=["Clientes"])
def actualizar_cliente(id: int, cliente_actualizado: modeloCliente):
    db = Session()
    try:
        cliente = db.query(Clientes).filter(Clientes.id == id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        for key, value in cliente_actualizado.model_dump().items():
            setattr(cliente, key, value)

        db.commit()
        db.refresh(cliente)
        return cliente
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al actualizar cliente", "excepción": str(e)})
    finally:
        db.close()

# Eliminar un cliente
@routerClientes.delete("/clientes/{id}", tags=["Clientes"])
def eliminar_cliente(id: int):
    db = Session()
    try:
        cliente = db.query(Clientes).filter(Clientes.id == id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        db.delete(cliente)
        db.commit()
        return JSONResponse(content={"message": "Cliente eliminado correctamente"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al eliminar cliente", "excepción": str(e)})
    finally:
        db.close()