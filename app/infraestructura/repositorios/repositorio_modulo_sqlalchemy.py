from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.dominio.modulo.entidad import Modulo
from app.puertos.salida.repositorio_modulo import RepositorioModulo
from app.infraestructura.modelado.modelo_modulo import ModuloModelo


class RepositorioModuloSQLAlchemy(RepositorioModulo):
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Modulo]:
        modelo = self.db.query(ModuloModelo).filter(ModuloModelo.id == id).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Modulo], int]:
        consulta = self.db.query(ModuloModelo)
        if buscar:
            consulta = consulta.filter(
                or_(
                    ModuloModelo.codigo.ilike(f"%{buscar}%"),
                    ModuloModelo.nombre.ilike(f"%{buscar}%"),
                )
            )
        total = consulta.count()
        modelos = consulta.order_by(ModuloModelo.id).offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, modulo: Modulo) -> Modulo:
        modelo = ModuloModelo(
            codigo=modulo.codigo,
            nombre=modulo.nombre,
            descripcion=modulo.descripcion,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, modulo: Modulo) -> Modulo:
        modelo = self.db.query(ModuloModelo).filter(ModuloModelo.id == modulo.id).first()
        if modelo:
            modelo.codigo = modulo.codigo
            modelo.nombre = modulo.nombre
            modelo.descripcion = modulo.descripcion
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(ModuloModelo).filter(ModuloModelo.id == id).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def existe_codigo(self, codigo: str, excluir_id: int = None) -> bool:
        consulta = self.db.query(ModuloModelo).filter(ModuloModelo.codigo.ilike(codigo))
        if excluir_id:
            consulta = consulta.filter(ModuloModelo.id != excluir_id)
        return consulta.first() is not None

    def _mapear_a_entidad(self, modelo: ModuloModelo) -> Modulo:
        return Modulo(
            id=modelo.id,
            codigo=modelo.codigo,
            nombre=modelo.nombre,
            descripcion=modelo.descripcion,
        )
