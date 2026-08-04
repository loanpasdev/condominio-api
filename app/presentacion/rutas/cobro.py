from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.cobro import (
    SolicitudCrearCobro, SolicitudActualizarCobro,
    RespuestaCobro, RespuestaListaCobros,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_cobro_sqlalchemy import RepositorioCobroSQLAlchemy
from app.infraestructura.repositorios.repositorio_condominio_sqlalchemy import RepositorioCondominioSQLAlchemy
from app.aplicacion.caso_uso.cobros import (
    CrearCobro, ListarCobros, ObtenerCobro, ActualizarCobro, EliminarCobro,
)
from app.dominio.cobro.excepciones import CobroNoExiste
from app.dominio.condominio.excepciones import CondominioNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/cobros", tags=["Cobros"])


@router.get("", response_model=RespuestaListaCobros)
def listar(
    buscar: str = Query(None),
    condominio_id: int = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioCobroSQLAlchemy(db)
    caso_uso = ListarCobros(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, condominio_id=condominio_id, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaCobros(
        items=items, total=total, pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaCobro, status_code=201)
def crear(
    datos: SolicitudCrearCobro,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioCobroSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = CrearCobro(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(
            condominio_id=datos.condominio_id, categoria_id=datos.categoria_id,
            descripcion=datos.descripcion, monto=datos.monto, fecha=datos.fecha,
            proveedor_id=datos.proveedor_id,
        )
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id}", response_model=RespuestaCobro)
def obtener(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioCobroSQLAlchemy(db)
    caso_uso = ObtenerCobro(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except CobroNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaCobro)
def actualizar(
    id: int, datos: SolicitudActualizarCobro,
    db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioCobroSQLAlchemy(db)
    caso_uso = ActualizarCobro(repositorio)
    try:
        return caso_uso.ejecutar(
            id=id, categoria_id=datos.categoria_id, descripcion=datos.descripcion,
            monto=datos.monto, fecha=datos.fecha, proveedor_id=datos.proveedor_id,
        )
    except CobroNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioCobroSQLAlchemy(db)
    caso_uso = EliminarCobro(repositorio)
    try:
        caso_uso.ejecutar(id)
    except CobroNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
