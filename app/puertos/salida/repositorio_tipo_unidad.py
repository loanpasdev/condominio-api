from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.tipo_unidad.entidad import TipoUnidad


class RepositorioTipoUnidad(ABC):
    """Puerto de salida para repositorio de tipos de unidad"""

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[TipoUnidad]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[TipoUnidad], int]:
        pass

    @abstractmethod
    def crear(self, tipo_unidad: TipoUnidad) -> TipoUnidad:
        pass

    @abstractmethod
    def actualizar(self, tipo_unidad: TipoUnidad) -> TipoUnidad:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass

    @abstractmethod
    def existe_nombre_en_condominio(self, nombre: str, condominio_id: int, excluir_id: int = None) -> bool:
        pass
