from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import obtener_db
from app.infraestructura.auth.gestor_tokens import verificar_token
from app.infraestructura.repositorios.repositorio_usuario_sqlalchemy import RepositorioUsuarioSQLAlchemy
from app.infraestructura.auth.hash_contrasena import verificar_contrasena
from app.dominio.usuario.excepciones import CredencialesInvalidas, SinPermisos

seguridad = HTTPBearer()


def obtener_repositorio_usuario(db: Session = Depends(obtener_db)):
    return RepositorioUsuarioSQLAlchemy(db)


async def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(seguridad),
    db: Session = Depends(obtener_db),
):
    token = credenciales.credentials
    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o expirado",
        )

    repositorio = RepositorioUsuarioSQLAlchemy(db)
    usuario = repositorio.obtener_por_id(int(payload["sub"]))
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )
    return usuario


ROLES_ADMIN = ("admin", "presidente")


async def requerir_admin(usuario_actual=Depends(obtener_usuario_actual)):
    if usuario_actual.rol.value not in ROLES_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador",
        )
    return usuario_actual
