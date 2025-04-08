from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from genToken import validateToken

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        # Llama al comportamiento por defecto (lee el Authorization header)
        auth = await super().__call__(request)

        # Valida el token recibido
        data = validateToken(auth.credentials)

        # Asegura que sea un diccionario válido
        if not isinstance(data, dict):
            raise HTTPException(status_code=401, detail="Token inválido")

        # Verifica que el usuario tenga permiso (aquí puedes personalizar más adelante)
        if data.get('email') != 'admin@comic.com':
            raise HTTPException(status_code=403, detail="Credenciales no válidas")