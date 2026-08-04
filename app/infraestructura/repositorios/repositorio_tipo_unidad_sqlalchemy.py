from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.dominio.tipo_unidad.entidad import TipoUnidad
from app.dominio.usuario.valores import EstadoUsuario
from app.puertos.salida.repositorio_tipo_unidad import RepositorioTipoUnidad
from app.infraestructura.modelado.modelo_tipo_unidad import TipoUnidadModelo


class RepositorioTipoUnidadSQLAlchemy(RepositorioTipoUnidad):
    """Implementacion del repositorio de tipos de unidad con SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[TipoUnidad]:
        modelo = self.db.query(TipoUnidadModelo).filter(
            TipoUnidadModelo.id == id
        ).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[TipoUnidad], int]:
        consulta = self.db.query(TipoUnidadModelo)

        if buscar:
            consulta = consulta.filter(
                TipoUnidadModelo.nombre.ilike(f"%{buscar}%")
            )

        total = consulta.count()
        modelos = consulta.offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, tipo_unidad: TipoUnidad) -> TipoUnidad:
        modelo = TipoUnidadModelo(
            nombre=tipo_unidad.nombre,
            condominio_id=tipo_unidad.condominio_id,
            estado=tipo_unidad.estado.value,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, tipo_unidad: TipoUnidad) -> TipoUnidad:
        modelo = self.db.query(TipoUnidadModelo).filter(
            TipoUnidadModelo.id == tipo_unidad.id
        ).first()
        if modelo:
            modelo.nombre = tipo_unidad.nombre
            modelo.condominio_id = tipo_unidad.condominio_id
            modelo.estado = tipo_unidad.estado.value
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(TipoUnidadModelo).filter(
            TipoUnidadModelo.id == id
        ).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: TipoUnidadModelo) -> TipoUnidad:
        return TipoUnidad(
            id=modelo.id,
            nombre=modelo.nombre,
            condominio_id=modelo.condominio_id,
            estado=EstadoUsuario(modelo.estado),
        )

    def existe_nombre_en_condominio(self, nombre: str, condominio_id: int, excluir_id: int = None) -> bool:
        consulta = self.db.query(TipoUnidadModelo).filter(
            TipoUnidadModelo.nombre.ilike(nombre),
            TipoUnidadModelo.condominio_id == condominio_id,
        )
        if excluir_id:
            consulta = consulta.filter(TipoUnidadModelo.id != excluir_id)
        return consulta.first() is not None
