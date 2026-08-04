from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from app.presentacion.dependencias import obtener_usuario_actual, requerir_admin
from app.infraestructura.repositorios.repositorio_permiso_sqlalchemy import RepositorioPermisoSQLAlchemy
from app.database import obtener_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/permisos", tags=["Permisos"])


class ModuloRespuesta(BaseModel):
    id: int
    codigo: str
    nombre: str


class RolPermisosRespuesta(BaseModel):
    rol: str
    modulos: List[str]


class ActualizarRolPermisos(BaseModel):
    modulos: List[str]


ROLES_DISPONIBLES = ["admin", "presidente", "tesorera", "secretario", "propietario", "consejo"]


@router.get("")
def obtener_permisos(
    usuario_actual=Depends(obtener_usuario_actual),
    db: Session = Depends(obtener_db),
):
    repositorio = RepositorioPermisoSQLAlchemy(db)
    rol = usuario_actual.rol if isinstance(usuario_actual.rol, str) else usuario_actual.rol.value
    modulos = repositorio.obtener_modulos_por_rol(rol)
    return {"rol": rol, "modulos": modulos}


@router.get("/modulos")
def listar_modulos(
    usuario_actual=Depends(requerir_admin),
    db: Session = Depends(obtener_db),
):
    repositorio = RepositorioPermisoSQLAlchemy(db)
    return repositorio.obtener_todos_los_modulos()


@router.get("/roles")
def listar_roles_permisos(
    usuario_actual=Depends(requerir_admin),
    db: Session = Depends(obtener_db),
):
    repositorio = RepositorioPermisoSQLAlchemy(db)
    resultado = []
    for rol in ROLES_DISPONIBLES:
        modulos = repositorio.obtener_modulos_por_rol(rol)
        resultado.append({"rol": rol, "modulos": modulos})
    return resultado


@router.get("/roles/{rol}")
def obtener_rol_permisos(
    rol: str,
    usuario_actual=Depends(requerir_admin),
    db: Session = Depends(obtener_db),
):
    if rol not in ROLES_DISPONIBLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rol no valido: {rol}",
        )
    repositorio = RepositorioPermisoSQLAlchemy(db)
    modulos = repositorio.obtener_modulos_por_rol(rol)
    return {"rol": rol, "modulos": modulos}


@router.put("/roles/{rol}")
def actualizar_rol_permisos(
    rol: str,
    body: ActualizarRolPermisos,
    usuario_actual=Depends(requerir_admin),
    db: Session = Depends(obtener_db),
):
    if rol not in ROLES_DISPONIBLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rol no valido: {rol}",
        )
    repositorio = RepositorioPermisoSQLAlchemy(db)
    repositorio.asignar_modulos_a_rol(rol, body.modulos)
    return {"mensaje": f"Permisos actualizados para rol {rol}", "modulos": body.modulos}
