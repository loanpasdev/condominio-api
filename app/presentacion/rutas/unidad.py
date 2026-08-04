from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.unidad import (
    SolicitudCrearUnidad, SolicitudActualizarUnidad, SolicitudDuplicarUnidad,
    RespuestaUnidad, RespuestaListaUnidades,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_unidad_sqlalchemy import RepositorioUnidadSQLAlchemy
from app.infraestructura.repositorios.repositorio_condominio_sqlalchemy import RepositorioCondominioSQLAlchemy
from app.aplicacion.caso_uso.unidades import (
    CrearUnidad, ListarUnidades, ObtenerUnidad, ActualizarUnidad, EliminarUnidad, DuplicarUnidad,
)
from app.dominio.unidad.excepciones import UnidadNoExiste
from app.dominio.condominio.excepciones import CondominioNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/unidades", tags=["Unidades"])


@router.get("", response_model=RespuestaListaUnidades)
def listar(
    buscar: str = Query(None),
    condominio_id: int = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioUnidadSQLAlchemy(db)
    caso_uso = ListarUnidades(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, condominio_id=condominio_id, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaUnidades(
        items=items, total=total, pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaUnidad, status_code=201)
def crear(
    datos: SolicitudCrearUnidad,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioUnidadSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = CrearUnidad(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(
            condominio_id=datos.condominio_id, tipo_unidad_id=datos.tipo_unidad_id,
            numero=datos.numero, metraje=datos.metraje, porcentual=datos.porcentual,
            propietario_id=datos.propietario_id, piso=datos.piso,
            grupo_residencial_id=datos.grupo_residencial_id, habitaciones=datos.habitaciones, banios=datos.banios,
            terraza=datos.terraza, balcon=datos.balcon, parking=datos.parking, notas=datos.notas,
        )
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{id}/duplicar", response_model=RespuestaUnidad, status_code=201)
def duplicar(
    id: int,
    datos: SolicitudDuplicarUnidad,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioUnidadSQLAlchemy(db)
    caso_uso = DuplicarUnidad(repositorio)
    try:
        return caso_uso.ejecutar(id=id, numero=datos.numero)
    except UnidadNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id}", response_model=RespuestaUnidad)
def obtener(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioUnidadSQLAlchemy(db)
    caso_uso = ObtenerUnidad(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except UnidadNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaUnidad)
def actualizar(
    id: int, datos: SolicitudActualizarUnidad,
    db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioUnidadSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = ActualizarUnidad(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(
            id=id, condominio_id=datos.condominio_id, tipo_unidad_id=datos.tipo_unidad_id,
            numero=datos.numero, metraje=datos.metraje, porcentual=datos.porcentual,
            propietario_id=datos.propietario_id, piso=datos.piso, estado=datos.estado,
            grupo_residencial_id=datos.grupo_residencial_id, habitaciones=datos.habitaciones, banios=datos.banios,
            terraza=datos.terraza, balcon=datos.balcon, parking=datos.parking, notas=datos.notas,
        )
    except (UnidadNoExiste, CondominioNoExiste) as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioUnidadSQLAlchemy(db)
    caso_uso = EliminarUnidad(repositorio)
    try:
        caso_uso.ejecutar(id)
    except UnidadNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
