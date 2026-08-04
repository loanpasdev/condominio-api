from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.modulo.entidad import Modulo


class RepositorioModulo(ABC):
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Modulo]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Modulo], int]:
        pass

    @abstractmethod
    def crear(self, modulo: Modulo) -> Modulo:
        pass

    @abstractmethod
    def actualizar(self, modulo: Modulo) -> Modulo:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass

    @abstractmethod
    def existe_codigo(self, codigo: str, excluir_id: int = None) -> bool:
        pass
