from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.notificacion import (
    SolicitudCrearNotificacion, SolicitudActualizarNotificacion,
    RespuestaNotificacion, RespuestaListaNotificaciones,
)
from app.presentacion.dependencias import obtener_usuario_actual
from app.infraestructura.repositorios.repositorio_notificacion_sqlalchemy import RepositorioNotificacionSQLAlchemy
from app.aplicacion.caso_uso.notificaciones import (
    CrearNotificacion, ListarNotificaciones, ObtenerNotificacion, ActualizarNotificacion, EliminarNotificacion,
)
from app.dominio.notificacion.excepciones import NotificacionNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/notificaciones", tags=["Notificaciones"])


@router.get("", response_model=RespuestaListaNotificaciones)
def listar(
    buscar: str = Query(None),
    condominio_id: int = Query(None),
    usuario_id: int = Query(None),
    tipo: str = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(obtener_usuario_actual),
):
    repositorio = RepositorioNotificacionSQLAlchemy(db)
    caso_uso = ListarNotificaciones(repositorio)
    items, total = caso_uso.ejecutar(
        buscar=buscar, condominio_id=condominio_id,
        usuario_id=usuario_id, tipo=tipo,
        pagina=pagina, por_pagina=por_pagina,
    )
    return RespuestaListaNotificaciones(
        items=items, total=total, pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaNotificacion, status_code=201)
def crear(
    datos: SolicitudCrearNotificacion,
    db: Session = Depends(obtener_db),
    _usuario=Depends(obtener_usuario_actual),
):
    repositorio = RepositorioNotificacionSQLAlchemy(db)
    caso_uso = CrearNotificacion(repositorio)
    return caso_uso.ejecutar(
        condominio_id=datos.condominio_id, titulo=datos.titulo,
        mensaje=datos.mensaje, tipo=datos.tipo, usuario_id=datos.usuario_id,
    )


@router.get("/{id}", response_model=RespuestaNotificacion)
def obtener(id: int, db: Session = Depends(obtener_db), _usuario=Depends(obtener_usuario_actual)):
    repositorio = RepositorioNotificacionSQLAlchemy(db)
    caso_uso = ObtenerNotificacion(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except NotificacionNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaNotificacion)
def actualizar(
    id: int, datos: SolicitudActualizarNotificacion,
    db: Session = Depends(obtener_db), _usuario=Depends(obtener_usuario_actual),
):
    repositorio = RepositorioNotificacionSQLAlchemy(db)
    caso_uso = ActualizarNotificacion(repositorio)
    try:
        return caso_uso.ejecutar(
            id=id, titulo=datos.titulo, mensaje=datos.mensaje,
            tipo=datos.tipo, leida=datos.leida,
        )
    except NotificacionNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(obtener_db), _usuario=Depends(obtener_usuario_actual)):
    repositorio = RepositorioNotificacionSQLAlchemy(db)
    caso_uso = EliminarNotificacion(repositorio)
    try:
        caso_uso.ejecutar(id)
    except NotificacionNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
