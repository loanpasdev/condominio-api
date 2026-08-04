from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.pago.entidad import Pago


class RepositorioPago(ABC):
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Pago]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, condominio_id: int = None, cuota_id: int = None, propietario_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Pago], int]:
        pass

    @abstractmethod
    def crear(self, pago: Pago) -> Pago:
        pass

    @abstractmethod
    def actualizar(self, pago: Pago) -> Pago:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
