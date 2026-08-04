from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.tipo_cuenta_bancaria import (
    SolicitudCrearTipoCuentaBancaria,
    SolicitudActualizarTipoCuentaBancaria,
    RespuestaTipoCuentaBancaria,
    RespuestaListaTiposCuentaBancaria,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_tipo_cuenta_bancaria_sqlalchemy import RepositorioTipoCuentaBancariaSQLAlchemy
from app.infraestructura.repositorios.repositorio_condominio_sqlalchemy import RepositorioCondominioSQLAlchemy
from app.aplicacion.caso_uso.tipos_cuenta_bancaria import (
    CrearTipoCuentaBancaria,
    ListarTiposCuentaBancaria,
    ObtenerTipoCuentaBancaria,
    ActualizarTipoCuentaBancaria,
    EliminarTipoCuentaBancaria,
)
from app.dominio.tipo_cuenta_bancaria.excepciones import TipoCuentaBancariaNoExiste, TipoCuentaBancariaYaExiste
from app.dominio.condominio.excepciones import CondominioNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/tipos-cuenta-bancaria", tags=["Tipos Cuenta Bancaria"])


@router.get("", response_model=RespuestaListaTiposCuentaBancaria)
def listar(
    buscar: str = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioTipoCuentaBancariaSQLAlchemy(db)
    caso_uso = ListarTiposCuentaBancaria(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaTiposCuentaBancaria(
        items=items,
        total=total,
        pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaTipoCuentaBancaria, status_code=201)
def crear(
    datos: SolicitudCrearTipoCuentaBancaria,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioTipoCuentaBancariaSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = CrearTipoCuentaBancaria(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(nombre=datos.nombre, condominio_id=datos.condominio_id)
    except TipoCuentaBancariaYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id}", response_model=RespuestaTipoCuentaBancaria)
def obtener(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioTipoCuentaBancariaSQLAlchemy(db)
    caso_uso = ObtenerTipoCuentaBancaria(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except TipoCuentaBancariaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaTipoCuentaBancaria)
def actualizar(
    id: int,
    datos: SolicitudActualizarTipoCuentaBancaria,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioTipoCuentaBancariaSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = ActualizarTipoCuentaBancaria(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(
            id=id,
            nombre=datos.nombre,
            condominio_id=datos.condominio_id,
            estado=datos.estado,
        )
    except TipoCuentaBancariaYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))
    except TipoCuentaBancariaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioTipoCuentaBancariaSQLAlchemy(db)
    caso_uso = EliminarTipoCuentaBancaria(repositorio)
    try:
        caso_uso.ejecutar(id)
    except TipoCuentaBancariaNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
