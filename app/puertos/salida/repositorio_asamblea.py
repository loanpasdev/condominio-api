from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.asamblea.entidad import Asamblea


class RepositorioAsamblea(ABC):
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Asamblea]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Asamblea], int]:
        pass

    @abstractmethod
    def crear(self, asamblea: Asamblea) -> Asamblea:
        pass

    @abstractmethod
    def actualizar(self, asamblea: Asamblea) -> Asamblea:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
