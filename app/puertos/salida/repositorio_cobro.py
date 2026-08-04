from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.cobro.entidad import Cobro


class RepositorioCobro(ABC):
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Cobro]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Cobro], int]:
        pass

    @abstractmethod
    def crear(self, cobro: Cobro) -> Cobro:
        pass

    @abstractmethod
    def actualizar(self, cobro: Cobro) -> Cobro:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
