from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.dominio.propietario.entidad import Propietario
from app.puertos.salida.repositorio_propietario import RepositorioPropietario
from app.infraestructura.modelado.modelo_propietario import PropietarioModelo


class RepositorioPropietarioSQLAlchemy(RepositorioPropietario):
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Propietario]:
        modelo = self.db.query(PropietarioModelo).filter(PropietarioModelo.id == id).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, condominio_id: int = None, estado: bool = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Propietario], int]:
        consulta = self.db.query(PropietarioModelo)
        if buscar:
            consulta = consulta.filter(or_(
                PropietarioModelo.nombre.ilike(f"%{buscar}%"),
                PropietarioModelo.apellido.ilike(f"%{buscar}%"),
                PropietarioModelo.cedula.ilike(f"%{buscar}%"),
                PropietarioModelo.correo.ilike(f"%{buscar}%"),
            ))
        if condominio_id:
            consulta = consulta.filter(PropietarioModelo.condominio_id == condominio_id)
        if estado is not None:
            consulta = consulta.filter(PropietarioModelo.estado == estado)
        total = consulta.count()
        modelos = consulta.order_by(PropietarioModelo.id.desc()).offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, propietario: Propietario) -> Propietario:
        modelo = PropietarioModelo(
            condominio_id=propietario.condominio_id,
            usuario_id=propietario.usuario_id,
            nombre=propietario.nombre,
            apellido=propietario.apellido,
            cedula=propietario.cedula,
            correo=propietario.correo,
            telefono=propietario.telefono,
            direccion=propietario.direccion,
            estado=propietario.estado,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, propietario: Propietario) -> Propietario:
        modelo = self.db.query(PropietarioModelo).filter(PropietarioModelo.id == propietario.id).first()
        if modelo:
            modelo.nombre = propietario.nombre
            modelo.apellido = propietario.apellido
            modelo.cedula = propietario.cedula
            modelo.correo = propietario.correo
            modelo.telefono = propietario.telefono
            modelo.direccion = propietario.direccion
            modelo.estado = propietario.estado
            modelo.usuario_id = propietario.usuario_id
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(PropietarioModelo).filter(PropietarioModelo.id == id).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def existe_por_cedula(self, cedula: str, exclude_id: int = None) -> bool:
        consulta = self.db.query(PropietarioModelo).filter(PropietarioModelo.cedula == cedula)
        if exclude_id:
            consulta = consulta.filter(PropietarioModelo.id != exclude_id)
        return consulta.first() is not None

    def _mapear_a_entidad(self, modelo: PropietarioModelo) -> Propietario:
        return Propietario(
            id=modelo.id,
            condominio_id=modelo.condominio_id,
            usuario_id=modelo.usuario_id,
            nombre=modelo.nombre,
            apellido=modelo.apellido,
            cedula=modelo.cedula,
            correo=modelo.correo,
            telefono=modelo.telefono,
            direccion=modelo.direccion,
            estado=modelo.estado,
        )
