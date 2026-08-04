from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.dominio.notificacion.entidad import Notificacion
from app.puertos.salida.repositorio_notificacion import RepositorioNotificacion
from app.infraestructura.modelado.modelo_notificacion import NotificacionModelo


class RepositorioNotificacionSQLAlchemy(RepositorioNotificacion):
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Notificacion]:
        modelo = self.db.query(NotificacionModelo).filter(NotificacionModelo.id == id).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, condominio_id: int = None, usuario_id: int = None, tipo: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Notificacion], int]:
        consulta = self.db.query(NotificacionModelo)
        if buscar:
            consulta = consulta.filter(or_(NotificacionModelo.titulo.ilike(f"%{buscar}%"), NotificacionModelo.mensaje.ilike(f"%{buscar}%")))
        if condominio_id:
            consulta = consulta.filter(NotificacionModelo.condominio_id == condominio_id)
        if usuario_id:
            consulta = consulta.filter(NotificacionModelo.usuario_id == usuario_id)
        if tipo:
            consulta = consulta.filter(NotificacionModelo.tipo == tipo)
        total = consulta.count()
        modelos = consulta.order_by(NotificacionModelo.fecha_creacion.desc()).offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, notificacion: Notificacion) -> Notificacion:
        modelo = NotificacionModelo(
            condominio_id=notificacion.condominio_id, usuario_id=notificacion.usuario_id,
            titulo=notificacion.titulo, mensaje=notificacion.mensaje,
            tipo=notificacion.tipo, leida=notificacion.leida,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, notificacion: Notificacion) -> Notificacion:
        modelo = self.db.query(NotificacionModelo).filter(NotificacionModelo.id == notificacion.id).first()
        if modelo:
            modelo.titulo = notificacion.titulo
            modelo.mensaje = notificacion.mensaje
            modelo.tipo = notificacion.tipo
            modelo.leida = notificacion.leida
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(NotificacionModelo).filter(NotificacionModelo.id == id).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: NotificacionModelo) -> Notificacion:
        return Notificacion(
            id=modelo.id, condominio_id=modelo.condominio_id,
            usuario_id=modelo.usuario_id, titulo=modelo.titulo,
            mensaje=modelo.mensaje, tipo=modelo.tipo, leida=modelo.leida,
        )
