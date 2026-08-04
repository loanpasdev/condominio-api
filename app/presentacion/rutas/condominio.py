from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.condominio import (
    SolicitudCrearCondominio,
    SolicitudActualizarCondominio,
    RespuestaCondominio,
    RespuestaListaCondominios,
)
from app.presentacion.dependencias import obtener_repositorio_usuario, obtener_usuario_actual, requerir_admin
from app.infraestructura.repositorios.repositorio_condominio_sqlalchemy import RepositorioCondominioSQLAlchemy
from app.aplicacion.caso_uso.condominios import (
    CrearCondominio,
    ListarCondominios,
    ObtenerCondominio,
    ActualizarCondominio,
    EliminarCondominio,
)
from app.dominio.condominio.excepciones import CondominioNoExiste, CondominioYaExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/condominios", tags=["Condominios"])


@router.get("/actual", response_model=RespuestaCondominio)
def obtener_condominio_actual(
    db: Session = Depends(obtener_db),
    _usuario=Depends(obtener_usuario_actual),
):
    repositorio = RepositorioCondominioSQLAlchemy(db)
    items, _ = repositorio.listar(pagina=1, por_pagina=1)
    if not items:
        raise HTTPException(status_code=404, detail="No hay condominios registrados")
    return items[0]


@router.get("", response_model=RespuestaListaCondominios)
def listar(
    buscar: str = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = ListarCondominios(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaCondominios(
        items=items,
        total=total,
        pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaCondominio, status_code=201)
def crear(
    datos: SolicitudCrearCondominio,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = CrearCondominio(repositorio)
    try:
        return caso_uso.ejecutar(
            nombre=datos.nombre,
            rif=datos.rif,
            direccion=datos.direccion,
            telefono=datos.telefono,
            email=datos.email,
            logo=datos.logo,
        )
    except CondominioYaExiste as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", response_model=RespuestaCondominio)
def obtener(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = ObtenerCondominio(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaCondominio)
def actualizar(
    id: int,
    datos: SolicitudActualizarCondominio,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = ActualizarCondominio(repositorio)
    try:
        return caso_uso.ejecutar(
            id=id,
            nombre=datos.nombre,
            rif=datos.rif,
            direccion=datos.direccion,
            telefono=datos.telefono,
            email=datos.email,
            logo=datos.logo,
        )
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CondominioYaExiste as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = EliminarCondominio(repositorio)
    try:
        caso_uso.ejecutar(id)
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
