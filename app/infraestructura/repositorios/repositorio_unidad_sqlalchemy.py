from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.dominio.unidad.entidad import Unidad
from app.puertos.salida.repositorio_unidad import RepositorioUnidad
from app.infraestructura.modelado.modelo_unidad import UnidadModelo


class RepositorioUnidadSQLAlchemy(RepositorioUnidad):
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Unidad]:
        modelo = self.db.query(UnidadModelo).filter(UnidadModelo.id == id).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Unidad], int]:
        consulta = self.db.query(UnidadModelo)
        if buscar:
            consulta = consulta.filter(UnidadModelo.numero.ilike(f"%{buscar}%"))
        if condominio_id:
            consulta = consulta.filter(UnidadModelo.condominio_id == condominio_id)
        total = consulta.count()
        modelos = consulta.offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, unidad: Unidad) -> Unidad:
        modelo = UnidadModelo(
            condominio_id=unidad.condominio_id,
            tipo_unidad_id=unidad.tipo_unidad_id,
            propietario_id=unidad.propietario_id,
            numero=unidad.numero,
            piso=unidad.piso,
            grupo_residencial_id=unidad.grupo_residencial_id,
            habitaciones=unidad.habitaciones,
            banios=unidad.banios,
            terraza=unidad.terraza,
            balcon=unidad.balcon,
            parking=unidad.parking,
            notas=unidad.notas,
            metraje=unidad.metraje,
            porcentual=unidad.porcentual,
            estado=unidad.estado,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, unidad: Unidad) -> Unidad:
        modelo = self.db.query(UnidadModelo).filter(UnidadModelo.id == unidad.id).first()
        if modelo:
            modelo.condominio_id = unidad.condominio_id
            modelo.tipo_unidad_id = unidad.tipo_unidad_id
            modelo.propietario_id = unidad.propietario_id
            modelo.numero = unidad.numero
            modelo.piso = unidad.piso
            modelo.grupo_residencial_id = unidad.grupo_residencial_id
            modelo.habitaciones = unidad.habitaciones
            modelo.banios = unidad.banios
            modelo.terraza = unidad.terraza
            modelo.balcon = unidad.balcon
            modelo.parking = unidad.parking
            modelo.notas = unidad.notas
            modelo.metraje = unidad.metraje
            modelo.porcentual = unidad.porcentual
            modelo.estado = unidad.estado
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(UnidadModelo).filter(UnidadModelo.id == id).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: UnidadModelo) -> Unidad:
        return Unidad(
            id=modelo.id,
            condominio_id=modelo.condominio_id,
            tipo_unidad_id=modelo.tipo_unidad_id,
            propietario_id=modelo.propietario_id,
            numero=modelo.numero,
            piso=modelo.piso,
            grupo_residencial_id=modelo.grupo_residencial_id,
            habitaciones=modelo.habitaciones,
            banios=modelo.banios,
            terraza=modelo.terraza,
            balcon=modelo.balcon,
            parking=modelo.parking,
            notas=modelo.notas,
            metraje=float(modelo.metraje),
            porcentual=float(modelo.porcentual),
            estado=modelo.estado,
        )
