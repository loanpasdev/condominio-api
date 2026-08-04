from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.cuenta_bancaria import (
    SolicitudCrearCuentaBancaria, SolicitudActualizarCuentaBancaria,
    RespuestaCuentaBancaria, RespuestaListaCuentasBancarias,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_cuenta_bancaria_sqlalchemy import RepositorioCuentaBancariaSQLAlchemy
from app.infraestructura.repositorios.repositorio_condominio_sqlalchemy import RepositorioCondominioSQLAlchemy
from app.aplicacion.caso_uso.cuentas_bancarias import (
    CrearCuentaBancaria, ListarCuentasBancarias, ObtenerCuentaBancaria, ActualizarCuentaBancaria, EliminarCuentaBancaria,
)
from app.dominio.cuenta_bancaria.excepciones import CuentaBancariaNoExiste
from app.dominio.condominio.excepciones import CondominioNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/cuentas-bancarias", tags=["Cuentas Bancarias"])


@router.get("", response_model=RespuestaListaCuentasBancarias)
def listar(buscar: str = Query(None), condominio_id: int = Query(None), pagina: int = Query(1, ge=1), por_pagina: int = Query(10, ge=1, le=50), db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioCuentaBancariaSQLAlchemy(db)
    caso_uso = ListarCuentasBancarias(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, condominio_id=condominio_id, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaCuentasBancarias(items=items, total=total, pagina=pagina, por_pagina=por_pagina, paginas=math.ceil(total / por_pagina) if total > 0 else 0)


@router.post("", response_model=RespuestaCuentaBancaria, status_code=201)
def crear(datos: SolicitudCrearCuentaBancaria, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioCuentaBancariaSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = CrearCuentaBancaria(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(condominio_id=datos.condominio_id, banco_id=datos.banco_id, tipo_cuenta_id=datos.tipo_cuenta_id, numero_cuenta=datos.numero_cuenta, titular=datos.titular, moneda_id=datos.moneda_id, saldo=datos.saldo)
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id}", response_model=RespuestaCuentaBancaria)
def obtener(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioCuentaBancariaSQLAlchemy(db)
    caso_uso = ObtenerCuentaBancaria(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except CuentaBancariaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaCuentaBancaria)
def actualizar(id: int, datos: SolicitudActualizarCuentaBancaria, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioCuentaBancariaSQLAlchemy(db)
    caso_uso = ActualizarCuentaBancaria(repositorio)
    try:
        return caso_uso.ejecutar(id=id, banco_id=datos.banco_id, tipo_cuenta_id=datos.tipo_cuenta_id, numero_cuenta=datos.numero_cuenta, titular=datos.titular, moneda_id=datos.moneda_id, saldo=datos.saldo, estado=datos.estado)
    except CuentaBancariaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(obtener_db), _usuario=Depends(requerir_admin)):
    repositorio = RepositorioCuentaBancariaSQLAlchemy(db)
    caso_uso = EliminarCuentaBancaria(repositorio)
    try:
        caso_uso.ejecutar(id)
    except CuentaBancariaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
