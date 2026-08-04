from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.dominio.factura.entidad import Factura
from app.puertos.salida.repositorio_factura import RepositorioFactura
from app.infraestructura.modelado.modelo_factura import FacturaModelo


class RepositorioFacturaSQLAlchemy(RepositorioFactura):
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Factura]:
        modelo = self.db.query(FacturaModelo).filter(FacturaModelo.id == id).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Factura], int]:
        consulta = self.db.query(FacturaModelo)
        if buscar:
            consulta = consulta.filter(or_(FacturaModelo.numero.ilike(f"%{buscar}%"), FacturaModelo.descripcion.ilike(f"%{buscar}%")))
        if condominio_id:
            consulta = consulta.filter(FacturaModelo.condominio_id == condominio_id)
        total = consulta.count()
        modelos = consulta.order_by(FacturaModelo.fecha.desc()).offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, factura: Factura) -> Factura:
        modelo = FacturaModelo(
            condominio_id=factura.condominio_id, numero=factura.numero,
            descripcion=factura.descripcion, monto_total=factura.monto_total,
            fecha=factura.fecha, distribucion=factura.distribucion,
            destino_id=factura.destino_id, estado=factura.estado,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, factura: Factura) -> Factura:
        modelo = self.db.query(FacturaModelo).filter(FacturaModelo.id == factura.id).first()
        if modelo:
            modelo.numero = factura.numero
            modelo.descripcion = factura.descripcion
            modelo.monto_total = factura.monto_total
            modelo.fecha = factura.fecha
            modelo.distribucion = factura.distribucion
            modelo.destino_id = factura.destino_id
            modelo.estado = factura.estado
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(FacturaModelo).filter(FacturaModelo.id == id).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: FacturaModelo) -> Factura:
        return Factura(
            id=modelo.id, condominio_id=modelo.condominio_id,
            numero=modelo.numero, descripcion=modelo.descripcion,
            monto_total=float(modelo.monto_total), fecha=modelo.fecha,
            distribucion=modelo.distribucion, destino_id=modelo.destino_id,
            estado=modelo.estado,
        )
