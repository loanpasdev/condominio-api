from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.cuota import (
    SolicitudCrearCuota, SolicitudActualizarCuota,
    RespuestaCuota, RespuestaListaCuotas,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_cuota_sqlalchemy import RepositorioCuotaSQLAlchemy
from app.infraestructura.repositorios.repositorio_condominio_sqlalchemy import RepositorioCondominioSQLAlchemy
from app.aplicacion.caso_uso.cuotas import (
    CrearCuota, ListarCuotas, ObtenerCuota, ActualizarCuota, EliminarCuota,
)
from app.dominio.cuota.excepciones import CuotaNoExiste
from app.dominio.condominio.excepciones import CondominioNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/cuotas", tags=["Cuotas"])


@router.get("", response_model=RespuestaListaCuotas)
def listar(
    buscar: str = Query(None),
    condominio_id: int = Query(None),
    unidad_id: int = Query(None),
    mes: int = Query(None),
    anio: int = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioCuotaSQLAlchemy(db)
    caso_uso = ListarCuotas(repositorio)
    items, total = caso_uso.ejecutar(
        buscar=buscar, condominio_id=condominio_id, unidad_id=unidad_id,
        mes=mes, anio=anio, pagina=pagina, por_pagina=por_pagina,
    )
    return RespuestaListaCuotas(
        items=items, total=total, pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaCuota, status_code=201)
def crear(
    datos: SolicitudCrearCuota,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioCuotaSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = CrearCuota(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(
            condominio_id=datos.condominio_id, unidad_id=datos.unidad_id,
            mes=datos.mes, anio=datos.anio, monto_total=datos.monto_total,
        )
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id}", response_model=RespuestaCuota)
def obtener(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioCuotaSQLAlchemy(db)
    caso_uso = ObtenerCuota(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except CuotaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaCuota)
def actualizar(
    id: int, datos: SolicitudActualizarCuota,
    db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioCuotaSQLAlchemy(db)
    caso_uso = ActualizarCuota(repositorio)
    try:
        return caso_uso.ejecutar(id=id, monto_total=datos.monto_total, estado=datos.estado)
    except CuotaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioCuotaSQLAlchemy(db)
    caso_uso = EliminarCuota(repositorio)
    try:
        caso_uso.ejecutar(id)
    except CuotaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
