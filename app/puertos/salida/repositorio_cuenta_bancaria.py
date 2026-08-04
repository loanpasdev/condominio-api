from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.cuenta_bancaria.entidad import CuentaBancaria


class RepositorioCuentaBancaria(ABC):
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[CuentaBancaria]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[CuentaBancaria], int]:
        pass

    @abstractmethod
    def crear(self, cuenta: CuentaBancaria) -> CuentaBancaria:
        pass

    @abstractmethod
    def actualizar(self, cuenta: CuentaBancaria) -> CuentaBancaria:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
