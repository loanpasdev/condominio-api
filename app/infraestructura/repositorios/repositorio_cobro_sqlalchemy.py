from typing import Optional, List
from sqlalchemy.orm import Session
from app.dominio.cobro.entidad import Cobro
from app.puertos.salida.repositorio_cobro import RepositorioCobro
from app.infraestructura.modelado.modelo_cobro import CobroModelo


class RepositorioCobroSQLAlchemy(RepositorioCobro):
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Cobro]:
        modelo = self.db.query(CobroModelo).filter(CobroModelo.id == id).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Cobro], int]:
        consulta = self.db.query(CobroModelo)
        if buscar:
            consulta = consulta.filter(CobroModelo.descripcion.ilike(f"%{buscar}%"))
        if condominio_id:
            consulta = consulta.filter(CobroModelo.condominio_id == condominio_id)
        total = consulta.count()
        modelos = consulta.order_by(CobroModelo.fecha.desc()).offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, cobro: Cobro) -> Cobro:
        modelo = CobroModelo(
            condominio_id=cobro.condominio_id,
            categoria_id=cobro.categoria_id,
            proveedor_id=cobro.proveedor_id,
            descripcion=cobro.descripcion,
            monto=cobro.monto,
            fecha=cobro.fecha,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, cobro: Cobro) -> Cobro:
        modelo = self.db.query(CobroModelo).filter(CobroModelo.id == cobro.id).first()
        if modelo:
            modelo.categoria_id = cobro.categoria_id
            modelo.proveedor_id = cobro.proveedor_id
            modelo.descripcion = cobro.descripcion
            modelo.monto = cobro.monto
            modelo.fecha = cobro.fecha
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(CobroModelo).filter(CobroModelo.id == id).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: CobroModelo) -> Cobro:
        return Cobro(
            id=modelo.id,
            condominio_id=modelo.condominio_id,
            categoria_id=modelo.categoria_id,
            proveedor_id=modelo.proveedor_id,
            descripcion=modelo.descripcion,
            monto=float(modelo.monto),
            fecha=modelo.fecha,
        )
