from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.dominio.solicitud.entidad import Solicitud
from app.puertos.salida.repositorio_solicitud import RepositorioSolicitud
from app.infraestructura.modelado.modelo_solicitud import SolicitudModelo


class RepositorioSolicitudSQLAlchemy(RepositorioSolicitud):
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Solicitud]:
        modelo = self.db.query(SolicitudModelo).filter(SolicitudModelo.id == id).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, condominio_id: int = None, propietario_id: int = None, estado: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Solicitud], int]:
        consulta = self.db.query(SolicitudModelo)
        if buscar:
            consulta = consulta.filter(or_(SolicitudModelo.titulo.ilike(f"%{buscar}%"), SolicitudModelo.descripcion.ilike(f"%{buscar}%")))
        if condominio_id:
            consulta = consulta.filter(SolicitudModelo.condominio_id == condominio_id)
        if propietario_id:
            consulta = consulta.filter(SolicitudModelo.propietario_id == propietario_id)
        if estado:
            consulta = consulta.filter(SolicitudModelo.estado == estado)
        total = consulta.count()
        modelos = consulta.order_by(SolicitudModelo.fecha_creacion.desc()).offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, solicitud: Solicitud) -> Solicitud:
        modelo = SolicitudModelo(
            condominio_id=solicitud.condominio_id, propietario_id=solicitud.propietario_id,
            titulo=solicitud.titulo, descripcion=solicitud.descripcion,
            categoria=solicitud.categoria, prioridad=solicitud.prioridad,
            estado=solicitud.estado, responsable=solicitud.responsable,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, solicitud: Solicitud) -> Solicitud:
        modelo = self.db.query(SolicitudModelo).filter(SolicitudModelo.id == solicitud.id).first()
        if modelo:
            modelo.titulo = solicitud.titulo
            modelo.descripcion = solicitud.descripcion
            modelo.categoria = solicitud.categoria
            modelo.prioridad = solicitud.prioridad
            modelo.estado = solicitud.estado
            modelo.responsable = solicitud.responsable
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(SolicitudModelo).filter(SolicitudModelo.id == id).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: SolicitudModelo) -> Solicitud:
        return Solicitud(
            id=modelo.id, condominio_id=modelo.condominio_id,
            propietario_id=modelo.propietario_id, titulo=modelo.titulo,
            descripcion=modelo.descripcion, categoria=modelo.categoria,
            prioridad=modelo.prioridad, estado=modelo.estado,
            responsable=modelo.responsable,
        )
