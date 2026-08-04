from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.solicitud import (
    SolicitudCrearSolicitud, SolicitudActualizarSolicitud,
    RespuestaSolicitud, RespuestaListaSolicitudes,
)
from app.presentacion.dependencias import obtener_usuario_actual
from app.infraestructura.repositorios.repositorio_solicitud_sqlalchemy import RepositorioSolicitudSQLAlchemy
from app.aplicacion.caso_uso.solicitudes import (
    CrearSolicitud, ListarSolicitudes, ObtenerSolicitud, ActualizarSolicitud, EliminarSolicitud,
)
from app.dominio.solicitud.excepciones import SolicitudNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/solicitudes", tags=["Solicitudes"])


@router.get("", response_model=RespuestaListaSolicitudes)
def listar(
    buscar: str = Query(None),
    condominio_id: int = Query(None),
    propietario_id: int = Query(None),
    estado: str = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(obtener_usuario_actual),
):
    repositorio = RepositorioSolicitudSQLAlchemy(db)
    caso_uso = ListarSolicitudes(repositorio)
    items, total = caso_uso.ejecutar(
        buscar=buscar, condominio_id=condominio_id,
        propietario_id=propietario_id, estado=estado,
        pagina=pagina, por_pagina=por_pagina,
    )
    return RespuestaListaSolicitudes(
        items=items, total=total, pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaSolicitud, status_code=201)
def crear(
    datos: SolicitudCrearSolicitud,
    db: Session = Depends(obtener_db),
    _usuario=Depends(obtener_usuario_actual),
):
    repositorio = RepositorioSolicitudSQLAlchemy(db)
    caso_uso = CrearSolicitud(repositorio)
    return caso_uso.ejecutar(
        condominio_id=datos.condominio_id, propietario_id=datos.propietario_id,
        titulo=datos.titulo, descripcion=datos.descripcion,
        categoria=datos.categoria, prioridad=datos.prioridad,
        responsable=datos.responsable,
    )


@router.get("/{id}", response_model=RespuestaSolicitud)
def obtener(id: int, db: Session = Depends(obtener_db), _usuario=Depends(obtener_usuario_actual)):
    repositorio = RepositorioSolicitudSQLAlchemy(db)
    caso_uso = ObtenerSolicitud(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except SolicitudNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaSolicitud)
def actualizar(
    id: int, datos: SolicitudActualizarSolicitud,
    db: Session = Depends(obtener_db), _usuario=Depends(obtener_usuario_actual),
):
    repositorio = RepositorioSolicitudSQLAlchemy(db)
    caso_uso = ActualizarSolicitud(repositorio)
    try:
        return caso_uso.ejecutar(
            id=id, titulo=datos.titulo, descripcion=datos.descripcion,
            categoria=datos.categoria, prioridad=datos.prioridad,
            estado=datos.estado, responsable=datos.responsable,
        )
    except SolicitudNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(obtener_db), _usuario=Depends(obtener_usuario_actual)):
    repositorio = RepositorioSolicitudSQLAlchemy(db)
    caso_uso = EliminarSolicitud(repositorio)
    try:
        caso_uso.ejecutar(id)
    except SolicitudNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
