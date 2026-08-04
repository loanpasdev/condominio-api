from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.propietario import (
    SolicitudCrearPropietario, SolicitudActualizarPropietario,
    RespuestaPropietario, RespuestaListaPropietarios,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_propietario_sqlalchemy import RepositorioPropietarioSQLAlchemy
from app.aplicacion.caso_uso.propietarios import (
    CrearPropietario, ListarPropietarios, ObtenerPropietario, ActualizarPropietario, EliminarPropietario,
)
from app.dominio.propietario.excepciones import PropietarioNoExiste, PropietarioYaExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/propietarios", tags=["Propietarios"])


@router.get("", response_model=RespuestaListaPropietarios)
def listar(
    buscar: str = Query(None),
    condominio_id: int = Query(None),
    estado: bool = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=100),
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioPropietarioSQLAlchemy(db)
    caso_uso = ListarPropietarios(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, condominio_id=condominio_id, estado=estado, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaPropietarios(
        propietarios=items, total=total, pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.get("/{id}", response_model=RespuestaPropietario)
def obtener(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioPropietarioSQLAlchemy(db)
    caso_uso = ObtenerPropietario(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except PropietarioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("", response_model=RespuestaPropietario, status_code=201)
def crear(
    datos: SolicitudCrearPropietario,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioPropietarioSQLAlchemy(db)
    caso_uso = CrearPropietario(repositorio)
    try:
        return caso_uso.ejecutar(
            condominio_id=datos.condominio_id, nombre=datos.nombre,
            apellido=datos.apellido, cedula=datos.cedula, correo=datos.correo,
            telefono=datos.telefono, direccion=datos.direccion,
            usuario_id=datos.usuario_id,
        )
    except PropietarioYaExiste as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", response_model=RespuestaPropietario)
def actualizar(
    id: int, datos: SolicitudActualizarPropietario,
    db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioPropietarioSQLAlchemy(db)
    caso_uso = ActualizarPropietario(repositorio)
    try:
        return caso_uso.ejecutar(
            id=id, condominio_id=datos.condominio_id, nombre=datos.nombre,
            apellido=datos.apellido, cedula=datos.cedula, correo=datos.correo,
            telefono=datos.telefono, direccion=datos.direccion,
            estado=datos.estado, usuario_id=datos.usuario_id,
        )
    except PropietarioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PropietarioYaExiste as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioPropietarioSQLAlchemy(db)
    caso_uso = EliminarPropietario(repositorio)
    try:
        caso_uso.ejecutar(id)
    except PropietarioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
