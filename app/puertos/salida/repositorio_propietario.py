from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.propietario.entidad import Propietario


class RepositorioPropietario(ABC):
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Propietario]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, condominio_id: int = None, estado: bool = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Propietario], int]:
        pass

    @abstractmethod
    def crear(self, propietario: Propietario) -> Propietario:
        pass

    @abstractmethod
    def actualizar(self, propietario: Propietario) -> Propietario:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass

    @abstractmethod
    def existe_por_cedula(self, cedula: str, exclude_id: int = None) -> bool:
        pass
