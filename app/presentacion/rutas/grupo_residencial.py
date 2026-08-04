from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.grupo_residencial import (
    SolicitudCrearGrupoResidencial,
    SolicitudActualizarGrupoResidencial,
    RespuestaGrupoResidencial,
    RespuestaListaGruposResidenciales,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_grupo_residencial_sqlalchemy import RepositorioGrupoResidencialSQLAlchemy
from app.infraestructura.repositorios.repositorio_condominio_sqlalchemy import RepositorioCondominioSQLAlchemy
from app.aplicacion.caso_uso.grupos_residenciales import (
    CrearGrupoResidencial,
    ListarGruposResidenciales,
    ObtenerGrupoResidencial,
    ActualizarGrupoResidencial,
    EliminarGrupoResidencial,
)
from app.dominio.grupo_residencial.excepciones import GrupoResidencialNoExiste, GrupoResidencialYaExiste
from app.dominio.condominio.excepciones import CondominioNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/grupos-residenciales", tags=["Grupos Residenciales"])


@router.get("", response_model=RespuestaListaGruposResidenciales)
def listar(
    buscar: str = Query(None),
    condominio_id: int = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioGrupoResidencialSQLAlchemy(db)
    caso_uso = ListarGruposResidenciales(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, condominio_id=condominio_id, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaGruposResidenciales(
        items=items, total=total, pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaGrupoResidencial, status_code=201)
def crear(
    datos: SolicitudCrearGrupoResidencial,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioGrupoResidencialSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = CrearGrupoResidencial(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(
            condominio_id=datos.condominio_id, nombre=datos.nombre,
            descripcion=datos.descripcion,
        )
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
    except GrupoResidencialYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/{id}", response_model=RespuestaGrupoResidencial)
def obtener(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioGrupoResidencialSQLAlchemy(db)
    caso_uso = ObtenerGrupoResidencial(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except GrupoResidencialNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaGrupoResidencial)
def actualizar(
    id: int,
    datos: SolicitudActualizarGrupoResidencial,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioGrupoResidencialSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = ActualizarGrupoResidencial(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(
            id=id, nombre=datos.nombre,
            descripcion=datos.descripcion, estado=datos.estado,
        )
    except GrupoResidencialNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
    except GrupoResidencialYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioGrupoResidencialSQLAlchemy(db)
    caso_uso = EliminarGrupoResidencial(repositorio)
    try:
        caso_uso.ejecutar(id)
    except GrupoResidencialNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
