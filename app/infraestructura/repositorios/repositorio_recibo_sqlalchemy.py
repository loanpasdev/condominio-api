from typing import Optional, List
from sqlalchemy.orm import Session
from app.dominio.recibo.entidad import Recibo
from app.puertos.salida.repositorio_recibo import RepositorioRecibo
from app.infraestructura.modelado.modelo_recibo import ReciboModelo


class RepositorioReciboSQLAlchemy(RepositorioRecibo):
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Recibo]:
        modelo = self.db.query(ReciboModelo).filter(ReciboModelo.id == id).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, condominio_id: int = None, factura_id: int = None, unidad_id: int = None, propietario_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Recibo], int]:
        consulta = self.db.query(ReciboModelo)
        if condominio_id:
            consulta = consulta.filter(ReciboModelo.condominio_id == condominio_id)
        if factura_id:
            consulta = consulta.filter(ReciboModelo.factura_id == factura_id)
        if unidad_id:
            consulta = consulta.filter(ReciboModelo.unidad_id == unidad_id)
        if propietario_id:
            consulta = consulta.filter(ReciboModelo.propietario_id == propietario_id)
        total = consulta.count()
        modelos = consulta.order_by(ReciboModelo.fecha_creacion.desc()).offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, recibo: Recibo) -> Recibo:
        modelo = ReciboModelo(
            condominio_id=recibo.condominio_id, factura_id=recibo.factura_id,
            unidad_id=recibo.unidad_id, propietario_id=recibo.propietario_id,
            subtotal=recibo.subtotal, mora=recibo.mora,
            total=recibo.total, estado=recibo.estado,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, recibo: Recibo) -> Recibo:
        modelo = self.db.query(ReciboModelo).filter(ReciboModelo.id == recibo.id).first()
        if modelo:
            modelo.subtotal = recibo.subtotal
            modelo.mora = recibo.mora
            modelo.total = recibo.total
            modelo.estado = recibo.estado
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(ReciboModelo).filter(ReciboModelo.id == id).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: ReciboModelo) -> Recibo:
        return Recibo(
            id=modelo.id, condominio_id=modelo.condominio_id,
            factura_id=modelo.factura_id, unidad_id=modelo.unidad_id,
            propietario_id=modelo.propietario_id, subtotal=float(modelo.subtotal),
            mora=float(modelo.mora), total=float(modelo.total),
            estado=modelo.estado,
        )
