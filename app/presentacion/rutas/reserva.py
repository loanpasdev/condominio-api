from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.reserva import (
    SolicitudCrearReserva, SolicitudActualizarReserva,
    RespuestaReserva, RespuestaListaReservas,
)
from app.presentacion.dependencias import obtener_usuario_actual
from app.infraestructura.repositorios.repositorio_reserva_sqlalchemy import RepositorioReservaSQLAlchemy
from app.aplicacion.caso_uso.reservas import (
    CrearReserva, ListarReservas, ObtenerReserva, ActualizarReserva, EliminarReserva,
)
from app.dominio.reserva.excepciones import ReservaNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/reservas", tags=["Reservas"])


@router.get("", response_model=RespuestaListaReservas)
def listar(
    buscar: str = Query(None),
    condominio_id: int = Query(None),
    area_comun_id: int = Query(None),
    propietario_id: int = Query(None),
    fecha: str = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(obtener_usuario_actual),
):
    repositorio = RepositorioReservaSQLAlchemy(db)
    caso_uso = ListarReservas(repositorio)
    items, total = caso_uso.ejecutar(
        buscar=buscar, condominio_id=condominio_id,
        area_comun_id=area_comun_id, propietario_id=propietario_id,
        fecha=fecha, pagina=pagina, por_pagina=por_pagina,
    )
    return RespuestaListaReservas(
        items=items, total=total, pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaReserva, status_code=201)
def crear(
    datos: SolicitudCrearReserva,
    db: Session = Depends(obtener_db),
    _usuario=Depends(obtener_usuario_actual),
):
    repositorio = RepositorioReservaSQLAlchemy(db)
    caso_uso = CrearReserva(repositorio)
    return caso_uso.ejecutar(
        condominio_id=datos.condominio_id, area_comun_id=datos.area_comun_id,
        propietario_id=datos.propietario_id, fecha=datos.fecha,
        hora_inicio=datos.hora_inicio, hora_fin=datos.hora_fin,
    )


@router.get("/{id}", response_model=RespuestaReserva)
def obtener(id: int, db: Session = Depends(obtener_db), _usuario=Depends(obtener_usuario_actual)):
    repositorio = RepositorioReservaSQLAlchemy(db)
    caso_uso = ObtenerReserva(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except ReservaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaReserva)
def actualizar(
    id: int, datos: SolicitudActualizarReserva,
    db: Session = Depends(obtener_db), _usuario=Depends(obtener_usuario_actual),
):
    repositorio = RepositorioReservaSQLAlchemy(db)
    caso_uso = ActualizarReserva(repositorio)
    try:
        return caso_uso.ejecutar(
            id=id, fecha=datos.fecha, hora_inicio=datos.hora_inicio,
            hora_fin=datos.hora_fin, estado=datos.estado,
        )
    except ReservaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(obtener_db), _usuario=Depends(obtener_usuario_actual)):
    repositorio = RepositorioReservaSQLAlchemy(db)
    caso_uso = EliminarReserva(repositorio)
    try:
        caso_uso.ejecutar(id)
    except ReservaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
