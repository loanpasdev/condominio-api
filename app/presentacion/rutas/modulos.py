from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import obtener_db
from app.presentacion.dependencias import obtener_usuario_actual, requerir_admin
from app.puertos.salida.repositorio_modulo import RepositorioModulo
from app.infraestructura.repositorios.repositorio_modulo_sqlalchemy import RepositorioModuloSQLAlchemy
from app.infraestructura.modelado.modelo_rol_modulo import RolModuloModelo
from app.dominio.modulo.excepciones import ModuloYaExiste, ModuloNoExiste
from app.presentacion.esquemas.modulo import ModuloCrear, ModuloActualizar, ModuloRespuesta

router = APIRouter(prefix="/api/modulos", tags=["Modulos"])


def _obtener_repositorio(db: Session) -> RepositorioModulo:
    return RepositorioModuloSQLAlchemy(db)


def _entidad_a_respuesta(modulo) -> dict:
    return {
        "id": modulo.id,
        "codigo": modulo.codigo,
        "nombre": modulo.nombre,
        "descripcion": modulo.descripcion,
    }


@router.get("")
def listar_modulos(
    buscar: str = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=50),
    usuario_actual=Depends(requerir_admin),
    db: Session = Depends(obtener_db),
):
    repositorio = _obtener_repositorio(db)
    modulos, total = repositorio.listar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)
    return {
        "modulos": [_entidad_a_respuesta(m) for m in modulos],
        "total": total,
        "pagina": pagina,
        "por_pagina": por_pagina,
        "paginas": -(-total // por_pagina) if total else 0,
    }


@router.get("/{modulo_id}")
def obtener_modulo(
    modulo_id: int,
    usuario_actual=Depends(requerir_admin),
    db: Session = Depends(obtener_db),
):
    repositorio = _obtener_repositorio(db)
    modulo = repositorio.obtener_por_id(modulo_id)
    if not modulo:
        raise HTTPException(status_code=404, detail="Modulo no encontrado")
    return _entidad_a_respuesta(modulo)


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_modulo(
    body: ModuloCrear,
    usuario_actual=Depends(requerir_admin),
    db: Session = Depends(obtener_db),
):
    repositorio = _obtener_repositorio(db)
    if repositorio.existe_codigo(body.codigo):
        raise HTTPException(status_code=409, detail=f"Ya existe un modulo con el codigo '{body.codigo}'")
    from app.dominio.modulo.entidad import Modulo
    nuevo = Modulo(codigo=body.codigo, nombre=body.nombre, descripcion=body.descripcion)
    creado = repositorio.crear(nuevo)
    for rol in ["admin", "presidente"]:
        db.add(RolModuloModelo(rol=rol, modulo_id=creado.id))
    db.commit()
    return _entidad_a_respuesta(creado)


@router.put("/{modulo_id}")
def actualizar_modulo(
    modulo_id: int,
    body: ModuloActualizar,
    usuario_actual=Depends(requerir_admin),
    db: Session = Depends(obtener_db),
):
    repositorio = _obtener_repositorio(db)
    modulo = repositorio.obtener_por_id(modulo_id)
    if not modulo:
        raise HTTPException(status_code=404, detail="Modulo no encontrado")
    if repositorio.existe_codigo(body.codigo, excluir_id=modulo_id):
        raise HTTPException(status_code=409, detail=f"Ya existe otro modulo con el codigo '{body.codigo}'")
    modulo.codigo = body.codigo
    modulo.nombre = body.nombre
    modulo.descripcion = body.descripcion
    actualizado = repositorio.actualizar(modulo)
    return _entidad_a_respuesta(actualizado)


@router.delete("/{modulo_id}")
def eliminar_modulo(
    modulo_id: int,
    usuario_actual=Depends(requerir_admin),
    db: Session = Depends(obtener_db),
):
    repositorio = _obtener_repositorio(db)
    modulo = repositorio.obtener_por_id(modulo_id)
    if not modulo:
        raise HTTPException(status_code=404, detail="Modulo no encontrado")
    db.query(RolModuloModelo).filter(RolModuloModelo.modulo_id == modulo_id).delete()
    repositorio.eliminar(modulo_id)
    return {"mensaje": "Modulo eliminado correctamente"}
