from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from modelsPydantic import modeloUsuario
from DB.conexion import Session
from models.modelsDB import User

routerUsuario = APIRouter()

# Obtener todos los usuarios
@routerUsuario.get("/usuarios", response_model=list[modeloUsuario], tags=["Usuarios"])
def obtener_usuarios():
    db = Session()
    try:
        resultados = db.query(User).all()
        return JSONResponse(content=jsonable_encoder(resultados))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al consultar usuarios", "excepción": str(e)})
    finally:
        db.close()

# Obtener usuario por ID
@routerUsuario.get("/usuarios/{id}", response_model=modeloUsuario, tags=["Usuarios"])
def obtener_usuario(id: int):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al buscar usuario", "excepción": str(e)})
    finally:
        db.close()

# Agregar usuario
@routerUsuario.post("/usuarios", response_model=modeloUsuario, tags=["Usuarios"])
def agregar_usuario(usuario: modeloUsuario):
    db = Session()
    try:
        nuevo_usuario = User(**usuario.model_dump())
        db.add(nuevo_usuario)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Usuario guardado correctamente"})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al guardar usuario", "excepción": str(e)})
    finally:
        db.close()

# Actualizar usuario
@routerUsuario.put("/usuarios/{id}", response_model=modeloUsuario, tags=["Usuarios"])
def actualizar_usuario(id: int, usuario_actualizado: modeloUsuario):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        for key, value in usuario_actualizado.model_dump().items():
            setattr(usuario, key, value)

        db.commit()
        db.refresh(usuario)
        return usuario
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al actualizar usuario", "excepción": str(e)})
    finally:
        db.close()

# Eliminar usuario
@routerUsuario.delete("/usuarios/{id}", tags=["Usuarios"])
def eliminar_usuario(id: int):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        db.delete(usuario)
        db.commit()
        return JSONResponse(content={"message": "Usuario eliminado correctamente"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al eliminar usuario", "excepción": str(e)})
    finally:
        db.close()