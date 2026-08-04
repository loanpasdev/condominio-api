from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.factura import (
    SolicitudCrearFactura, SolicitudActualizarFactura,
    RespuestaFactura, RespuestaListaFacturas,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_factura_sqlalchemy import RepositorioFacturaSQLAlchemy
from app.aplicacion.caso_uso.facturas import (
    CrearFactura, ListarFacturas, ObtenerFactura, ActualizarFactura, EliminarFactura,
)
from app.dominio.factura.excepciones import FacturaNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/facturas", tags=["Facturas"])


@router.get("", response_model=RespuestaListaFacturas)
def listar(buscar: str = Query(None), condominio_id: int = Query(None), pagina: int = Query(1, ge=1), por_pagina: int = Query(10, ge=1, le=50), db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioFacturaSQLAlchemy(db)
    caso_uso = ListarFacturas(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, condominio_id=condominio_id, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaFacturas(items=items, total=total, pagina=pagina, por_pagina=por_pagina, paginas=math.ceil(total / por_pagina) if total > 0 else 0)


@router.post("", response_model=RespuestaFactura, status_code=201)
def crear(datos: SolicitudCrearFactura, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioFacturaSQLAlchemy(db)
    caso_uso = CrearFactura(repositorio)
    return caso_uso.ejecutar(condominio_id=datos.condominio_id, numero=datos.numero, descripcion=datos.descripcion, monto_total=datos.monto_total, fecha=datos.fecha, distribucion=datos.distribucion, destino_id=datos.destino_id)


@router.get("/{id}", response_model=RespuestaFactura)
def obtener(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioFacturaSQLAlchemy(db)
    caso_uso = ObtenerFactura(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except FacturaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaFactura)
def actualizar(id: int, datos: SolicitudActualizarFactura, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioFacturaSQLAlchemy(db)
    caso_uso = ActualizarFactura(repositorio)
    try:
        return caso_uso.ejecutar(id=id, numero=datos.numero, descripcion=datos.descripcion, monto_total=datos.monto_total, fecha=datos.fecha, distribucion=datos.distribucion, destino_id=datos.destino_id, estado=datos.estado)
    except FacturaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioFacturaSQLAlchemy(db)
    caso_uso = EliminarFactura(repositorio)
    try:
        caso_uso.ejecutar(id)
    except FacturaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
