from fastapi import APIRouter, Depends, HTTPException, Query
from app.presentacion.esquemas.proveedor import (
    SolicitudCrearProveedor,
    SolicitudActualizarProveedor,
    RespuestaProveedor,
    RespuestaListaProveedores,
)
from app.presentacion.dependencias import requerir_admin
from app.infraestructura.repositorios.repositorio_proveedor_sqlalchemy import RepositorioProveedorSQLAlchemy
from app.infraestructura.repositorios.repositorio_condominio_sqlalchemy import RepositorioCondominioSQLAlchemy
from app.aplicacion.caso_uso.proveedores import (
    CrearProveedor,
    ListarProveedores,
    ObtenerProveedor,
    ActualizarProveedor,
    EliminarProveedor,
)
from app.dominio.proveedor.excepciones import ProveedorNoExiste, ProveedorYaExiste
from app.dominio.condominio.excepciones import CondominioNoExiste
from app.database import obtener_db
from sqlalchemy.orm import Session
import math

router = APIRouter(prefix="/api/proveedores", tags=["Proveedores"])


@router.get("", response_model=RespuestaListaProveedores)
def listar(
    buscar: str = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioProveedorSQLAlchemy(db)
    caso_uso = ListarProveedores(repositorio)
    items, total = caso_uso.ejecutar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)
    return RespuestaListaProveedores(
        items=items, total=total, pagina=pagina,
        por_pagina=por_pagina,
        paginas=math.ceil(total / por_pagina) if total > 0 else 0,
    )


@router.post("", response_model=RespuestaProveedor, status_code=201)
def crear(
    datos: SolicitudCrearProveedor,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioProveedorSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = CrearProveedor(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(
            nombre=datos.nombre, rif=datos.rif,
            condominio_id=datos.condominio_id,
            telefono=datos.telefono, email=datos.email,
        )
    except ProveedorYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))
    except CondominioNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id}", response_model=RespuestaProveedor)
def obtener(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioProveedorSQLAlchemy(db)
    caso_uso = ObtenerProveedor(repositorio)
    try:
        return caso_uso.ejecutar(id)
    except ProveedorNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{id}", response_model=RespuestaProveedor)
def actualizar(
    id: int,
    datos: SolicitudActualizarProveedor,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioProveedorSQLAlchemy(db)
    repositorio_condominio = RepositorioCondominioSQLAlchemy(db)
    caso_uso = ActualizarProveedor(repositorio, repositorio_condominio)
    try:
        return caso_uso.ejecutar(
            id=id, nombre=datos.nombre, rif=datos.rif,
            condominio_id=datos.condominio_id,
            telefono=datos.telefono, email=datos.email,
            estado=datos.estado,
        )
    except ProveedorYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))
    except (ProveedorNoExiste, CondominioNoExiste) as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
def eliminar(
    id: int,
    db: Session = Depends(obtener_db),
    _usuario=Depends(requerir_admin),
):
    repositorio = RepositorioProveedorSQLAlchemy(db)
    caso_uso = EliminarProveedor(repositorio)
    try:
        caso_uso.ejecutar(id)
    except ProveedorNoExiste as e:
        raise HTTPException(status_code=404, detail=str(e))
