from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.banco import (
    SolicitudCrearBanco,
    SolicitudActualizarBanco,
    RespuestaBanco,
    RespuestaListaBancos,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_banco_sqlalchemy import RepositorioBancoSQLAlchemy
from app.aplicacion.caso_uso.bancos import (
    CrearBanco,
    ListarBancos,
    ObtenerBanco,
    ActualizarBanco,
    EliminarBanco,
)
from app.dominio.banco.excepciones import BancoNoExiste, BancoYaExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/bancos", tags=["Bancos"])


@router.get("", response_model=RespuestaListaBancos)
def listar(
    buscar: str = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioBancoSQLAlchemy(db)
    caso_uso = ListarBancos(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaBancos(
        items=items,
        total=total,
        pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaBanco, status_code=201)
def crear(
    datos: SolicitudCrearBanco,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioBancoSQLAlchemy(db)
    caso_uso = CrearBanco(repositorio)
    try:
        return caso_uso.ejecutar(codigo=datos.codigo, nombre=datos.nombre)
    except BancoYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", response_model=RespuestaBanco)
def obtener(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioBancoSQLAlchemy(db)
    caso_uso = ObtenerBanco(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except BancoNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaBanco)
def actualizar(
    id: int,
    datos: SolicitudActualizarBanco,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioBancoSQLAlchemy(db)
    caso_uso = ActualizarBanco(repositorio)
    try:
        return caso_uso.ejecutar(id=id, codigo=datos.codigo, nombre=datos.nombre)
    except BancoYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BancoNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioBancoSQLAlchemy(db)
    caso_uso = EliminarBanco(repositorio)
    try:
        caso_uso.ejecutar(id)
    except BancoNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
