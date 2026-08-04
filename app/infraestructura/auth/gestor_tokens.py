from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import configuracion


def crear_token_acceso(datos: dict, tiempo_expiracion: timedelta = None):
    datos_a_cifrar = datos.copy()
    if tiempo_expiracion:
        fecha_expiracion = datetime.utcnow() + tiempo_expiracion
    else:
        fecha_expiracion = datetime.utcnow() + timedelta(
            minutes=configuracion.MINUTOS_EXPIRACION_TOKEN
        )
    datos_a_cifrar.update({"exp": fecha_expiracion})
    token_jwt = jwt.encode(
        datos_a_cifrar,
        configuracion.CLAVE_SECRETA,
        algorithm=configuracion.ALGORITMO,
    )
    return token_jwt


def verificar_token(token: str):
    try:
        payload = jwt.decode(
            token,
            configuracion.CLAVE_SECRETA,
            algorithms=[configuracion.ALGORITMO],
        )
        return payload
    except JWTError:
        return None
