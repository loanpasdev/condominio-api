from typing import Optional, List
from sqlalchemy.orm import Session
from app.dominio.reserva.entidad import Reserva
from app.puertos.salida.repositorio_reserva import RepositorioReserva
from app.infraestructura.modelado.modelo_reserva import ReservaModelo


class RepositorioReservaSQLAlchemy(RepositorioReserva):
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Reserva]:
        modelo = self.db.query(ReservaModelo).filter(ReservaModelo.id == id).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, condominio_id: int = None, area_comun_id: int = None, propietario_id: int = None, fecha: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Reserva], int]:
        consulta = self.db.query(ReservaModelo)
        if condominio_id:
            consulta = consulta.filter(ReservaModelo.condominio_id == condominio_id)
        if area_comun_id:
            consulta = consulta.filter(ReservaModelo.area_comun_id == area_comun_id)
        if propietario_id:
            consulta = consulta.filter(ReservaModelo.propietario_id == propietario_id)
        if fecha:
            consulta = consulta.filter(ReservaModelo.fecha == fecha)
        total = consulta.count()
        modelos = consulta.order_by(ReservaModelo.fecha.desc()).offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, reserva: Reserva) -> Reserva:
        modelo = ReservaModelo(
            condominio_id=reserva.condominio_id, area_comun_id=reserva.area_comun_id,
            propietario_id=reserva.propietario_id, fecha=reserva.fecha,
            hora_inicio=reserva.hora_inicio, hora_fin=reserva.hora_fin,
            estado=reserva.estado,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, reserva: Reserva) -> Reserva:
        modelo = self.db.query(ReservaModelo).filter(ReservaModelo.id == reserva.id).first()
        if modelo:
            modelo.fecha = reserva.fecha
            modelo.hora_inicio = reserva.hora_inicio
            modelo.hora_fin = reserva.hora_fin
            modelo.estado = reserva.estado
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(ReservaModelo).filter(ReservaModelo.id == id).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: ReservaModelo) -> Reserva:
        return Reserva(
            id=modelo.id, condominio_id=modelo.condominio_id,
            area_comun_id=modelo.area_comun_id, propietario_id=modelo.propietario_id,
            fecha=modelo.fecha, hora_inicio=modelo.hora_inicio,
            hora_fin=modelo.hora_fin, estado=modelo.estado,
        )
