from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.dominio.condominio.entidad import Condominio
from app.puertos.salida.repositorio_condominio import RepositorioCondominio
from app.infraestructura.modelado.modelo_condominio import CondominioModelo


class RepositorioCondominioSQLAlchemy(RepositorioCondominio):
    """Implementacion del repositorio de condominios con SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Condominio]:
        modelo = self.db.query(CondominioModelo).filter(
            CondominioModelo.id == id
        ).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def obtener_por_rif(self, rif: str) -> Optional[Condominio]:
        modelo = self.db.query(CondominioModelo).filter(
            CondominioModelo.rif == rif
        ).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Condominio], int]:
        consulta = self.db.query(CondominioModelo)

        if buscar:
            filtro = or_(
                CondominioModelo.nombre.ilike(f"%{buscar}%"),
                CondominioModelo.rif.ilike(f"%{buscar}%"),
            )
            consulta = consulta.filter(filtro)

        total = consulta.count()
        modelos = consulta.offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, condominio: Condominio) -> Condominio:
        modelo = CondominioModelo(
            nombre=condominio.nombre,
            rif=condominio.rif,
            direccion=condominio.direccion,
            telefono=condominio.telefono,
            email=condominio.email,
            logo=condominio.logo,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, condominio: Condominio) -> Condominio:
        modelo = self.db.query(CondominioModelo).filter(
            CondominioModelo.id == condominio.id
        ).first()
        if modelo:
            modelo.nombre = condominio.nombre
            modelo.rif = condominio.rif
            modelo.direccion = condominio.direccion
            modelo.telefono = condominio.telefono
            modelo.email = condominio.email
            modelo.logo = condominio.logo
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(CondominioModelo).filter(
            CondominioModelo.id == id
        ).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: CondominioModelo) -> Condominio:
        return Condominio(
            id=modelo.id,
            nombre=modelo.nombre,
            rif=modelo.rif,
            direccion=modelo.direccion,
            telefono=modelo.telefono,
            email=modelo.email,
            logo=modelo.logo,
        )
