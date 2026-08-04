from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.metodo_pago import (
    SolicitudCrearMetodoPago,
    SolicitudActualizarMetodoPago,
    RespuestaMetodoPago,
    RespuestaListaMetodosPago,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_metodo_pago_sqlalchemy import RepositorioMetodoPagoSQLAlchemy
from app.infraestructura.repositorios.repositorio_condominio_sqlalchemy import RepositorioCondominioSQLAlchemy
from app.aplicacion.caso_uso.metodos_pago import (
    CrearMetodoPago,
    ListarMetodosPago,
    ObtenerMetodoPago,
    ActualizarMetodoPago,
    EliminarMetodoPago,
)
from app.dominio.metodo_pago.excepciones import MetodoPagoNoExiste, MetodoPagoYaExiste
from app.dominio.condominio.excepciones import CondominioNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/metodos-pago", tags=["Metodos de Pago"])


@router.get("", response_model=RespuestaListaMetodosPago)
def listar(
    buscar: str = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioMetodoPagoSQLAlchemy(db)
    caso_uso = ListarMetodosPago(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaMetodosPago(
        items=items,
        total=total,
        pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaMetodoPago, status_code=201)
def crear(
    datos: SolicitudCrearMetodoPago,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioMetodoPagoSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = CrearMetodoPago(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(nombre=datos.nombre, condominio_id=datos.condominio_id)
    except MetodoPagoYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id}", response_model=RespuestaMetodoPago)
def obtener(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioMetodoPagoSQLAlchemy(db)
    caso_uso = ObtenerMetodoPago(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except MetodoPagoNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaMetodoPago)
def actualizar(
    id: int,
    datos: SolicitudActualizarMetodoPago,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioMetodoPagoSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = ActualizarMetodoPago(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(
            id=id,
            nombre=datos.nombre,
            condominio_id=datos.condominio_id,
            estado=datos.estado,
        )
    except MetodoPagoYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))
    except MetodoPagoNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioMetodoPagoSQLAlchemy(db)
    caso_uso = EliminarMetodoPago(repositorio)
    try:
        caso_uso.ejecutar(id)
    except MetodoPagoNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
