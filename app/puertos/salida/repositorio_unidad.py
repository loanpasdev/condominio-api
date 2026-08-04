from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.unidad.entidad import Unidad


class RepositorioUnidad(ABC):
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Unidad]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Unidad], int]:
        pass

    @abstractmethod
    def crear(self, unidad: Unidad) -> Unidad:
        pass

    @abstractmethod
    def actualizar(self, unidad: Unidad) -> Unidad:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
