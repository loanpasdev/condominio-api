from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.area_comun import (
    SolicitudCrearAreaComun,
    SolicitudActualizarAreaComun,
    RespuestaAreaComun,
    RespuestaListaAreasComunes,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_area_comun_sqlalchemy import RepositorioAreaComunSQLAlchemy
from app.infraestructura.repositorios.repositorio_condominio_sqlalchemy import RepositorioCondominioSQLAlchemy
from app.aplicacion.caso_uso.areas_comunes import (
    CrearAreaComun,
    ListarAreasComunes,
    ObtenerAreaComun,
    ActualizarAreaComun,
    EliminarAreaComun,
)
from app.dominio.area_comun.excepciones import AreaComunNoExiste, AreaComunYaExiste
from app.dominio.condominio.excepciones import CondominioNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/areas-comunes", tags=["Areas Comunes"])


@router.get("", response_model=RespuestaListaAreasComunes)
def listar(
    buscar: str = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioAreaComunSQLAlchemy(db)
    caso_uso = ListarAreasComunes(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaAreasComunes(
        items=items, total=total, pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaAreaComun, status_code=201)
def crear(
    datos: SolicitudCrearAreaComun,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioAreaComunSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = CrearAreaComun(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(
            nombre=datos.nombre, condominio_id=datos.condominio_id,
            descripcion=datos.descripcion, capacidad=datos.capacidad,
            tarifa=datos.tarifa, hora_inicio=datos.hora_inicio,
            hora_fin=datos.hora_fin,
        )
    except AreaComunYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id}", response_model=RespuestaAreaComun)
def obtener(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioAreaComunSQLAlchemy(db)
    caso_uso = ObtenerAreaComun(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except AreaComunNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaAreaComun)
def actualizar(
    id: int,
    datos: SolicitudActualizarAreaComun,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioAreaComunSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = ActualizarAreaComun(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(
            id=id, nombre=datos.nombre, condominio_id=datos.condominio_id,
            descripcion=datos.descripcion, capacidad=datos.capacidad,
            tarifa=datos.tarifa, hora_inicio=datos.hora_inicio,
            hora_fin=datos.hora_fin, estado=datos.estado,
        )
    except AreaComunYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))
    except (AreaComunNoExiste, CondominioNoExiste) as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioAreaComunSQLAlchemy(db)
    caso_uso = EliminarAreaComun(repositorio)
    try:
        caso_uso.ejecutar(id)
    except AreaComunNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
