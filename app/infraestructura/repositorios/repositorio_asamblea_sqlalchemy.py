from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.dominio.asamblea.entidad import Asamblea
from app.puertos.salida.repositorio_asamblea import RepositorioAsamblea
from app.infraestructura.modelado.modelo_asamblea import AsambleaModelo


class RepositorioAsambleaSQLAlchemy(RepositorioAsamblea):
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Asamblea]:
        modelo = self.db.query(AsambleaModelo).filter(AsambleaModelo.id == id).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Asamblea], int]:
        consulta = self.db.query(AsambleaModelo)
        if buscar:
            consulta = consulta.filter(or_(AsambleaModelo.titulo.ilike(f"%{buscar}%"), AsambleaModelo.descripcion.ilike(f"%{buscar}%")))
        if condominio_id:
            consulta = consulta.filter(AsambleaModelo.condominio_id == condominio_id)
        total = consulta.count()
        modelos = consulta.order_by(AsambleaModelo.fecha.desc()).offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, asamblea: Asamblea) -> Asamblea:
        modelo = AsambleaModelo(
            condominio_id=asamblea.condominio_id, tipo=asamblea.tipo,
            titulo=asamblea.titulo, descripcion=asamblea.descripcion,
            fecha=asamblea.fecha, hora=asamblea.hora,
            lugar=asamblea.lugar, quorum_requerido=asamblea.quorum_requerido,
            quorum_obtenido=asamblea.quorum_obtenido, estado=asamblea.estado,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, asamblea: Asamblea) -> Asamblea:
        modelo = self.db.query(AsambleaModelo).filter(AsambleaModelo.id == asamblea.id).first()
        if modelo:
            modelo.titulo = asamblea.titulo
            modelo.descripcion = asamblea.descripcion
            modelo.fecha = asamblea.fecha
            modelo.hora = asamblea.hora
            modelo.lugar = asamblea.lugar
            modelo.quorum_requerido = asamblea.quorum_requerido
            modelo.quorum_obtenido = asamblea.quorum_obtenido
            modelo.estado = asamblea.estado
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(AsambleaModelo).filter(AsambleaModelo.id == id).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: AsambleaModelo) -> Asamblea:
        return Asamblea(
            id=modelo.id, condominio_id=modelo.condominio_id,
            tipo=modelo.tipo, titulo=modelo.titulo,
            descripcion=modelo.descripcion, fecha=modelo.fecha,
            hora=modelo.hora, lugar=modelo.lugar,
            quorum_requerido=float(modelo.quorum_requerido),
            quorum_obtenido=float(modelo.quorum_obtenido),
            estado=modelo.estado,
        )
