from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.condominio.entidad import Condominio


class RepositorioCondominio(ABC):
    """Puerto de salida para repositorio de condominios"""

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Condominio]:
        pass

    @abstractmethod
    def obtener_por_rif(self, rif: str) -> Optional[Condominio]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Condominio], int]:
        pass

    @abstractmethod
    def crear(self, condominio: Condominio) -> Condominio:
        pass

    @abstractmethod
    def actualizar(self, condominio: Condominio) -> Condominio:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
