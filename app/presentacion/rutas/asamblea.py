from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.asamblea import (
    SolicitudCrearAsamblea, SolicitudActualizarAsamblea,
    RespuestaAsamblea, RespuestaListaAsambleas,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_asamblea_sqlalchemy import RepositorioAsambleaSQLAlchemy
from app.aplicacion.caso_uso.asambleas import (
    CrearAsamblea, ListarAsambleas, ObtenerAsamblea, ActualizarAsamblea, EliminarAsamblea,
)
from app.dominio.asamblea.excepciones import AsambleaNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/asambleas", tags=["Asambleas"])


@router.get("", response_model=RespuestaListaAsambleas)
def listar(buscar: str = Query(None), condominio_id: int = Query(None), pagina: int = Query(1, ge=1), por_pagina: int = Query(10, ge=1, le=50), db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioAsambleaSQLAlchemy(db)
    caso_uso = ListarAsambleas(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, condominio_id=condominio_id, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaAsambleas(items=items, total=total, pagina=pagina, por_pagina=por_pagina, paginas=math.ceil(total / por_pagina) if total > 0 else 0)


@router.post("", response_model=RespuestaAsamblea, status_code=201)
def crear(datos: SolicitudCrearAsamblea, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioAsambleaSQLAlchemy(db)
    caso_uso = CrearAsamblea(repositorio)
    return caso_uso.ejecutar(condominio_id=datos.condominio_id, tipo=datos.tipo, titulo=datos.titulo, fecha=datos.fecha, hora=datos.hora, quorum_requerido=datos.quorum_requerido, descripcion=datos.descripcion, lugar=datos.lugar)


@router.get("/{id}", response_model=RespuestaAsamblea)
def obtener(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioAsambleaSQLAlchemy(db)
    caso_uso = ObtenerAsamblea(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except AsambleaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaAsamblea)
def actualizar(id: int, datos: SolicitudActualizarAsamblea, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioAsambleaSQLAlchemy(db)
    caso_uso = ActualizarAsamblea(repositorio)
    try:
        return caso_uso.ejecutar(id=id, titulo=datos.titulo, descripcion=datos.descripcion, fecha=datos.fecha, hora=datos.hora, lugar=datos.lugar, quorum_requerido=datos.quorum_requerido, quorum_obtenido=datos.quorum_obtenido, estado=datos.estado)
    except AsambleaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioAsambleaSQLAlchemy(db)
    caso_uso = EliminarAsamblea(repositorio)
    try:
        caso_uso.ejecutar(id)
    except AsambleaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
