from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.area_comun.entidad import AreaComun


class RepositorioAreaComun(ABC):
    """Puerto de salida para repositorio de areas comunes"""

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[AreaComun]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[AreaComun], int]:
        pass

    @abstractmethod
    def crear(self, area: AreaComun) -> AreaComun:
        pass

    @abstractmethod
    def actualizar(self, area: AreaComun) -> AreaComun:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass

    @abstractmethod
    def existe_nombre_en_condominio(self, nombre: str, condominio_id: int, excluir_id: int = None) -> bool:
        pass
