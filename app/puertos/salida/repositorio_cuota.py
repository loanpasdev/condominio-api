from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.cuota.entidad import Cuota


class RepositorioCuota(ABC):
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Cuota]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, condominio_id: int = None, unidad_id: int = None, mes: int = None, anio: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Cuota], int]:
        pass

    @abstractmethod
    def crear(self, cuota: Cuota) -> Cuota:
        pass

    @abstractmethod
    def actualizar(self, cuota: Cuota) -> Cuota:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
