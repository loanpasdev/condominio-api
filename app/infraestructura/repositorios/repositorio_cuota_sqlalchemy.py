from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.dominio.cuota.entidad import Cuota
from app.puertos.salida.repositorio_cuota import RepositorioCuota
from app.infraestructura.modelado.modelo_cuota import CuotaModelo


class RepositorioCuotaSQLAlchemy(RepositorioCuota):
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Cuota]:
        modelo = self.db.query(CuotaModelo).filter(CuotaModelo.id == id).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, condominio_id: int = None, unidad_id: int = None, mes: int = None, anio: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Cuota], int]:
        consulta = self.db.query(CuotaModelo)
        if condominio_id:
            consulta = consulta.filter(CuotaModelo.condominio_id == condominio_id)
        if unidad_id:
            consulta = consulta.filter(CuotaModelo.unidad_id == unidad_id)
        if mes is not None:
            consulta = consulta.filter(CuotaModelo.mes == mes)
        if anio is not None:
            consulta = consulta.filter(CuotaModelo.anio == anio)
        total = consulta.count()
        modelos = consulta.order_by(CuotaModelo.anio.desc(), CuotaModelo.mes.desc()).offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, cuota: Cuota) -> Cuota:
        modelo = CuotaModelo(
            condominio_id=cuota.condominio_id,
            unidad_id=cuota.unidad_id,
            mes=cuota.mes,
            anio=cuota.anio,
            monto_total=cuota.monto_total,
            estado=cuota.estado,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, cuota: Cuota) -> Cuota:
        modelo = self.db.query(CuotaModelo).filter(CuotaModelo.id == cuota.id).first()
        if modelo:
            modelo.monto_total = cuota.monto_total
            modelo.estado = cuota.estado
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(CuotaModelo).filter(CuotaModelo.id == id).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: CuotaModelo) -> Cuota:
        return Cuota(
            id=modelo.id,
            condominio_id=modelo.condominio_id,
            unidad_id=modelo.unidad_id,
            mes=modelo.mes,
            anio=modelo.anio,
            monto_total=float(modelo.monto_total),
            estado=modelo.estado,
        )
