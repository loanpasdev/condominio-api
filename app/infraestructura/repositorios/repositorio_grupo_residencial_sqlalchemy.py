from typing import Optional, List
from sqlalchemy.orm import Session
from app.dominio.grupo_residencial import GrupoResidencial
from app.puertos.salida.repositorio_grupo_residencial import RepositorioGrupoResidencial
from app.infraestructura.modelado.modelo_grupo_residencial import GrupoResidencialModelo


class RepositorioGrupoResidencialSQLAlchemy(RepositorioGrupoResidencial):
    """Implementacion del repositorio de grupos residenciales con SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[GrupoResidencial]:
        modelo = self.db.query(GrupoResidencialModelo).filter(
            GrupoResidencialModelo.id == id
        ).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[GrupoResidencial], int]:
        consulta = self.db.query(GrupoResidencialModelo)

        if buscar:
            consulta = consulta.filter(
                GrupoResidencialModelo.nombre.ilike(f"%{buscar}%")
            )

        if condominio_id:
            consulta = consulta.filter(
                GrupoResidencialModelo.condominio_id == condominio_id
            )

        total = consulta.count()
        modelos = consulta.offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, grupo: GrupoResidencial) -> GrupoResidencial:
        modelo = GrupoResidencialModelo(
            nombre=grupo.nombre,
            descripcion=grupo.descripcion,
            condominio_id=grupo.condominio_id,
            estado=grupo.estado,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, grupo: GrupoResidencial) -> GrupoResidencial:
        modelo = self.db.query(GrupoResidencialModelo).filter(
            GrupoResidencialModelo.id == grupo.id
        ).first()
        if modelo:
            modelo.nombre = grupo.nombre
            modelo.descripcion = grupo.descripcion
            modelo.condominio_id = grupo.condominio_id
            modelo.estado = grupo.estado
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(GrupoResidencialModelo).filter(
            GrupoResidencialModelo.id == id
        ).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def existe_nombre_en_condominio(self, nombre: str, condominio_id: int, excluir_id: int = None) -> bool:
        consulta = self.db.query(GrupoResidencialModelo).filter(
            GrupoResidencialModelo.nombre.ilike(nombre),
            GrupoResidencialModelo.condominio_id == condominio_id,
        )
        if excluir_id:
            consulta = consulta.filter(GrupoResidencialModelo.id != excluir_id)
        return consulta.first() is not None

    def _mapear_a_entidad(self, modelo: GrupoResidencialModelo) -> GrupoResidencial:
        return GrupoResidencial(
            id=modelo.id,
            nombre=modelo.nombre,
            descripcion=modelo.descripcion,
            condominio_id=modelo.condominio_id,
            estado=bool(modelo.estado) if modelo.estado is not None else True,
        )
