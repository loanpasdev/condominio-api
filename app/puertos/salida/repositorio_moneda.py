from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.moneda.entidad import Moneda


class RepositorioMoneda(ABC):
    """Puerto de salida para repositorio de monedas"""

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Moneda]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Moneda], int]:
        pass

    @abstractmethod
    def crear(self, moneda: Moneda) -> Moneda:
        pass

    @abstractmethod
    def actualizar(self, moneda: Moneda) -> Moneda:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass

    @abstractmethod
    def existe_nombre(self, nombre: str, excluir_id: int = None) -> bool:
        pass
