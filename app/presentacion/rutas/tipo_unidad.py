from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.tipo_unidad import (
    SolicitudCrearTipoUnidad,
    SolicitudActualizarTipoUnidad,
    RespuestaTipoUnidad,
    RespuestaListaTiposUnidad,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_tipo_unidad_sqlalchemy import RepositorioTipoUnidadSQLAlchemy
from app.infraestructura.repositorios.repositorio_condominio_sqlalchemy import RepositorioCondominioSQLAlchemy
from app.aplicacion.caso_uso.tipos_unidad import (
    CrearTipoUnidad,
    ListarTiposUnidad,
    ObtenerTipoUnidad,
    ActualizarTipoUnidad,
    EliminarTipoUnidad,
)
from app.dominio.tipo_unidad.excepciones import TipoUnidadNoExiste, TipoUnidadYaExiste
from app.dominio.condominio.excepciones import CondominioNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/tipos-unidad", tags=["Tipos de Unidad"])


@router.get("", response_model=RespuestaListaTiposUnidad)
def listar(
    buscar: str = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioTipoUnidadSQLAlchemy(db)
    caso_uso = ListarTiposUnidad(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaTiposUnidad(
        items=items,
        total=total,
        pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaTipoUnidad, status_code=201)
def crear(
    datos: SolicitudCrearTipoUnidad,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioTipoUnidadSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = CrearTipoUnidad(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(nombre=datos.nombre, condominio_id=datos.condominio_id)
    except TipoUnidadYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id}", response_model=RespuestaTipoUnidad)
def obtener(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioTipoUnidadSQLAlchemy(db)
    caso_uso = ObtenerTipoUnidad(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except TipoUnidadNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaTipoUnidad)
def actualizar(
    id: int,
    datos: SolicitudActualizarTipoUnidad,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioTipoUnidadSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = ActualizarTipoUnidad(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(
            id=id,
            nombre=datos.nombre,
            condominio_id=datos.condominio_id,
            estado=datos.estado,
        )
    except TipoUnidadYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))
    except TipoUnidadNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioTipoUnidadSQLAlchemy(db)
    caso_uso = EliminarTipoUnidad(repositorio)
    try:
        caso_uso.ejecutar(id)
    except TipoUnidadNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
