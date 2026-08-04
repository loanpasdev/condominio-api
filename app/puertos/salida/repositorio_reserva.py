from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.reserva.entidad import Reserva


class RepositorioReserva(ABC):
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Reserva]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, condominio_id: int = None, area_comun_id: int = None, propietario_id: int = None, fecha: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Reserva], int]:
        pass

    @abstractmethod
    def crear(self, reserva: Reserva) -> Reserva:
        pass

    @abstractmethod
    def actualizar(self, reserva: Reserva) -> Reserva:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
