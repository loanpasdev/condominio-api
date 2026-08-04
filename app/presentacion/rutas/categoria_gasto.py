from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.categoria_gasto import (
    SolicitudCrearCategoriaGasto,
    SolicitudActualizarCategoriaGasto,
    RespuestaCategoriaGasto,
    RespuestaListaCategoriasGasto,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_categoria_gasto_sqlalchemy import RepositorioCategoriaGastoSQLAlchemy
from app.infraestructura.repositorios.repositorio_condominio_sqlalchemy import RepositorioCondominioSQLAlchemy
from app.aplicacion.caso_uso.categorias_gasto import (
    CrearCategoriaGasto,
    ListarCategoriasGasto,
    ObtenerCategoriaGasto,
    ActualizarCategoriaGasto,
    EliminarCategoriaGasto,
)
from app.dominio.categoria_gasto.excepciones import CategoriaGastoNoExiste, CategoriaGastoYaExiste
from app.dominio.condominio.excepciones import CondominioNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/categorias-gasto", tags=["Categorias de Gasto"])


@router.get("", response_model=RespuestaListaCategoriasGasto)
def listar(
    buscar: str = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioCategoriaGastoSQLAlchemy(db)
    caso_uso = ListarCategoriasGasto(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaCategoriasGasto(
        items=items, total=total, pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaCategoriaGasto, status_code=201)
def crear(
    datos: SolicitudCrearCategoriaGasto,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioCategoriaGastoSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = CrearCategoriaGasto(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(nombre=datos.nombre, condominio_id=datos.condominio_id)
    except CategoriaGastoYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id}", response_model=RespuestaCategoriaGasto)
def obtener(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioCategoriaGastoSQLAlchemy(db)
    caso_uso = ObtenerCategoriaGasto(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except CategoriaGastoNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaCategoriaGasto)
def actualizar(
    id: int,
    datos: SolicitudActualizarCategoriaGasto,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioCategoriaGastoSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = ActualizarCategoriaGasto(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(
            id=id, nombre=datos.nombre,
            condominio_id=datos.condominio_id, estado=datos.estado,
        )
    except CategoriaGastoYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))
    except (CategoriaGastoNoExiste, CondominioNoExiste) as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioCategoriaGastoSQLAlchemy(db)
    caso_uso = EliminarCategoriaGasto(repositorio)
    try:
        caso_uso.ejecutar(id)
    except CategoriaGastoNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
