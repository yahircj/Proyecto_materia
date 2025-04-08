from fastapi import APIRouter
from fastapi.responses import JSONResponse
from modelsPydantic import modeloAuth
from genToken import createToken

routerAuth = APIRouter()

# Ruta de autenticación
@routerAuth.post('/auth/', tags=['Autenticación'])
def login(credenciales: modeloAuth):
    if credenciales.email == "admin@comic.com" and credenciales.passw == "12345678":
        token = createToken(credenciales.model_dump())
        return JSONResponse(content={"token": token})
    else:
        return JSONResponse(status_code=401, content={"mensaje": "Credenciales inválidas"})