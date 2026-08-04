from typing import Optional, List
from sqlalchemy.orm import Session
from app.dominio.pago.entidad import Pago
from app.puertos.salida.repositorio_pago import RepositorioPago
from app.infraestructura.modelado.modelo_pago import PagoModelo


class RepositorioPagoSQLAlchemy(RepositorioPago):
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Pago]:
        modelo = self.db.query(PagoModelo).filter(PagoModelo.id == id).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, condominio_id: int = None, cuota_id: int = None, propietario_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Pago], int]:
        consulta = self.db.query(PagoModelo)
        if condominio_id:
            consulta = consulta.filter(PagoModelo.condominio_id == condominio_id)
        if cuota_id:
            consulta = consulta.filter(PagoModelo.cuota_id == cuota_id)
        if propietario_id:
            consulta = consulta.filter(PagoModelo.propietario_id == propietario_id)
        total = consulta.count()
        modelos = consulta.order_by(PagoModelo.fecha_pago.desc()).offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, pago: Pago) -> Pago:
        modelo = PagoModelo(
            condominio_id=pago.condominio_id,
            cuota_id=pago.cuota_id,
            propietario_id=pago.propietario_id,
            monto=pago.monto,
            metodo_pago_id=pago.metodo_pago_id,
            moneda_id=pago.moneda_id,
            referencia=pago.referencia,
            fecha_pago=pago.fecha_pago,
            notas=pago.notas,
            estado=pago.estado,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, pago: Pago) -> Pago:
        modelo = self.db.query(PagoModelo).filter(PagoModelo.id == pago.id).first()
        if modelo:
            modelo.monto = pago.monto
            modelo.metodo_pago_id = pago.metodo_pago_id
            modelo.moneda_id = pago.moneda_id
            modelo.referencia = pago.referencia
            modelo.fecha_pago = pago.fecha_pago
            modelo.notas = pago.notas
            modelo.estado = pago.estado
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(PagoModelo).filter(PagoModelo.id == id).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: PagoModelo) -> Pago:
        return Pago(
            id=modelo.id,
            condominio_id=modelo.condominio_id,
            cuota_id=modelo.cuota_id,
            propietario_id=modelo.propietario_id,
            monto=float(modelo.monto),
            metodo_pago_id=modelo.metodo_pago_id,
            moneda_id=modelo.moneda_id,
            referencia=modelo.referencia,
            fecha_pago=modelo.fecha_pago,
            notas=modelo.notas,
            estado=modelo.estado,
        )
