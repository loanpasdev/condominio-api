from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.dominio.banco.entidad import Banco
from app.puertos.salida.repositorio_banco import RepositorioBanco
from app.infraestructura.modelado.modelo_banco import BancoModelo


class RepositorioBancoSQLAlchemy(RepositorioBanco):
    """Implementacion del repositorio de bancos con SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Banco]:
        modelo = self.db.query(BancoModelo).filter(
            BancoModelo.id == id
        ).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Banco], int]:
        consulta = self.db.query(BancoModelo)

        if buscar:
            consulta = consulta.filter(
                or_(
                    BancoModelo.nombre.ilike(f"%{buscar}%"),
                    BancoModelo.codigo.ilike(f"%{buscar}%"),
                )
            )

        total = consulta.count()
        modelos = consulta.offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, banco: Banco) -> Banco:
        modelo = BancoModelo(
            codigo=banco.codigo,
            nombre=banco.nombre,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, banco: Banco) -> Banco:
        modelo = self.db.query(BancoModelo).filter(
            BancoModelo.id == banco.id
        ).first()
        if modelo:
            modelo.codigo = banco.codigo
            modelo.nombre = banco.nombre
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(BancoModelo).filter(
            BancoModelo.id == id
        ).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def existe_nombre(self, nombre: str, excluir_id: int = None) -> bool:
        consulta = self.db.query(BancoModelo).filter(BancoModelo.nombre.ilike(nombre))
        if excluir_id:
            consulta = consulta.filter(BancoModelo.id != excluir_id)
        return consulta.first() is not None

    def _mapear_a_entidad(self, modelo: BancoModelo) -> Banco:
        return Banco(
            id=modelo.id,
            codigo=modelo.codigo,
            nombre=modelo.nombre,
        )
