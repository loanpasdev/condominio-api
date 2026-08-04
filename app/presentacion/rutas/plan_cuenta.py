from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.plan_cuenta import (
    SolicitudCrearPlanCuenta,
    SolicitudActualizarPlanCuenta,
    RespuestaPlanCuenta,
    RespuestaListaPlanCuentas,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_plan_cuenta_sqlalchemy import RepositorioPlanCuentaSQLAlchemy
from app.aplicacion.caso_uso.plan_cuentas import (
    CrearPlanCuenta,
    ListarPlanCuentas,
    ObtenerPlanCuenta,
    ActualizarPlanCuenta,
    EliminarPlanCuenta,
)
from app.dominio.plan_cuenta.excepciones import PlanCuentaNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/planes-cuentas", tags=["Plan de Cuentas"])


@router.get("", response_model=RespuestaListaPlanCuentas)
def listar(
    buscar: str = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioPlanCuentaSQLAlchemy(db)
    caso_uso = ListarPlanCuentas(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaPlanCuentas(
        items=items, total=total, pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaPlanCuenta, status_code=201)
def crear(
    datos: SolicitudCrearPlanCuenta,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioPlanCuentaSQLAlchemy(db)
    caso_uso = CrearPlanCuenta(repositorio)
    try:
        return caso_uso.ejecutar(
            codigo=datos.codigo, nombre=datos.nombre,
            tipo=datos.tipo, descripcion=datos.descripcion,
            padre_id=datos.padre_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", response_model=RespuestaPlanCuenta)
def obtener(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioPlanCuentaSQLAlchemy(db)
    caso_uso = ObtenerPlanCuenta(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except PlanCuentaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaPlanCuenta)
def actualizar(
    id: int,
    datos: SolicitudActualizarPlanCuenta,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioPlanCuentaSQLAlchemy(db)
    caso_uso = ActualizarPlanCuenta(repositorio)
    try:
        return caso_uso.ejecutar(
            id=id, codigo=datos.codigo, nombre=datos.nombre,
            tipo=datos.tipo, descripcion=datos.descripcion,
            padre_id=datos.padre_id, activo=datos.activo,
        )
    except PlanCuentaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioPlanCuentaSQLAlchemy(db)
    caso_uso = EliminarPlanCuenta(repositorio)
    try:
        caso_uso.ejecutar(id)
    except PlanCuentaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
