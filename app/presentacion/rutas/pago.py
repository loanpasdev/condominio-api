from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.pago import (
    SolicitudCrearPago, SolicitudActualizarPago,
    RespuestaPago, RespuestaListaPagos,
)
from app.presentacion.dependencias import requerir_admin, obtener_usuario_actual
from app.infraestructura.repositorios.repositorio_pago_sqlalchemy import RepositorioPagoSQLAlchemy
from app.infraestructura.repositorios.repositorio_condominio_sqlalchemy import RepositorioCondominioSQLAlchemy
from app.aplicacion.caso_uso.pagos import (
    CrearPago, ListarPagos, ObtenerPago, ActualizarPago, EliminarPago,
)
from app.dominio.pago.excepciones import PagoNoExiste
from app.dominio.condominio.excepciones import CondominioNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/pagos", tags=["Pagos"])


@router.get("", response_model=RespuestaListaPagos)
def listar(
    buscar: str = Query(None),
    condominio_id: int = Query(None),
    cuota_id: int = Query(None),
    propietario_id: int = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioPagoSQLAlchemy(db)
    caso_uso = ListarPagos(repositorio)
    items, total = caso_uso.ejecutar(
        buscar=buscar, condominio_id=condominio_id, cuota_id=cuota_id,
        propietario_id=propietario_id, pagina=pagina, por_pagina=por_pagina,
    )
    return RespuestaListaPagos(
        items=items, total=total, pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaPago, status_code=201)
def crear(
    datos: SolicitudCrearPago,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioPagoSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = CrearPago(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(
            condominio_id=datos.condominio_id, cuota_id=datos.cuota_id,
            propietario_id=datos.propietario_id, monto=datos.monto,
            metodo_pago_id=datos.metodo_pago_id, moneda_id=datos.moneda_id,
            fecha_pago=datos.fecha_pago, referencia=datos.referencia, notas=datos.notas,
        )
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id}", response_model=RespuestaPago)
def obtener(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioPagoSQLAlchemy(db)
    caso_uso = ObtenerPago(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except PagoNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaPago)
def actualizar(
    id: int, datos: SolicitudActualizarPago,
    db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioPagoSQLAlchemy(db)
    caso_uso = ActualizarPago(repositorio)
    try:
        return caso_uso.ejecutar(
            id=id, monto=datos.monto, metodo_pago_id=datos.metodo_pago_id,
            moneda_id=datos.moneda_id, referencia=datos.referencia,
            fecha_pago=datos.fecha_pago, notas=datos.notas, estado=datos.estado,
        )
    except PagoNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioPagoSQLAlchemy(db)
    caso_uso = EliminarPago(repositorio)
    try:
        caso_uso.ejecutar(id)
    except PagoNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
