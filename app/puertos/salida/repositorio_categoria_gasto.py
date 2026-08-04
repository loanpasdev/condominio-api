from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.categoria_gasto.entidad import CategoriaGasto


class RepositorioCategoriaGasto(ABC):
    """Puerto de salida para repositorio de categorias de gasto"""

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[CategoriaGasto]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[CategoriaGasto], int]:
        pass

    @abstractmethod
    def crear(self, categoria: CategoriaGasto) -> CategoriaGasto:
        pass

    @abstractmethod
    def actualizar(self, categoria: CategoriaGasto) -> CategoriaGasto:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass

    @abstractmethod
    def existe_nombre_en_condominio(self, nombre: str, condominio_id: int, excluir_id: int = None) -> bool:
        pass
