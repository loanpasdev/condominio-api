from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.recibo import (
    SolicitudCrearRecibo, SolicitudActualizarRecibo,
    RespuestaRecibo, RespuestaListaRecibos,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_recibo_sqlalchemy import RepositorioReciboSQLAlchemy
from app.aplicacion.caso_uso.recibos import (
    CrearRecibo, ListarRecibos, ObtenerRecibo, ActualizarRecibo, EliminarRecibo,
)
from app.dominio.recibo.excepciones import ReciboNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/recibos", tags=["Recibos"])


@router.get("", response_model=RespuestaListaRecibos)
def listar(condominio_id: int = Query(None), factura_id: int = Query(None), unidad_id: int = Query(None), propietario_id: int = Query(None), pagina: int = Query(1, ge=1), por_pagina: int = Query(10, ge=1, le=50), db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioReciboSQLAlchemy(db)
    caso_uso = ListarRecibos(repositorio)
    items, total = caso_uso.ejecutar(condominio_id=condominio_id, factura_id=factura_id, unidad_id=unidad_id, propietario_id=propietario_id, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaRecibos(items=items, total=total, pagina=pagina, por_pagina=por_pagina, paginas=math.ceil(total / por_pagina) if total > 0 else 0)


@router.post("", response_model=RespuestaRecibo, status_code=201)
def crear(datos: SolicitudCrearRecibo, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioReciboSQLAlchemy(db)
    caso_uso = CrearRecibo(repositorio)
    return caso_uso.ejecutar(condominio_id=datos.condominio_id, factura_id=datos.factura_id, unidad_id=datos.unidad_id, propietario_id=datos.propietario_id, subtotal=datos.subtotal, total=datos.total, mora=datos.mora)


@router.get("/{id}", response_model=RespuestaRecibo)
def obtener(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioReciboSQLAlchemy(db)
    caso_uso = ObtenerRecibo(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except ReciboNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaRecibo)
def actualizar(id: int, datos: SolicitudActualizarRecibo, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioReciboSQLAlchemy(db)
    caso_uso = ActualizarRecibo(repositorio)
    try:
        return caso_uso.ejecutar(id=id, subtotal=datos.subtotal, mora=datos.mora, total=datos.total, estado=datos.estado)
    except ReciboNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioReciboSQLAlchemy(db)
    caso_uso = EliminarRecibo(repositorio)
    try:
        caso_uso.ejecutar(id)
    except ReciboNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
