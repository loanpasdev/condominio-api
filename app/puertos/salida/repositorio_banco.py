from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.banco.entidad import Banco


class RepositorioBanco(ABC):
    """Puerto de salida para repositorio de bancos"""

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Banco]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Banco], int]:
        pass

    @abstractmethod
    def crear(self, banco: Banco) -> Banco:
        pass

    @abstractmethod
    def actualizar(self, banco: Banco) -> Banco:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass

    @abstractmethod
    def existe_nombre(self, nombre: str, excluir_id: int = None) -> bool:
        pass
