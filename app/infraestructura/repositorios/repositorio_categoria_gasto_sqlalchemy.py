from typing import Optional, List
from sqlalchemy.orm import Session
from app.dominio.categoria_gasto.entidad import CategoriaGasto
from app.dominio.usuario.valores import EstadoUsuario
from app.puertos.salida.repositorio_categoria_gasto import RepositorioCategoriaGasto
from app.infraestructura.modelado.modelo_categoria_gasto import CategoriaGastoModelo


class RepositorioCategoriaGastoSQLAlchemy(RepositorioCategoriaGasto):
    """Implementacion del repositorio de categorias de gasto con SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[CategoriaGasto]:
        modelo = self.db.query(CategoriaGastoModelo).filter(
            CategoriaGastoModelo.id == id
        ).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[CategoriaGasto], int]:
        consulta = self.db.query(CategoriaGastoModelo)

        if buscar:
            consulta = consulta.filter(
                CategoriaGastoModelo.nombre.ilike(f"%{buscar}%")
            )

        total = consulta.count()
        modelos = consulta.offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, categoria: CategoriaGasto) -> CategoriaGasto:
        modelo = CategoriaGastoModelo(
            nombre=categoria.nombre,
            condominio_id=categoria.condominio_id,
            estado=categoria.estado.value,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, categoria: CategoriaGasto) -> CategoriaGasto:
        modelo = self.db.query(CategoriaGastoModelo).filter(
            CategoriaGastoModelo.id == categoria.id
        ).first()
        if modelo:
            modelo.nombre = categoria.nombre
            modelo.condominio_id = categoria.condominio_id
            modelo.estado = categoria.estado.value
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(CategoriaGastoModelo).filter(
            CategoriaGastoModelo.id == id
        ).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: CategoriaGastoModelo) -> CategoriaGasto:
        return CategoriaGasto(
            id=modelo.id,
            nombre=modelo.nombre,
            condominio_id=modelo.condominio_id,
            estado=EstadoUsuario(modelo.estado),
        )

    def existe_nombre_en_condominio(self, nombre: str, condominio_id: int, excluir_id: int = None) -> bool:
        consulta = self.db.query(CategoriaGastoModelo).filter(
            CategoriaGastoModelo.nombre.ilike(nombre),
            CategoriaGastoModelo.condominio_id == condominio_id,
        )
        if excluir_id:
            consulta = consulta.filter(CategoriaGastoModelo.id != excluir_id)
        return consulta.first() is not None
