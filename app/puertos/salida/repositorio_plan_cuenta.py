from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.plan_cuenta.entidad import PlanCuenta


class RepositorioPlanCuenta(ABC):
    """Puerto de salida para repositorio de plan de cuentas"""

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[PlanCuenta]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[PlanCuenta], int]:
        pass

    @abstractmethod
    def crear(self, cuenta: PlanCuenta) -> PlanCuenta:
        pass

    @abstractmethod
    def actualizar(self, cuenta: PlanCuenta) -> PlanCuenta:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
