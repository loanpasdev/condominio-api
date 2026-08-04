from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.moneda import (
    SolicitudCrearMoneda,
    SolicitudActualizarMoneda,
    RespuestaMoneda,
    RespuestaListaMonedas,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_moneda_sqlalchemy import RepositorioMonedaSQLAlchemy
from app.aplicacion.caso_uso.monedas import (
    CrearMoneda,
    ListarMonedas,
    ObtenerMoneda,
    ActualizarMoneda,
    EliminarMoneda,
)
from app.dominio.moneda.excepciones import MonedaNoExiste, MonedaYaExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/monedas", tags=["Monedas"])


@router.get("", response_model=RespuestaListaMonedas)
def listar(
    buscar: str = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioMonedaSQLAlchemy(db)
    caso_uso = ListarMonedas(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaMonedas(
        items=items,
        total=total,
        pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaMoneda, status_code=201)
def crear(
    datos: SolicitudCrearMoneda,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioMonedaSQLAlchemy(db)
    caso_uso = CrearMoneda(repositorio)
    try:
        return caso_uso.ejecutar(codigo=datos.codigo, nombre=datos.nombre, simbolo=datos.simbolo, es_base=datos.es_base, tasa_cambio=datos.tasa_cambio)
    except MonedaYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", response_model=RespuestaMoneda)
def obtener(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioMonedaSQLAlchemy(db)
    caso_uso = ObtenerMoneda(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except MonedaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaMoneda)
def actualizar(
    id: int,
    datos: SolicitudActualizarMoneda,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioMonedaSQLAlchemy(db)
    caso_uso = ActualizarMoneda(repositorio)
    try:
        return caso_uso.ejecutar(
            id=id,
            codigo=datos.codigo,
            nombre=datos.nombre,
            simbolo=datos.simbolo,
            estado=datos.estado,
            es_base=datos.es_base,
            tasa_cambio=datos.tasa_cambio,
        )
    except MonedaYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))
    except MonedaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioMonedaSQLAlchemy(db)
    caso_uso = EliminarMoneda(repositorio)
    try:
        caso_uso.ejecutar(id)
    except MonedaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
